#!/usr/bin/env python3
"""Audit adjacent segment entry/exit state and prop handoffs.

Input is a JSON object with a ``segments`` list. Each segment may contain
``entry`` and ``exit`` objects with ``characters`` and ``props`` mappings.
Use ``first_action_changes`` for state paths intentionally changed by the
next segment's first visible action, and ``transitions`` for prop handoffs.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


CHARACTER_FIELDS = (
    "position",
    "depth",
    "posture",
    "body_direction",
    "face_direction",
    "eyeline",
    "left_hand",
    "right_hand",
)

PROP_FIELDS = (
    "holder",
    "hand",
    "location",
    "orientation",
    "functional_state",
)


def load(path: str) -> list[dict]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    segments = data if isinstance(data, list) else data.get("segments")
    if not isinstance(segments, list):
        raise ValueError("JSON must be a list or an object containing a segments list")
    if not all(isinstance(item, dict) for item in segments):
        raise ValueError("every segment must be an object")
    return segments


def changed_paths(segment: dict) -> set[str]:
    values = segment.get("first_action_changes", [])
    return {str(item) for item in values} if isinstance(values, list) else set()


def prop_transition(segment: dict, prop_id: str, field: str,
                    before: object, after: object) -> bool:
    transitions = segment.get("transitions", [])
    if not isinstance(transitions, list):
        return False
    for item in transitions:
        if not isinstance(item, dict) or str(item.get("prop_id")) != prop_id:
            continue
        if not str(item.get("shot", "")).strip():
            continue
        if field == "holder":
            return item.get("from") == before and item.get("to") == after
        if field == "hand":
            if "from_hand" in item or "to_hand" in item:
                return item.get("from_hand") == before and item.get("to_hand") == after
            return item.get("from") is not None and item.get("to") is not None
    return False


def compare_mapping(previous: dict, current: dict, fields: tuple[str, ...],
                    prefix: str, allowed: set[str], errors: list[str],
                    segment_id: object, segment: dict,
                    prop_mode: bool = False) -> None:
    if not isinstance(previous, dict) or not isinstance(current, dict):
        errors.append(f"第{segment_id}段{prefix}状态必须为对象")
        return
    for asset_id in sorted(set(previous) & set(current)):
        before = previous.get(asset_id) or {}
        after = current.get(asset_id) or {}
        if not isinstance(before, dict) or not isinstance(after, dict):
            errors.append(f"第{segment_id}段{prefix}.{asset_id}状态必须为对象")
            continue
        for field in fields:
            if field not in before or field not in after or before[field] == after[field]:
                continue
            path = f"{prefix}.{asset_id}.{field}"
            if path in allowed:
                continue
            if prop_mode and field in ("holder", "hand") and prop_transition(
                segment, asset_id, field, before[field], after[field]
            ):
                continue
            errors.append(
                f"第{segment_id}段进入状态不承接：{path} "
                f"{before[field]!r}→{after[field]!r}；需首动作变化或交接镜"
            )


def audit(segments: list[dict]) -> dict:
    errors, warnings = [], []
    if not segments:
        return {"errors": ["没有分段"], "warnings": [], "stats": {"segment_count": 0}}
    previous_id = None
    for index, segment in enumerate(segments, 1):
        sid = segment.get("id", index)
        if previous_id is not None and isinstance(previous_id, int) and isinstance(sid, int) and sid != previous_id + 1:
            errors.append(f"段号不连续：{previous_id}→{sid}")
        previous_id = sid
        if index == 1:
            continue
        previous = segments[index - 2]
        previous_exit = previous.get("exit", {})
        current_entry = segment.get("entry", {})
        if not isinstance(previous_exit, dict) or not isinstance(current_entry, dict):
            errors.append(f"第{sid}段缺少可审查的entry或上一段exit对象")
            continue
        allowed = changed_paths(segment)
        compare_mapping(
            previous_exit.get("characters", {}),
            current_entry.get("characters", {}),
            CHARACTER_FIELDS,
            "characters",
            allowed,
            errors,
            sid,
            segment,
        )
        compare_mapping(
            previous_exit.get("props", {}),
            current_entry.get("props", {}),
            PROP_FIELDS,
            "props",
            allowed,
            errors,
            sid,
            segment,
            prop_mode=True,
        )
        previous_props_data = previous_exit.get("props") or {}
        current_props_data = current_entry.get("props") or {}
        previous_props = set(previous_props_data.keys()) if isinstance(previous_props_data, dict) else set()
        current_props = set(current_props_data.keys()) if isinstance(current_props_data, dict) else set()
        disappeared = sorted(previous_props - current_props)
        if disappeared:
            warnings.append(f"第{sid}段进入状态未列上一段道具：{'、'.join(disappeared)}")
    return {
        "errors": errors,
        "warnings": warnings,
        "stats": {"segment_count": len(segments), "transition_count": max(0, len(segments) - 1)},
    }


def render(result: dict, fmt: str) -> str:
    if fmt == "json":
        return json.dumps(result, ensure_ascii=False, indent=2)
    stats = result["stats"]
    if fmt == "markdown":
        lines = [
            "## 连续性审查",
            "",
            f"- 分段数：{stats['segment_count']}",
            f"- 相邻交接：{stats.get('transition_count', 0)}",
        ]
        error_prefix, warning_prefix = "- ERROR：", "- WARN："
    else:
        lines = [f"分段数：{stats['segment_count']}；相邻交接：{stats.get('transition_count', 0)}"]
        error_prefix, warning_prefix = "ERROR: ", "WARN: "
    lines.extend(error_prefix + item for item in result["errors"])
    lines.extend(warning_prefix + item for item in result["warnings"])
    if not result["errors"] and not result["warnings"]:
        lines.append("PASS：人物与道具跨段状态连续。")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--format", choices=("text", "markdown", "json"), default="text")
    args = parser.parse_args()
    try:
        result = audit(load(args.path))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(render(result, args.format))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
