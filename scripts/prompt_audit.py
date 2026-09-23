#!/usr/bin/env python3
"""Audit Community V1.5.5 full or quick Seedance prompts and optional dialogue."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


FULL_MODULES = [
    "[声画硬锁]",
    "[参考图 / 音频对应表]",
    "[本段任务]",
    "[人物状态、站位、轴线与群像]",
    "[风格、光影与氛围]",
    "[镜头时间轴]",
    "[声音与剪辑]",
    "[连续性底线]",
]

QUICK_MODULES = [
    "[STYLELOCK]",
    "[REFERENCE]",
    "[SHOT]",
    "[BEATS]",
]

FORBIDDEN = ("风险等级", "生成风险", "执行策略", "稳定备选", "[关键帧]", "模仿导演", "导演风格")
COMPLEX = ("Technocrane", "环绕", "Whip Pan", "鞭甩", "Dolly Zoom", "眩晕变焦", "Crash Zoom", "快速变焦", "Crane", "Jib")
VISUAL_PROGRESS = ("L-cut", "反应", "推进", "横移", "焦点", "切", "走位", "动作", "道具", "景别")


def section(text: str, heading: str, modules: list[str]) -> str:
    start = text.find(heading)
    if start < 0:
        return ""
    start += len(heading)
    candidates = [text.find(item, start) for item in modules if text.find(item, start) >= 0]
    end = min(candidates) if candidates else len(text)
    return text[start:end].strip()


def load_dialogues(path: str | None) -> list[str]:
    if not path:
        return []
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, list):
        return [str(x["text"] if isinstance(x, dict) else x) for x in data]
    if isinstance(data, dict):
        items = data.get("dialogues", [])
        return [str(x["text"] if isinstance(x, dict) else x) for x in items]
    raise ValueError("dialogue JSON must be a list or contain dialogues")


def extract_dialogues(text: str) -> list[str]:
    return [item.strip() for item in re.findall(r"\{([^{}]+)\}", text, flags=re.S)]


def shot_blocks(shot_text: str) -> list[str]:
    marks = list(re.finditer(r"(?m)^镜头\s*\d+[^\n]*", shot_text))
    blocks = []
    for i, mark in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(shot_text)
        blocks.append(shot_text[mark.start():end].strip())
    return blocks


def shot_timecode(heading: str) -> tuple[float, float] | None:
    match = re.search(r"(\d+(?:\.\d+)?)\s*[—–-]\s*(\d+(?:\.\d+)?)\s*秒", heading)
    if not match:
        return None
    return float(match.group(1)), float(match.group(2))


def tenth_aligned(value: float) -> bool:
    return abs(value * 10 - round(value * 10)) < 1e-7


def sequential_reference_errors(mapping: str) -> list[str]:
    errors = []
    for label, pattern in (("图片", r"(?:@\[图片|@图)(\d+)\]?"), ("音频", r"(?:@\[音频|@音频)(\d+)\]?")):
        values = [int(item) for item in re.findall(pattern, mapping)]
        if not values:
            continue
        if len(values) != len(set(values)):
            errors.append(f"{label}执行编号重复")
        unique = list(dict.fromkeys(values))
        if unique != list(range(1, len(unique) + 1)):
            errors.append(f"{label}执行编号必须从1开始并按映射顺序连续：当前为{unique}")
    return errors


def audit(text: str, expected_dialogues: list[str], contract: str = "auto") -> dict:
    errors, warnings = [], []
    if contract == "auto":
        contract = "full" if any(item in text for item in FULL_MODULES[2:]) else "quick"
    modules = FULL_MODULES if contract == "full" else QUICK_MODULES
    positions = []
    for module in modules:
        pos = text.find(module)
        if pos < 0:
            errors.append(f"缺少模块：{module}")
        positions.append(pos)
    present = [p for p in positions if p >= 0]
    if present != sorted(present):
        errors.append(f"{contract}契约模块顺序不正确")
    headings = re.findall(r"(?m)^\[[^\]\n]+\]\s*$", text)
    extras = [h for h in headings if h not in modules]
    if extras:
        errors.append("存在额外模块：" + "、".join(extras))
    for term in FORBIDDEN:
        if term in text:
            errors.append(f"包含禁用内容：{term}")

    hard = section(text, modules[0], modules) if contract == "full" else text
    if "无字幕" not in hard:
        errors.append("缺少“无字幕”硬锁")
    if "无背景音乐" not in hard:
        errors.append("缺少“无背景音乐”硬锁")
    if "<>" not in hard and "<" not in text:
        warnings.append("未发现音效<>规范或实际音效")
    if "{}" not in hard and "{" not in text:
        warnings.append("未发现台词{}规范或实际台词")

    mapping_heading = FULL_MODULES[1] if contract == "full" else QUICK_MODULES[1]
    mapping = section(text, mapping_heading, modules)
    mapping_lines = [line.strip() for line in mapping.splitlines() if line.strip()]
    for line in mapping_lines:
        if "=" in line and not any(token in line for token in ("@[图片", "@[音频", "@图", "@音频")):
            warnings.append(f"映射行可能缺少@素材：{line[:40]}")
    errors.extend(sequential_reference_errors(mapping))

    def refs(blob: str) -> set[str]:
        found = set()
        for label, pattern in (("图片", r"(?:@\[图片|@图)(\d+)\]?"), ("音频", r"(?:@\[音频|@音频)(\d+)\]?")):
            for number in re.findall(pattern, blob):
                found.add(f"{label}{int(number)}")
        return found

    declared_refs = refs(mapping)

    if contract == "quick":
        style = section(text, QUICK_MODULES[0], modules)
        shot_text = section(text, QUICK_MODULES[2], modules)
        beats = section(text, QUICK_MODULES[3], modules)
        task = ""
        blocking = shot_text + "\n" + beats
        shots_section = shot_text
        sound = beats
        continuity = beats
    else:
        task = section(text, FULL_MODULES[2], modules)
        blocking = section(text, FULL_MODULES[3], modules)
        style = section(text, FULL_MODULES[4], modules)
        shots_section = section(text, FULL_MODULES[5], modules)
        sound = section(text, FULL_MODULES[6], modules)
        continuity = section(text, FULL_MODULES[7], modules)

    if contract == "full":
        if not re.search(r"\d+(?:\.\d+)?\s*秒", task):
            warnings.append("[本段任务]可能缺少时长核算")
        for token in ("情绪", "视点", "钩子", "气口"):
            if token not in task:
                warnings.append(f"[本段任务]可能缺少：{token}")
        for token in ("核心冲击", "对比轴", "视觉变化"):
            if token not in task:
                errors.append(f"[本段任务]缺少V1.5.5字段：{token}")
        if "1.5秒" not in task and "前1.5秒" not in task:
            warnings.append("[本段任务]未明确前1.5秒钩子")

    for group, options in {
        "左右关系": ("画面左", "画面右", "左侧", "右侧"),
        "朝向": ("朝向", "面向", "背对"),
        "眼神": ("眼神", "视线", "看向"),
        "轴线": ("轴线", "180度"),
        "行动落点": ("路径", "落点", "停在"),
    }.items():
        if not any(item in blocking for item in options):
            warnings.append(f"站位模块可能缺少{group}")

    if not any(x in style for x in ("主光", "光源", "日光", "侧光", "逆光", "顶光", "lighting", "light source", "daylight")):
        warnings.append("风格模块可能缺少主光来源/方向")
    if not any(x in style for x in ("冷", "暖", "色温", "白平衡", "主色", "warm", "cool", "color", "colour")):
        warnings.append("风格模块可能缺少冷暖或色彩逻辑")

    shot_refs = refs(shots_section)
    undeclared = sorted(shot_refs - declared_refs)
    unused = sorted(declared_refs - shot_refs)
    if undeclared:
        errors.append("镜头正文调用了未在参考表声明的素材：" + "、".join(undeclared))
    if unused:
        warnings.append("参考表存在未在镜头时间轴调用的素材：" + "、".join(unused))

    shots = shot_blocks(shots_section)
    if not shots:
        errors.append("[镜头时间轴]没有可识别镜头")
    timecodes = []
    impact_count = 0
    for i, block in enumerate(shots, 1):
        heading = block.splitlines()[0]
        timecode = shot_timecode(heading)
        if timecode is None:
            warnings.append(f"镜头{i}缺少起止时间码")
        else:
            start, end = timecode
            timecodes.append((i, start, end))
            if end <= start:
                errors.append(f"镜头{i}结束时间必须晚于开始时间")
            if not tenth_aligned(start) or not tenth_aligned(end):
                errors.append(f"镜头{i}时间码必须按0.1秒规划精度")
        if re.search(r"\bIMPACT\b|核心冲击", heading, re.I):
            impact_count += 1
        if not re.search(r"\b\d{2,3}\s*mm(?![A-Za-z])", block, re.I):
            errors.append(f"镜头{i}缺少焦段")
        if contract == "full" and not re.search(r"\bf\s*/\s*\d+(?:\.\d+)?\b", block, re.I):
            errors.append(f"镜头{i}缺少f/光圈")
        if any(term.lower() in block.lower() for term in COMPLEX):
            needed = ("起点", "触发", "路径", "落点", "焦点")
            missing = [item for item in needed if item not in block]
            if missing:
                errors.append(f"镜头{i}复杂运镜缺少：{'、'.join(missing)}")
            used = {term.lower() for term in COMPLEX if term.lower() in block.lower()}
            if len(used) > 2:
                warnings.append(f"镜头{i}可能堆叠超过一个主要运动和一个增强语法")
        if any(term in block for term in ("抓", "递", "接", "撞", "跳", "落地", "挡", "按灭")):
            if not any(term in block for term in ("接触点", "触地", "掌心", "指尖", "落点")):
                warnings.append(f"镜头{i}可能缺少动作接触点/落点")
        if "{" in block and not any(term in block for term in ("气口", "停顿", "吸气", "吞咽")):
            warnings.append(f"镜头{i}有台词但可能缺少台词前气口")
        if "{" in block and not any(term in block for term in ("听者", "反应", "台词后", "说完后")):
            warnings.append(f"镜头{i}有台词但可能缺少台词后反应")
        for line in extract_dialogues(block):
            if len(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", line)) >= 13:
                if not any(term in block for term in VISUAL_PROGRESS):
                    warnings.append(f"镜头{i}长对白可能缺少内部视觉推进")
        if re.search(r"\bAU\s*\d+\b", block, re.I):
            warnings.append(f"镜头{i}直接输出FACS AU编号，建议转译为可见表演")
        if re.search(r"\d+(?:\.\d+)?\s*毫米", block):
            warnings.append(f"镜头{i}包含毫米级表演参数，检查是否为伪精确")

    if impact_count != 1:
        errors.append(f"核心冲击镜头应为1个，当前识别到{impact_count}个")
    for (prev_i, _, prev_end), (curr_i, curr_start, _) in zip(timecodes, timecodes[1:]):
        if abs(prev_end - curr_start) > 0.05:
            errors.append(f"镜头{prev_i}与镜头{curr_i}时间码不连续：{prev_end:g}→{curr_start:g}")
    if timecodes and abs(timecodes[0][1]) > 0.05:
        warnings.append(f"首镜从{timecodes[0][1]:g}秒开始，通常应从0.0秒开始")
    header_duration = re.search(r"(?m)^#.*?｜\s*(\d+(?:\.\d+)?)\s*秒\s*$", text)
    if header_duration and timecodes:
        expected_duration = float(header_duration.group(1))
        if abs(timecodes[-1][2] - expected_duration) > 0.05:
            errors.append(
                f"末镜结束{timecodes[-1][2]:g}秒，与段落时长{expected_duration:g}秒不一致"
            )

    actual = extract_dialogues(shots_section)
    if expected_dialogues:
        if actual != expected_dialogues:
            errors.append("原台词逐字或顺序不一致")
        counts = Counter(actual)
        duplicates = [item for item, count in counts.items() if count > 1]
        if duplicates:
            errors.append("台词重复出现：" + "｜".join(duplicates))

    if not any(x in sound for x in ("Room tone", "room tone", "底噪", "环境声")):
        warnings.append("声音模块可能缺少空间底噪")
    if not any(x in sound for x in ("J-cut", "L-cut", "声音桥", "硬切", "切点")):
        warnings.append("声音模块可能缺少跨镜或剪辑关系")

    if contract == "full":
        for token in ("道具", "轴线", "落点"):
            if token not in continuity:
                warnings.append(f"连续性底线可能缺少：{token}")
    elif not any(token in continuity for token in ("退出状态", "结束状态", "末帧")):
        warnings.append("[BEATS]可能缺少段末退出状态")

    duplicated_lines = [line for line, count in Counter(
        line.strip() for line in text.splitlines()
        if len(line.strip()) >= 20 and not line.lstrip().startswith("镜头")
    ).items() if count > 1]
    if duplicated_lines:
        warnings.append(f"发现{len(duplicated_lines)}条长句重复，检查模块去重")
    return {"errors": errors, "warnings": warnings, "stats": {"contract": contract, "shots": len(shots), "dialogues": len(actual)}}


def render(result: dict, fmt: str) -> str:
    if fmt == "json":
        return json.dumps(result, ensure_ascii=False, indent=2)
    lines = []
    if fmt == "markdown":
        lines.extend(["## 提示词审查", "", f"- 契约：{result['stats']['contract']}", f"- 镜头数：{result['stats']['shots']}", f"- 台词数：{result['stats']['dialogues']}"])
        prefix_error, prefix_warn = "- ERROR：", "- WARN："
    else:
        lines.append(f"契约：{result['stats']['contract']}；镜头数：{result['stats']['shots']}；台词数：{result['stats']['dialogues']}")
        prefix_error, prefix_warn = "ERROR: ", "WARN: "
    lines.extend(prefix_error + item for item in result["errors"])
    lines.extend(prefix_warn + item for item in result["warnings"])
    if not result["errors"] and not result["warnings"]:
        lines.append("PASS：模块、参考编号、声画、时长、站位、镜头与连续性检查通过。")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Prompt text file")
    parser.add_argument("--contract", choices=("auto", "full", "quick"), default="auto")
    parser.add_argument("--dialogue-json", help="JSON list or {dialogues:[...]} of expected lines")
    parser.add_argument("--format", choices=("text", "markdown", "json"), default="text")
    args = parser.parse_args()
    try:
        text = Path(args.path).read_text(encoding="utf-8")
        expected = load_dialogues(args.dialogue_json)
        result = audit(text, expected, args.contract)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(render(result, args.format))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
