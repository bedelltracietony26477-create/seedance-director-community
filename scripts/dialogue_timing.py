#!/usr/bin/env python3
"""Estimate Chinese dialogue, pause, breath, and reaction duration."""

from __future__ import annotations

import argparse
import json
import re
import sys


MODES = {
    # Emotion changes breath, pause, and reaction timing; it does not silently
    # change speech rate. Use urgent/slow only when the source explicitly marks speed.
    "urgent": {"cps": (4.4, 4.8), "planning_cps": 4.6, "pause": 0.75, "pre": (0.10, 0.30), "post": (0.20, 0.50)},
    "neutral": {"cps": (4.0, 4.5), "planning_cps": 4.2, "pause": 1.00, "pre": (0.15, 0.30), "post": (0.40, 0.80)},
    "authoritative": {"cps": (4.0, 4.5), "planning_cps": 4.2, "pause": 1.10, "pre": (0.20, 0.45), "post": (0.40, 0.90)},
    "restrained": {"cps": (4.0, 4.5), "planning_cps": 4.2, "pause": 1.25, "pre": (0.30, 0.60), "post": (0.50, 1.20)},
    "shock": {"cps": (4.0, 4.5), "planning_cps": 4.2, "pause": 1.30, "pre": (0.50, 1.00), "post": (0.70, 1.20)},
    "slow": {"cps": (3.4, 3.8), "planning_cps": 3.6, "pause": 1.25, "pre": (0.30, 0.60), "post": (0.50, 1.20)},
}

PAUSES = {
    "、": (0.10, 0.20), "，": (0.15, 0.30), ",": (0.15, 0.30),
    "；": (0.25, 0.45), ";": (0.25, 0.45), "：": (0.25, 0.45),
    "。": (0.30, 0.60), ".": (0.30, 0.60), "！": (0.25, 0.60),
    "!": (0.25, 0.60), "？": (0.25, 0.60), "?": (0.25, 0.60),
    "—": (0.20, 0.40),
}


def strip_speaker(text: str) -> str:
    """Strip a likely speaker label only at the beginning of one line."""
    return re.sub(r"^\s*[^\s：:，,。！？!?]{1,16}\s*[：:]\s*", "", text.strip())


def spoken_units(text: str) -> int:
    body = strip_speaker(text)
    chinese = re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", body)
    numerals = re.findall(r"\d", body)
    latin_words = re.findall(r"[A-Za-z]+", body)
    return len(chinese) + len(numerals) + len(latin_words)


def punctuation_pause(text: str) -> tuple[float, float]:
    working = strip_speaker(text)
    low = high = 0.0
    for token in ("……", "..."):
        count = working.count(token)
        if count:
            low += count * 0.60
            high += count * 1.20
            working = working.replace(token, "")
    for mark, (mark_low, mark_high) in PAUSES.items():
        count = working.count(mark)
        low += count * mark_low
        high += count * mark_high
    return low, high


def estimate(text: str, mode: str, pre: float | None, post: float | None,
             reset: float, action: float, overlap: float) -> dict[str, object]:
    profile = MODES[mode]
    body = strip_speaker(text)
    units = spoken_units(text)
    cps_slow, cps_fast = profile["cps"]
    planning_cps = profile["planning_cps"]
    speech_low = units / cps_fast if units else 0.0
    speech_high = units / cps_slow if units else 0.0
    speech_planning = units / planning_cps if units else 0.0
    pause_low, pause_high = punctuation_pause(text)
    pause_low *= profile["pause"]
    pause_high *= profile["pause"]
    pre_range = (pre, pre) if pre is not None else profile["pre"]
    post_range = (post, post) if post is not None else profile["post"]
    extra = max(0.0, reset) + max(0.0, action) - max(0.0, overlap)
    total_low = max(0.0, speech_low + pause_low + pre_range[0] + post_range[0] + extra)
    total_high = max(total_low, speech_high + pause_high + pre_range[1] + post_range[1] + extra)
    planning_total = max(0.0, speech_planning + (pause_low + pause_high) / 2
                         + (pre_range[0] + pre_range[1]) / 2
                         + (post_range[0] + post_range[1]) / 2 + extra)
    return {
        "original_text": text,
        "spoken_text": body,
        "mode": mode,
        "spoken_units": units,
        "cps_range": [cps_slow, cps_fast],
        "planning_cps": planning_cps,
        "speech_seconds": [round(speech_low, 2), round(speech_high, 2)],
        "planning_speech_seconds": round(speech_planning, 2),
        "punctuation_pause_seconds": [round(pause_low, 2), round(pause_high, 2)],
        "pre_line_seconds": [round(pre_range[0], 2), round(pre_range[1], 2)],
        "post_line_reaction_seconds": [round(post_range[0], 2), round(post_range[1], 2)],
        "reset_seconds": round(reset, 2),
        "nonverbal_action_seconds": round(action, 2),
        "overlap_seconds": round(overlap, 2),
        "performance_total_seconds": [round(total_low, 2), round(total_high, 2)],
        "planning_total_seconds": round(planning_total, 2),
    }


def render_markdown(result: dict[str, object]) -> str:
    return "\n".join([
        "| 项目 | 结果 |", "|---|---|",
        f"| 台词 | {result['spoken_text']} |",
        f"| 模式 | {result['mode']} |",
        f"| 有效字数 | {result['spoken_units']} |",
        f"| 语速 | {result['cps_range'][0]}–{result['cps_range'][1]}字/秒 |",
        f"| 稳定规划语速 | {result['planning_cps']}字/秒 |",
        f"| 纯说话 | {result['speech_seconds'][0]:.2f}–{result['speech_seconds'][1]:.2f}秒 |",
        f"| 稳定规划纯说话 | {result['planning_speech_seconds']:.2f}秒 |",
        f"| 标点停顿 | {result['punctuation_pause_seconds'][0]:.2f}–{result['punctuation_pause_seconds'][1]:.2f}秒 |",
        f"| 含气口、动作与反应 | {result['performance_total_seconds'][0]:.2f}–{result['performance_total_seconds'][1]:.2f}秒 |",
        f"| 稳定规划总时长 | {result['planning_total_seconds']:.2f}秒 |",
    ])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Dialogue text; reads stdin when omitted.")
    parser.add_argument("--mode", choices=sorted(MODES), default="neutral")
    parser.add_argument("--pre", type=float, help="Override pre-line pause seconds.")
    parser.add_argument("--post", type=float, help="Override post-line reaction seconds.")
    parser.add_argument("--reset", type=float, default=0.0, help="Swallow/reset seconds.")
    parser.add_argument("--action", type=float, default=0.0, help="Nonverbal action seconds.")
    parser.add_argument("--overlap", type=float, default=0.0, help="Action seconds overlapping speech.")
    parser.add_argument("--format", choices=("text", "markdown", "json"), default="text")
    args = parser.parse_args()
    text = args.text if args.text is not None else sys.stdin.read().strip()
    if not text:
        parser.error("dialogue text is required via --text or stdin")
    result = estimate(text, args.mode, args.pre, args.post, args.reset, args.action, args.overlap)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result))
    else:
        print(f"台词：{result['spoken_text']}")
        print(f"模式：{result['mode']}；有效字数：{result['spoken_units']}")
        print(f"稳定规划语速：{result['planning_cps']:.1f}字/秒")
        print(f"纯说话：{result['speech_seconds'][0]:.2f}–{result['speech_seconds'][1]:.2f}秒")
        print(f"含气口、动作与反应：{result['performance_total_seconds'][0]:.2f}–{result['performance_total_seconds'][1]:.2f}秒")
        print(f"稳定规划总时长：{result['planning_total_seconds']:.2f}秒")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
