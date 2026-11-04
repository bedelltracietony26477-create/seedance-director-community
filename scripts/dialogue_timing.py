#!/usr/bin/env python3
"""Estimate V1.6 Chinese dialogue, pauses, action overlap, and segment mode."""
from __future__ import annotations
import argparse, json, re, sys

MODES = {
    "urgent": {"cps": (4.4, 4.8), "planning_cps": 4.6, "pause": .75, "pre": (.10,.30), "post": (.20,.50)},
    "neutral": {"cps": (4.0, 4.5), "planning_cps": 4.2, "pause": 1.0, "pre": (.15,.30), "post": (.40,.80)},
    "authoritative": {"cps": (4.0, 4.5), "planning_cps": 4.2, "pause": 1.1, "pre": (.20,.45), "post": (.40,.90)},
    "restrained": {"cps": (4.0, 4.5), "planning_cps": 4.2, "pause": 1.25, "pre": (.30,.60), "post": (.50,1.20)},
    "shock": {"cps": (4.0, 4.5), "planning_cps": 4.2, "pause": 1.30, "pre": (.50,1.00), "post": (.70,1.20)},
    "slow": {"cps": (3.4, 3.8), "planning_cps": 3.6, "pause": 1.25, "pre": (.30,.60), "post": (.50,1.20)},
}
PAUSES={"、":(.10,.20),"，":(.15,.30),",":(.15,.30),"；":(.25,.45),";":(.25,.45),"：":(.25,.45),"。":(.30,.60),".":(.30,.60),"！":(.25,.60),"!":(.25,.60),"？":(.25,.60),"?":(.25,.60),"—":(.20,.40)}

def strip_speaker(text:str)->str:
    return re.sub(r"^\s*[^\s：:，,。！？!?]{1,16}\s*[：:]\s*","",text.strip())

def spoken_units(text:str)->int:
    body=strip_speaker(text)
    return len(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]",body))+len(re.findall(r"\d",body))+len(re.findall(r"[A-Za-z]+",body))

def punctuation_pause(text:str)->tuple[float,float]:
    working=strip_speaker(text); low=high=0.0
    for token in ("……","..."):
        c=working.count(token); low+=c*.60; high+=c*1.20; working=working.replace(token,"")
    for mark,(lo,hi) in PAUSES.items():
        c=working.count(mark); low+=c*lo; high+=c*hi
    return low,high

def estimate(text,mode,pre,post,reset,action,overlap,segment_mode):
    prof=MODES[mode]; units=spoken_units(text); body=strip_speaker(text)
    slow,fast=prof["cps"]; pcps=prof["planning_cps"]
    speech=(units/fast if units else 0.0, units/slow if units else 0.0); speech_plan=units/pcps if units else 0.0
    plo,phi=punctuation_pause(text); plo*=prof["pause"]; phi*=prof["pause"]
    pre_r=(pre,pre) if pre is not None else prof["pre"]; post_r=(post,post) if post is not None else prof["post"]
    extra=max(0,reset)+max(0,action)-max(0,overlap)
    total_lo=max(0,speech[0]+plo+pre_r[0]+post_r[0]+extra); total_hi=max(total_lo,speech[1]+phi+pre_r[1]+post_r[1]+extra)
    plan=max(0,speech_plan+(plo+phi)/2+sum(pre_r)/2+sum(post_r)/2+extra)
    recommended="extended" if plan>15.0 else "standard"
    selected=recommended if segment_mode=="auto" else segment_mode
    warning=None
    if selected=="standard" and plan>15.0: warning="规划总时长超过15秒；建议拆段或授权Extended Mode。"
    if selected=="extended" and plan<=15.0: warning="当前容量可落入Standard Mode；仅在连续表演/空间动作有明确理由时保留Extended。"
    return {"original_text":text,"spoken_text":body,"mode":mode,"segment_mode":selected,"recommended_segment_mode":recommended,
            "spoken_units":units,"cps_range":[slow,fast],"planning_cps":pcps,
            "speech_seconds":[round(speech[0],2),round(speech[1],2)],"planning_speech_seconds":round(speech_plan,2),
            "punctuation_pause_seconds":[round(plo,2),round(phi,2)],"pre_line_seconds":[round(pre_r[0],2),round(pre_r[1],2)],
            "post_line_reaction_seconds":[round(post_r[0],2),round(post_r[1],2)],"reset_seconds":round(reset,2),
            "nonverbal_action_seconds":round(action,2),"overlap_seconds":round(overlap,2),
            "performance_total_seconds":[round(total_lo,2),round(total_hi,2)],"planning_total_seconds":round(plan,2),"warning":warning}

def render_markdown(r):
    rows=[("台词",r['spoken_text']),("模式",r['mode']),("分段模式",r['segment_mode']),("推荐分段模式",r['recommended_segment_mode']),
          ("有效字数",r['spoken_units']),("稳定规划语速",f"{r['planning_cps']}字/秒"),("稳定规划纯说话",f"{r['planning_speech_seconds']:.2f}秒"),
          ("含气口、动作与反应",f"{r['performance_total_seconds'][0]:.2f}–{r['performance_total_seconds'][1]:.2f}秒"),("稳定规划总时长",f"{r['planning_total_seconds']:.2f}秒")]
    out=["| 项目 | 结果 |","|---|---|"]+[f"| {a} | {b} |" for a,b in rows]
    if r['warning']: out.append(f"\n- WARN：{r['warning']}")
    return "\n".join(out)

def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--text'); ap.add_argument('--mode',choices=sorted(MODES),default='neutral')
    ap.add_argument('--segment-mode',choices=('auto','standard','extended'),default='auto')
    ap.add_argument('--pre',type=float); ap.add_argument('--post',type=float); ap.add_argument('--reset',type=float,default=0.0); ap.add_argument('--action',type=float,default=0.0); ap.add_argument('--overlap',type=float,default=0.0)
    ap.add_argument('--format',choices=('text','markdown','json'),default='text'); a=ap.parse_args(); text=a.text if a.text is not None else sys.stdin.read().strip()
    if not text: ap.error('dialogue text is required via --text or stdin')
    r=estimate(text,a.mode,a.pre,a.post,a.reset,a.action,a.overlap,a.segment_mode)
    if a.format=='json': print(json.dumps(r,ensure_ascii=False,indent=2))
    elif a.format=='markdown': print(render_markdown(r))
    else:
        print(f"台词：{r['spoken_text']}"); print(f"稳定规划总时长：{r['planning_total_seconds']:.2f}秒；模式：{r['segment_mode']}")
        if r['warning']: print('WARN:',r['warning'])
    return 0
if __name__=='__main__': raise SystemExit(main())
