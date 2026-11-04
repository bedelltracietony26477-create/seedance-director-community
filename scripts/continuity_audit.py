#!/usr/bin/env python3
"""Audit V1.6 adjacent START/END state, prop semantic state, voice state, and handoffs."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path

CHARACTER_FIELDS=("position","depth","posture","body_direction","face_direction","eyeline","left_hand","right_hand","emotion")
PROP_FIELDS=("holder","hand","contact","relation_mode","position_zone","location","orientation","functional_state","continuity_active")
VOICE_FIELDS=("voice_identity","voice_mode","lip_sync","spatial_filter")

def load(path):
    data=json.loads(Path(path).read_text(encoding='utf-8')); segs=data if isinstance(data,list) else data.get('segments')
    if not isinstance(segs,list) or not all(isinstance(x,dict) for x in segs): raise ValueError('JSON must be a list or object containing a segments list')
    return segs

def changed_paths(seg):
    vals=seg.get('first_action_changes',[]); return {str(x) for x in vals} if isinstance(vals,list) else set()

def transition_allows(seg,asset_id,field,before,after):
    for item in seg.get('transitions',[]) if isinstance(seg.get('transitions',[]),list) else []:
        if not isinstance(item,dict) or str(item.get('prop_id',item.get('asset_id','')))!=asset_id: continue
        if not str(item.get('shot','')).strip(): continue
        if field in ('holder','hand','relation_mode','position_zone','functional_state'):
            fb=item.get('from_'+field,item.get('from')); ta=item.get('to_'+field,item.get('to'))
            if fb==before and ta==after:return True
    return False

def compare(prev,curr,fields,prefix,allowed,errors,sid,seg,prop=False):
    if not isinstance(prev,dict) or not isinstance(curr,dict): errors.append(f'第{sid}段{prefix}状态必须为对象'); return
    for aid in sorted(set(prev)&set(curr)):
        b=prev.get(aid) or {}; a=curr.get(aid) or {}
        if not isinstance(b,dict) or not isinstance(a,dict):errors.append(f'第{sid}段{prefix}.{aid}状态必须为对象');continue
        for f in fields:
            if f not in b or f not in a or b[f]==a[f]:continue
            path=f'{prefix}.{aid}.{f}'
            if path in allowed:continue
            if prop and transition_allows(seg,aid,f,b[f],a[f]):continue
            errors.append(f'第{sid}段进入状态不承接：{path} {b[f]!r}→{a[f]!r}；需首动作变化或交接/状态转换镜')

def audit(segs):
    errors=[];warnings=[]
    if not segs:return {'errors':['没有分段'],'warnings':[],'stats':{'segment_count':0}}
    prev_id=None
    for i,seg in enumerate(segs,1):
        sid=seg.get('id',i)
        if prev_id is not None and isinstance(prev_id,int) and isinstance(sid,int) and sid!=prev_id+1:errors.append(f'段号不连续：{prev_id}→{sid}')
        prev_id=sid
        # per-segment sanity
        for state_name in ('entry','exit'):
            st=seg.get(state_name,{})
            props=st.get('props',{}) if isinstance(st,dict) else {}
            if isinstance(props,dict):
                for pid,pv in props.items():
                    if not isinstance(pv,dict):continue
                    if pv.get('continuity_active') is True:
                        for req in ('relation_mode','position_zone'):
                            if req not in pv:warnings.append(f'第{sid}段{state_name}连续道具{pid}缺少{req}')
        if i==1:continue
        prev=segs[i-2]; pexit=prev.get('exit',{}); centry=seg.get('entry',{})
        if not isinstance(pexit,dict) or not isinstance(centry,dict):errors.append(f'第{sid}段缺少可审查的entry或上一段exit对象');continue
        allowed=changed_paths(seg)
        compare(pexit.get('characters',{}),centry.get('characters',{}),CHARACTER_FIELDS,'characters',allowed,errors,sid,seg)
        compare(pexit.get('props',{}),centry.get('props',{}),PROP_FIELDS,'props',allowed,errors,sid,seg,True)
        compare(pexit.get('voices',{}),centry.get('voices',{}),VOICE_FIELDS,'voices',allowed,errors,sid,seg)
        pp=pexit.get('props') or {}; cp=centry.get('props') or {}
        if isinstance(pp,dict) and isinstance(cp,dict):
            for pid in sorted(set(pp)-set(cp)):
                pv=pp.get(pid) or {}
                if isinstance(pv,dict) and pv.get('continuity_active') is True:
                    errors.append(f'第{sid}段CONTINUITY_PROP_REFERENCE_DROPPED：{pid}上一段仍active=true但进入状态缺失')
                else:warnings.append(f'第{sid}段进入状态未列上一段道具：{pid}')
        # optional knowledge boundary continuity
        pk=pexit.get('character_knowledge',{}); ck=centry.get('character_knowledge',{})
        if isinstance(pk,dict) and isinstance(ck,dict):
            for cid in set(pk)&set(ck):
                before=set(map(str,pk.get(cid,[]) or [])); after=set(map(str,ck.get(cid,[]) or []))
                gained=after-before
                declared=set(map(str,(seg.get('knowledge_gains',{}) or {}).get(cid,[]) or [])) if isinstance(seg.get('knowledge_gains',{}),dict) else set()
                if gained-declared:warnings.append(f'第{sid}段角色{cid}新增知识未声明来源：'+ '、'.join(sorted(gained-declared)))
    return {'errors':errors,'warnings':warnings,'stats':{'segment_count':len(segs),'transition_count':max(0,len(segs)-1)}}

def render(r,fmt):
    if fmt=='json':return json.dumps(r,ensure_ascii=False,indent=2)
    s=r['stats']; lines=[f"分段数：{s['segment_count']}；相邻交接：{s.get('transition_count',0)}"]
    if fmt=='markdown':lines=['## 连续性审查','',f"- 分段数：{s['segment_count']}",f"- 相邻交接：{s.get('transition_count',0)}"]
    lines += [("- ERROR：" if fmt=='markdown' else 'ERROR: ')+x for x in r['errors']]
    lines += [("- WARN：" if fmt=='markdown' else 'WARN: ')+x for x in r['warnings']]
    if not r['errors'] and not r['warnings']:lines.append('PASS：人物、道具、声音与知识状态跨段连续。')
    return '\n'.join(lines)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('path');ap.add_argument('--format',choices=('text','markdown','json'),default='text');a=ap.parse_args()
    try:r=audit(load(a.path))
    except (OSError,ValueError,json.JSONDecodeError) as e:print('ERROR:',e,file=sys.stderr);return 2
    print(render(r,a.format));return 1 if r['errors'] else 0
if __name__=='__main__':raise SystemExit(main())
