#!/usr/bin/env python3
"""Audit Community V1.5.5 segmentation for timing, coverage, and model-aware duration profiles."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

MODEL_ALIASES = {
    "2.0": "seedance2.0",
    "seedance2": "seedance2.0",
    "seedance2.0": "seedance2.0",
    "seedance-2.0": "seedance2.0",
    "2.5": "seedance2.5",
    "seedance2.5": "seedance2.5",
    "seedance-2.5": "seedance2.5",
}


def load(path: str) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, list):
        return {"segments": data}
    if not isinstance(data, dict) or not isinstance(data.get("segments"), list):
        raise ValueError("JSON must be a list or an object containing a segments list")
    return data


def normalize_model(value: str | None) -> str:
    key = str(value or "seedance2.0").strip().lower().replace(" ", "")
    if key not in MODEL_ALIASES:
        raise ValueError(f"unsupported model profile: {value!r}; use seedance2.0 or seedance2.5")
    return MODEL_ALIASES[key]


def expected_shots(duration: float, model: str) -> tuple[int, int]:
    if model == "seedance2.5":
        if duration <= 20:
            return 5, 9
        if duration <= 25:
            return 6, 10
        return 7, 12
    if duration <= 10:
        return 3, 5
    if duration <= 12:
        return 4, 7
    return 5, 8


def audit(data: dict, model_override: str | None = None) -> dict:
    errors, warnings = [], []
    model = normalize_model(model_override or data.get("model"))
    segments = data["segments"]
    if not segments:
        errors.append("没有分段")
        return {"errors": errors, "warnings": warnings, "stats": {"model": model}}

    durations, source_ids, assigned = [], set(), []
    narrative_nodes = []
    previous_id = None

    for index, seg in enumerate(segments, 1):
        sid = seg.get("id", index)
        duration = float(seg.get("duration", 0))
        durations.append(duration)

        if previous_id is not None and isinstance(sid, int) and isinstance(previous_id, int) and sid != previous_id + 1:
            errors.append(f"段号不连续：{previous_id}→{sid}")
        previous_id = sid

        if model == "seedance2.0":
            if duration > 15:
                errors.append(f"第{sid}段超过Seedance 2.0上限15秒：{duration:g}秒")
            elif duration < 8:
                reason = str(seg.get("short_reason", "")).strip()
                if not reason:
                    errors.append(f"第{sid}段低于Seedance 2.0标准8秒且无理由：{duration:g}秒")
                else:
                    warnings.append(f"第{sid}段为2.0短段：{duration:g}秒；理由：{reason}")
        else:
            if duration > 30:
                errors.append(f"第{sid}段超过Seedance 2.5上限30秒：{duration:g}秒")
            elif duration < 15:
                errors.append(f"第{sid}段低于Seedance 2.5开放范围15秒：{duration:g}秒")
            elif duration < 16:
                reason = str(seg.get("boundary_reason", seg.get("short_reason", ""))).strip()
                if not reason:
                    warnings.append(f"第{sid}段为15秒边界段；建议提供boundary_reason或改为16–30秒标准段")
                else:
                    warnings.append(f"第{sid}段为2.5边界段：{duration:g}秒；理由：{reason}")

        dialogue = float(seg.get("dialogue_seconds", 0))
        pauses = float(seg.get("pause_reaction_seconds", 0))
        action = float(seg.get("action_seconds", 0))
        overlap = float(seg.get("overlap_seconds", 0))
        required = max(0.0, dialogue + pauses + action - overlap)
        if required > duration + 0.05:
            errors.append(f"第{sid}段容量超载：需要{required:.2f}秒，只有{duration:.2f}秒")

        shots = int(seg.get("shots", 0))
        if shots:
            lo, hi = expected_shots(duration, model)
            if shots < lo or shots > hi:
                warnings.append(f"第{sid}段{duration:g}秒配置{shots}镜，{model}建议{lo}–{hi}镜")

        max_actions = seg.get("max_actions_in_one_second")
        if isinstance(max_actions, (int, float)) and max_actions > 2:
            warnings.append(f"第{sid}段存在每秒{max_actions:g}个主要动作，可能过载")

        if seg.get("source_id"):
            source_ids.add(str(seg["source_id"]))
        if isinstance(seg.get("dialogue_ids"), list):
            assigned.extend(map(str, seg["dialogue_ids"]))
        if isinstance(seg.get("narrative_node_ids"), list):
            narrative_nodes.extend(map(str, seg["narrative_node_ids"]))

        hook_seconds = seg.get("hook_seconds")
        if hook_seconds is None:
            warnings.append(f"第{sid}段缺少hook_seconds，无法审查前1.5秒钩子")
        elif float(hook_seconds) > 1.5:
            warnings.append(f"第{sid}段钩子到{float(hook_seconds):.1f}秒才成立，建议压到前1.5秒")

        impact_shots = seg.get("impact_shots")
        if impact_shots is None:
            warnings.append(f"第{sid}段缺少impact_shots，无法审查核心冲击镜头")
        elif int(impact_shots) != 1:
            warnings.append(f"第{sid}段核心冲击镜头为{int(impact_shots)}个，建议保持唯一主爆点")

        contrast_axes = seg.get("contrast_axes")
        if not isinstance(contrast_axes, list) or len({str(x) for x in contrast_axes if str(x).strip()}) < 2:
            warnings.append(f"第{sid}段少于两种有效对比轴")

        visual_stasis = seg.get("max_visual_stasis_seconds")
        stasis_limit = 4.0 if model == "seedance2.5" else 3.0
        if visual_stasis is None:
            warnings.append(f"第{sid}段缺少max_visual_stasis_seconds，无法审查视觉变化密度")
        elif float(visual_stasis) > stasis_limit and not str(seg.get("visual_stasis_reason", "")).strip():
            warnings.append(
                f"第{sid}段最长视觉静止{float(visual_stasis):.1f}秒且无情绪/动作理由；{model}建议不超过{stasis_limit:g}秒"
            )

        if model == "seedance2.5" and duration >= 20:
            microbeats = seg.get("microbeats")
            if not isinstance(microbeats, list) or not 2 <= len(microbeats) <= 4:
                warnings.append(f"第{sid}段为{duration:g}秒长段，建议提供2–4个microbeats以证明内部推进")

        if not str(seg.get("end_hook", "")).strip():
            warnings.append(f"第{sid}段缺少结尾钩子")

    expected_sources = set(map(str, data.get("expected_source_ids", [])))
    missing_sources = sorted(expected_sources - source_ids)
    if missing_sources:
        errors.append("遗漏来源场次：" + "、".join(missing_sources))

    expected_dialogue = list(map(str, data.get("expected_dialogue_ids", [])))
    missing_dialogue = [item for item in expected_dialogue if item not in assigned]
    duplicates = sorted({item for item in assigned if assigned.count(item) > 1})
    if missing_dialogue:
        errors.append("遗漏台词ID：" + "、".join(missing_dialogue))
    if duplicates:
        errors.append("重复分配台词ID：" + "、".join(duplicates))

    expected_nodes = list(map(str, data.get("expected_narrative_node_ids", [])))
    missing_nodes = [item for item in expected_nodes if item not in narrative_nodes]
    duplicate_nodes = sorted({item for item in narrative_nodes if narrative_nodes.count(item) > 1})
    if missing_nodes:
        errors.append("遗漏叙事节点ID：" + "、".join(missing_nodes))
    if duplicate_nodes:
        errors.append("重复分配叙事节点ID：" + "、".join(duplicate_nodes))

    if model == "seedance2.0":
        preferred = sum(1 for d in durations if 13 <= d <= 15)
        regular = sum(1 for d in durations if 8 <= d <= 15)
        preferred_label = "13–15秒分段占比"
        preferred_ratio = preferred / len(durations)
        if preferred_ratio < 0.5:
            warnings.append(f"13–15秒分段占比仅{preferred_ratio:.0%}；检查是否能在戏剧上自然合并")
    else:
        preferred = sum(1 for d in durations if 16 <= d <= 30)
        regular = sum(1 for d in durations if 15 <= d <= 30)
        preferred_label = "16–30秒标准段占比"
        preferred_ratio = preferred / len(durations)
        if preferred_ratio < 0.75:
            warnings.append(f"16–30秒标准段占比仅{preferred_ratio:.0%}；检查15秒边界段是否使用过多")

    stats = {
        "model": model,
        "segment_count": len(segments),
        "total_seconds": round(sum(durations), 2),
        "regular_count": regular,
        "preferred_count": preferred,
        "preferred_ratio": round(preferred_ratio, 4),
        "preferred_label": preferred_label,
        "narrative_node_count": len(narrative_nodes),
    }
    return {"errors": errors, "warnings": warnings, "stats": stats}


def markdown(result: dict) -> str:
    stats = result["stats"]
    lines = ["## 分段审查", "", "| 指标 | 结果 |", "|---|---:|"]
    if stats:
        lines.extend([
            f"| 模型档 | {stats.get('model', '-')} |",
            f"| 分段数 | {stats.get('segment_count', 0)} |",
            f"| 素材总时长 | {stats.get('total_seconds', 0):.2f}秒 |",
            f"| 有效时长范围分段 | {stats.get('regular_count', 0)} |",
            f"| {stats.get('preferred_label', '标准段占比')} | {stats.get('preferred_ratio', 0):.0%} |",
        ])
    lines.append("")
    for item in result["errors"]:
        lines.append(f"- ERROR：{item}")
    for item in result["warnings"]:
        lines.append(f"- WARN：{item}")
    if not result["errors"] and not result["warnings"]:
        lines.append("- PASS：模型时长、容量、镜头量与覆盖检查通过。")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--model", choices=("seedance2.0", "seedance2.5", "2.0", "2.5"))
    parser.add_argument("--format", choices=("text", "markdown", "json"), default="text")
    args = parser.parse_args()
    try:
        result = audit(load(args.path), args.model)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(markdown(result))
    else:
        stats = result["stats"]
        print(f"模型档：{stats.get('model', '-')}; 分段数：{stats.get('segment_count', 0)}；总时长：{stats.get('total_seconds', 0)}秒")
        for item in result["errors"]:
            print(f"ERROR: {item}")
        for item in result["warnings"]:
            print(f"WARN: {item}")
        if not result["errors"] and not result["warnings"]:
            print("PASS: 模型时长、容量、镜头量与覆盖检查通过")
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
