#!/usr/bin/env python3
"""Validate a lightweight, fixed-roster scene ledger (standard library only).

Checks structured state and event replay; does not evaluate prompt or video semantics.
"""
from __future__ import annotations
import argparse
import copy
import json
import math
from pathlib import Path
import sys

CHAR_FIELDS = ("position", "posture", "body_direction", "eyeline", "left_hand", "right_hand", "action_phase", "emotion", "knowledge")
PROP_FIELDS = ("holder", "hand", "location", "orientation", "functional_state")

def number(value):
    return type(value) in (int, float) and math.isfinite(value)

def nonempty(value):
    return isinstance(value, str) and bool(value.strip())

def validate_state(state, where, errors):
    if not isinstance(state, dict) or set(state) != {"scene", "characters", "props"}:
        errors.append(f"{where}: state requires scene, characters and props only")
        return False
    if not nonempty(state["scene"]):
        errors.append(f"{where}: scene must be a nonempty string")
    for group, fields in (("characters", CHAR_FIELDS), ("props", PROP_FIELDS)):
        assets = state[group]
        if not isinstance(assets, dict):
            errors.append(f"{where}.{group}: must be an object")
            continue
        if group == "characters" and not assets:
            errors.append(f"{where}: characters cannot be empty")
        for asset, values in assets.items():
            label = f"{where}.{group}.{asset}"
            if not nonempty(asset) or "." in asset:
                errors.append(f"{label}: ID must be nonempty and contain no dots")
            if not isinstance(values, dict) or set(values) != set(fields):
                errors.append(f"{label}: requires exactly {', '.join(fields)}")
                continue
            for field, value in values.items():
                if field == "knowledge":
                    if not isinstance(value, list) or not all(nonempty(x) for x in value) or (isinstance(value, list) and len({str(x) for x in value}) != len(value)):
                        errors.append(f"{label}.knowledge: requires unique nonempty fact IDs")
                elif field in ("holder", "hand"):
                    if value is not None and not nonempty(value):
                        errors.append(f"{label}.{field}: must be a string or null")
                elif not nonempty(value):
                    errors.append(f"{label}.{field}: must be a nonempty string")
            if group == "props":
                holder, hand = values["holder"], values["hand"]
                characters = state.get("characters", {})
                if holder is None:
                    if hand is not None:
                        errors.append(f"{label}: an unheld prop must have null hand")
                elif not isinstance(characters, dict) or not isinstance(holder, str) or holder not in characters or hand not in ("left", "right", "both"):
                    errors.append(f"{label}: holder must exist and hand must be left/right/both")
    return True

def audit(data, max_shot_seconds=4.0):
    errors = []
    if not isinstance(data, dict) or data.get("schema_version") != 1 or type(data.get("schema_version")) is not int:
        return {"errors": ["schema_version must be integer 1"], "warnings": [], "segments": 0}
    limit = data.get("model_max_seconds")
    if type(limit) is not int or limit <= 0:
        errors.append("model_max_seconds must be a positive integer")
    segments = data.get("segments")
    if not isinstance(segments, list) or not segments:
        return {"errors": errors + ["segments must be a nonempty list"], "warnings": [], "segments": 0}
    previous_exit = None
    seen_segments = set()
    for index, segment in enumerate(segments, 1):
        where = f"segment[{index}]"
        if not isinstance(segment, dict):
            errors.append(f"{where}: must be an object")
            continue
        sid = segment.get("id")
        if type(sid) is not int or sid != index or sid in seen_segments:
            errors.append(f"{where}: id must be consecutive from 1")
        if type(sid) is int:
            seen_segments.add(sid)
        duration = segment.get("duration")
        if type(duration) is not int or duration <= 0 or (type(limit) is int and duration > limit):
            errors.append(f"{where}: duration must be positive integer within model_max_seconds")
        entry, expected_exit = segment.get("entry"), segment.get("exit")
        valid = validate_state(entry, where + ".entry", errors)
        validate_state(expected_exit, where + ".exit", errors)
        if previous_exit is not None and entry != previous_exit:
            errors.append(f"{where}: entry differs from previous exit; repair this boundary")
        previous_exit = expected_exit
        if not valid:
            continue
        state = copy.deepcopy(entry)
        shots = segment.get("shots")
        if not isinstance(shots, list) or not shots:
            errors.append(f"{where}: shots must be a nonempty list")
            continue
        end_previous = 0.0
        seen_shots = set()
        for shot_index, shot in enumerate(shots, 1):
            sw = f"{where}.shot[{shot_index}]"
            if not isinstance(shot, dict):
                errors.append(f"{sw}: must be an object")
                continue
            shot_id = shot.get("id")
            if not nonempty(shot_id) or shot_id in seen_shots:
                errors.append(f"{sw}: shot id must be unique and nonempty")
            if isinstance(shot_id, str):
                seen_shots.add(shot_id)
            start, end = shot.get("start"), shot.get("end")
            if not number(start) or not number(end) or end <= start:
                errors.append(f"{sw}: invalid shot times")
            else:
                if abs(start - end_previous) > 1e-7:
                    errors.append(f"{sw}: timecode gap/overlap or nonzero start")
                if end - start > max_shot_seconds + 1e-7:
                    errors.append(f"{sw}: shot exceeds {max_shot_seconds:g}s")
                if any(abs(t * 10 - round(t * 10)) > 1e-7 for t in (start, end)):
                    errors.append(f"{sw}: timecodes must align to 0.1s")
                end_previous = end
            if not nonempty(shot.get("event")):
                errors.append(f"{sw}: event needs a visible action or stimulus")
            changes = shot.get("changes")
            if not isinstance(changes, list):
                errors.append(f"{sw}: changes must be a list")
                continue
            for change in changes:
                if not isinstance(change, dict) or set(change) != {"path", "before", "after"}:
                    errors.append(f"{sw}: each change needs path/before/after only")
                    continue
                path = change["path"]
                parts = path.split(".") if isinstance(path, str) else []
                if len(parts) != 3 or parts[0] not in ("characters", "props"):
                    errors.append(f"{sw}: invalid path {path!r}")
                    continue
                group, asset, field = parts
                values = state.get(group, {})
                values = values.get(asset) if isinstance(values, dict) else None
                if not isinstance(values, dict) or field not in values:
                    errors.append(f"{sw}: unknown state path {path!r}")
                    continue
                if values[field] != change["before"]:
                    errors.append(f"{sw}: {path} before does not match current state")
                    continue
                if change["before"] == change["after"]:
                    errors.append(f"{sw}: {path} change has no effect")
                values[field] = copy.deepcopy(change["after"])
            validate_state(state, sw + ".result", errors)
        if type(duration) is int and abs(end_previous - duration) > 1e-7:
            errors.append(f"{where}: last shot must end at segment duration")
        if state != expected_exit:
            errors.append(f"{where}: event replay does not produce declared exit")
    return {"errors": errors, "warnings": [], "segments": len(segments)}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--format", choices=("json", "text"), default="text")
    parser.add_argument("--max-shot-seconds", type=float, default=4.0)
    args = parser.parse_args()
    try:
        if not number(args.max_shot_seconds) or args.max_shot_seconds <= 0:
            raise ValueError("max-shot-seconds must be finite and positive")
        result = audit(json.loads(Path(args.path).read_text(encoding="utf-8")), args.max_shot_seconds)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("\n".join(result["errors"]) if result["errors"] else f"PASS: {result['segments']} segments; structured ledger only")
    return 1 if result["errors"] else 0

if __name__ == "__main__":
    raise SystemExit(main())
