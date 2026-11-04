#!/usr/bin/env python3
"""Audit Pro V1.6 segmentation: Standard/Extended timing, coverage, impact and density."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path

def load(path):
    data=json.loads(Path(path).read_text(encoding='utf-8'))
    if isinstance(data,list): return {'segments':data}
    if not isinstance(data,dict) or not isinstance(data.get('segments'),list): raise ValueError('JSON must be a list or an object containing a segments list')
    return data

def expected_shots(d):
    if d<=10:return (3,5)
    if d<=12:return (4,7)
    if d<=15:return (5,8)
    return (5,16)

def audit(data):
    errors=[]; warnings=[]; segs=data['segments']; durations=[]; source_ids=set(); assigned=[]; nodes=[]; prev=None
    if not segs:return {'errors':['没有分段'],'warnings':[],'stats':{}}
    for idx,seg in enumerate(segs,1):
        sid=seg.get('id',idx); d=float(seg.get('duration',0)); durations.append(d)
        if prev is not None and isinstance(prev,int) and isinstance(sid,int) and sid!=prev+1: errors.append(f'段号不连续：{prev}→{sid}')
        prev=sid
        mode=str(seg.get('segment_mode','standard')).lower(); reason=str(seg.get('extended_reason','')).strip()
        if d>30: errors.append(f'第{sid}段超过30秒：{d:g}秒；默认必须拆段')
        elif d>15 and mode!='extended': errors.append(f'第{sid}段{d:g}秒但未声明Extended Mode')
        elif d>15 and not reason: warnings.append(f'第{sid}段为Extended Mode但缺少extended_reason')
        elif d<8 and not str(seg.get('short_reason','')).strip(): errors.append(f'第{sid}段低于8秒且无理由：{d:g}秒')
        dialogue=float(seg.get('dialogue_seconds',0)); pauses=float(seg.get('pause_reaction_seconds',0)); action=float(seg.get('action_seconds',0)); overlap=float(seg.get('overlap_seconds',0))
        required=max(0,dialogue+pauses+action-overlap)
        if required>d+.05: errors.append(f'第{sid}段容量超载：需要{required:.2f}秒，只有{d:.2f}秒')
        shots=int(seg.get('shots',0))
        if shots:
            lo,hi=expected_shots(d)
            if shots<lo or shots>hi:warnings.append(f'第{sid}段{d:g}秒配置{shots}镜，常见可读范围{lo}–{hi}镜')
        if seg.get('source_id'): source_ids.add(str(seg['source_id']))
        if isinstance(seg.get('dialogue_ids'),list): assigned+=list(map(str,seg['dialogue_ids']))
        if isinstance(seg.get('narrative_node_ids'),list): nodes+=list(map(str,seg['narrative_node_ids']))
        hook=seg.get('hook_seconds')
        if hook is None:warnings.append(f'第{sid}段缺少hook_seconds')
        elif float(hook)>1.5:warnings.append(f'第{sid}段钩子到{float(hook):.1f}秒才成立')
        impact=seg.get('impact_shots')
        if impact is None:warnings.append(f'第{sid}段缺少impact_shots')
        elif int(impact)!=1:warnings.append(f'第{sid}段核心冲击镜头为{int(impact)}个，建议唯一')
        axes=seg.get('contrast_axes')
        if not isinstance(axes,list) or len({str(x) for x in axes if str(x).strip()})<2:warnings.append(f'第{sid}段少于两种有效对比轴')
        stasis=seg.get('max_visual_stasis_seconds')
        if stasis is None:warnings.append(f'第{sid}段缺少max_visual_stasis_seconds')
        elif float(stasis)>3 and not str(seg.get('visual_stasis_reason','')).strip():warnings.append(f'第{sid}段最长视觉静止{float(stasis):.1f}秒且无理由')
        if d>15:
            strat=seg.get('max_strategy_stasis_seconds')
            if strat is None:warnings.append(f'第{sid}段Extended缺少max_strategy_stasis_seconds')
            elif float(strat)>6 and not str(seg.get('strategy_stasis_reason','')).strip():warnings.append(f'第{sid}段策略/空间/信息静止{float(strat):.1f}秒，超过Extended建议')
        if not str(seg.get('end_hook','')).strip():warnings.append(f'第{sid}段缺少结尾钩子')
    exp=set(map(str,data.get('expected_source_ids',[]))); miss=sorted(exp-source_ids)
    if miss:errors.append('遗漏来源场次：'+'、'.join(miss))
    expd=list(map(str,data.get('expected_dialogue_ids',[]))); miss=[x for x in expd if x not in assigned]; dup=sorted({x for x in assigned if assigned.count(x)>1})
    if miss:errors.append('遗漏台词ID：'+'、'.join(miss))
    if dup:errors.append('重复分配台词ID：'+'、'.join(dup))
    expn=list(map(str,data.get('expected_narrative_node_ids',[]))); miss=[x for x in expn if x not in nodes]; dup=sorted({x for x in nodes if nodes.count(x)>1})
    if miss:errors.append('遗漏叙事节点ID：'+'、'.join(miss))
    if dup:errors.append('重复分配叙事节点ID：'+'、'.join(dup))
    std=sum(1 for d in durations if 8<=d<=15); ext=sum(1 for d in durations if 15<d<=30)
    stats={'segment_count':len(segs),'total_seconds':round(sum(durations),2),'standard_count':std,'extended_count':ext,'narrative_node_count':len(nodes)}
    return {'errors':errors,'warnings':warnings,'stats':stats}

def render(r,fmt):
    if fmt=='json':return json.dumps(r,ensure_ascii=False,indent=2)
    s=r['stats']; lines=[f"分段数：{s.get('segment_count',0)}；总时长：{s.get('total_seconds',0)}秒；Standard：{s.get('standard_count',0)}；Extended：{s.get('extended_count',0)}"]
    if fmt=='markdown': lines=['## 分段审查','',f"- 分段数：{s.get('segment_count',0)}",f"- 总时长：{s.get('total_seconds',0)}秒",f"- Standard：{s.get('standard_count',0)}",f"- Extended：{s.get('extended_count',0)}"]
    lines += [(' - ERROR：' if fmt=='markdown' else 'ERROR: ')+x for x in r['errors']]
    lines += [(' - WARN：' if fmt=='markdown' else 'WARN: ')+x for x in r['warnings']]
    if not r['errors'] and not r['warnings']:lines.append('PASS：V1.6时长、容量、冲击与密度检查通过。')
    return '\n'.join(lines)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('path');ap.add_argument('--format',choices=('text','markdown','json'),default='text');a=ap.parse_args()
    try:r=audit(load(a.path))
    except (OSError,ValueError,json.JSONDecodeError) as e:print('ERROR:',e,file=sys.stderr);return 2
    print(render(r,a.format));return 1 if r['errors'] else 0
if __name__=='__main__':raise SystemExit(main())
