#!/usr/bin/env python3
"""Audit Pro V1.6 full/quick Seedance prompts, @ binding, timing, and optional dialogue."""
from __future__ import annotations
import argparse,json,re,sys
from collections import Counter
from pathlib import Path

FULL_MODULES=["[声画硬锁]","[参考图 / 音频对应表]","[本段任务]","[人物状态、站位、面部朝向、轴线与群像]","[风格、光影与氛围]","[镜头时间轴]","[声音与剪辑]","[连续性底线]"]
FULL_BLOCKING_ALIASES=("[人物状态、站位、面部朝向、轴线与群像]","[人物状态、站位、轴线与群像]")
QUICK_MODULES=["[STYLELOCK]","[REFERENCE]","[SHOT]","[BEATS]"]
FORBIDDEN=("风险等级","生成风险","执行策略","稳定备选","[关键帧]","模仿导演","导演风格")
COMPLEX=("Technocrane","环绕","Whip Pan","鞭甩","Dolly Zoom","眩晕变焦","Crash Zoom","快速变焦","Crane","Jib")
VISUAL_PROGRESS=("L-cut","O.S.","反应","推进","横移","焦点","切","走位","动作","道具","景别","手部","POV","过肩","绕")
SCENE_HINTS=("场景","主视角","反打","卧室","宴会厅","室内","车内","楼下","小区","老宅","大厅","街道","房间")
PROP_HINTS=("手机","校牌","协议","合同","钥匙","道具","戒指","文件","信","卡片","手表","武器","挂件")

def section(text,heading,modules):
    start=text.find(heading)
    if start<0:return ""
    start+=len(heading); poss=[text.find(m,start) for m in modules if text.find(m,start)>=0]
    return text[start:min(poss) if poss else len(text)].strip()

def load_dialogues(path):
    if not path:return []
    data=json.loads(Path(path).read_text(encoding='utf-8'))
    if isinstance(data,list):return [str(x['text'] if isinstance(x,dict) else x) for x in data]
    if isinstance(data,dict):return [str(x['text'] if isinstance(x,dict) else x) for x in data.get('dialogues',[])]
    raise ValueError('dialogue JSON must be a list or contain dialogues')

def extract_dialogues(text):return [x.strip() for x in re.findall(r"\{([^{}]+)\}",text,flags=re.S)]

def shot_blocks(txt):
    marks=list(re.finditer(r"(?m)^\*{0,2}镜头\s*\d+[^\n]*",txt));out=[]
    for i,m in enumerate(marks):out.append(txt[m.start():(marks[i+1].start() if i+1<len(marks) else len(txt))].strip())
    return out

def shot_timecode(head):
    m=re.search(r"(\d+(?:\.\d+)?)\s*[—–-]\s*(\d+(?:\.\d+)?)\s*秒",head);return (float(m.group(1)),float(m.group(2))) if m else None

def tenth(x):return abs(x*10-round(x*10))<1e-7

def parse_mapping(mapping):
    items=[]
    for line in mapping.splitlines():
        clean=re.sub(r"[*`#]","",line).strip()
        m=re.search(r"([^=：:\n]+?)\s*(?:=|：|:)\s*(@\[(图片|音频)(\d+)\])",clean)
        if not m:continue
        name=m.group(1).strip(' -'); ref=m.group(2); kind=m.group(3)
        if kind=='音频':typ='audio'
        elif any(h in name for h in SCENE_HINTS):typ='scene'
        elif any(h in name for h in PROP_HINTS):typ='prop'
        else:typ='character'
        items.append({'name':name,'ref':ref,'kind':kind,'type':typ,'n':int(m.group(4))})
    return items

def sequential_reference_errors(mapping):
    errors=[]
    for label,pat in (("图片",r"@\[图片(\d+)\]"),("音频",r"@\[音频(\d+)\]")):
        vals=[int(x) for x in re.findall(pat,mapping)]
        if not vals:continue
        if len(vals)!=len(set(vals)):errors.append(f'{label}执行编号重复')
        uniq=list(dict.fromkeys(vals)); expected=list(range(1,len(uniq)+1))
        if uniq!=expected:errors.append(f'{label}执行编号必须从1开始并按映射顺序连续：当前为{uniq}')
    if re.search(r"@图\d+",mapping):errors.append('V1.6用户输出禁止使用旧@图N格式；改用@[图片N]')
    return errors

def audit_binding(shots,items,errors,warnings):
    scenes=[x for x in items if x['type']=='scene']; chars=[x for x in items if x['type']=='character']; props=[x for x in items if x['type']=='prop']
    used=set()
    for i,block in enumerate(shots,1):
        refs=set(re.findall(r"@\[(?:图片|音频)\d+\]",block));used|=refs
        # If mapped name is explicitly mentioned, require its ref in same shot.
        for it in chars+props+scenes:
            if it['name'] and it['name'] in block and it['ref'] not in refs:
                code='VISIBLE_CHARACTER_REFERENCE_MISSING' if it['type']=='character' else ('SCENE_REFERENCE_MISSING' if it['type']=='scene' else 'CONTINUITY_PROP_REFERENCE_MISSING')
                errors.append(f'镜头{i} {code}：提到“{it["name"]}”但未绑定{it["ref"]}')
        # if there are scene refs defined and shot has any image/visual content, expect one scene ref unless graphic/ECU explicitly says pure graphic
        if scenes and any(x['ref'] in refs for x in chars+props) and not any(x['ref'] in refs for x in scenes):
            if not any(k in block for k in ('纯色背景','纯白背景','GRAPHIC','字卡','设计化开场')):
                warnings.append(f'镜头{i} SCENE_REFERENCE_MISSING：存在人物/道具图绑定但未见场景@')
        # voice/image overbinding heuristic
        if re.search(r"\b(?:VO|O\.S\.|OS)\b|画外|电话VO|电话声音",block,re.I):
            for it in chars:
                if it['ref'] in refs and (it['name'] in block):
                    warnings.append(f'镜头{i} OFFSCREEN_CHARACTER_IMAGE_OVERBOUND：画外声音语境中同时绑定{it["ref"]}，确认该人物确实入画')
    for it in items:
        if it['ref'] not in used:warnings.append(f'UNUSED_REFERENCE_ASSET：参考表{it["ref"]}“{it["name"]}”未在镜头时间轴调用')

def audit(text,expected_dialogues,contract='auto'):
    errors=[];warnings=[]
    if contract=='auto':contract='full' if '[本段任务]' in text or '[镜头时间轴]' in text else 'quick'
    modules=FULL_MODULES if contract=='full' else QUICK_MODULES
    # Blocking alias compatibility
    working=text
    if contract=='full' and FULL_MODULES[3] not in working and FULL_BLOCKING_ALIASES[1] in working:
        working=working.replace(FULL_BLOCKING_ALIASES[1],FULL_MODULES[3],1);warnings.append('使用了V1.5旧站位模块名；V1.6建议加入“面部朝向”')
    pos=[]
    for m in modules:
        p=working.find(m);pos.append(p)
        if p<0:errors.append(f'缺少模块：{m}')
    present=[p for p in pos if p>=0]
    if present!=sorted(present):errors.append(f'{contract}契约模块顺序不正确')
    headings=re.findall(r"(?m)^\[[^\]\n]+\]\s*$",working);extra=[h for h in headings if h not in modules]
    if extra:errors.append('存在额外模块：'+'、'.join(extra))
    for term in FORBIDDEN:
        if term in working:errors.append(f'包含禁用内容：{term}')
    hard=section(working,modules[0],modules) if contract=='full' else working
    if '无字幕' not in hard and '唯一字幕' not in hard:errors.append('缺少无字幕/唯一字幕硬锁')
    if '无背景音乐' not in hard and '禁止生成BGM' not in hard:errors.append('缺少“无背景音乐”硬锁')
    mapping_heading=FULL_MODULES[1] if contract=='full' else QUICK_MODULES[1];mapping=section(working,mapping_heading,modules);items=parse_mapping(mapping);errors+=sequential_reference_errors(mapping)
    for line in [x.strip() for x in mapping.splitlines() if x.strip()]:
        if '=' in line and '@[图片' not in line and '@[音频' not in line:warnings.append(f'映射行可能缺少@素材：{line[:50]}')
    if contract=='quick':
        task='';blocking=section(working,'[SHOT]',modules)+'\n'+section(working,'[BEATS]',modules);style=section(working,'[STYLELOCK]',modules);shots_sec=section(working,'[BEATS]',modules);sound=shots_sec;continuity=shots_sec
    else:
        task=section(working,'[本段任务]',modules);blocking=section(working,FULL_MODULES[3],modules);style=section(working,'[风格、光影与氛围]',modules);shots_sec=section(working,'[镜头时间轴]',modules);sound=section(working,'[声音与剪辑]',modules);continuity=section(working,'[连续性底线]',modules)
        for tok in ('情绪','视点','钩子','气口'): 
            if tok not in task:warnings.append(f'[本段任务]可能缺少：{tok}')
        for tok in ('核心冲击','对比轴','视觉变化'):
            if tok not in task:errors.append(f'[本段任务]缺少V1.6字段：{tok}')
    for group,opts in {'左右关系':('左侧','右侧','画面左','画面右'),'朝向':('朝向','面向','背对'),'眼神':('眼神','视线','看向'),'轴线':('轴线','关系轴','180度'),'行动落点':('路径','落点','停在')}.items():
        if not any(o in blocking for o in opts):warnings.append(f'站位模块可能缺少{group}')
    if not any(x in style for x in ('主光','光源','日光','侧光','逆光','顶光','lighting','light source','daylight')):warnings.append('风格模块可能缺少主光来源/方向')
    shots=shot_blocks(shots_sec)
    if not shots:errors.append('[镜头时间轴]没有可识别镜头')
    audit_binding(shots,items,errors,warnings)
    timecodes=[];impact=0
    for i,b in enumerate(shots,1):
        head=b.splitlines()[0];tc=shot_timecode(head)
        if tc is None:warnings.append(f'镜头{i}缺少起止时间码')
        else:
            st,en=tc;timecodes.append((i,st,en))
            if en<=st:errors.append(f'镜头{i}结束时间必须晚于开始时间')
            if not tenth(st) or not tenth(en):errors.append(f'镜头{i}时间码必须按0.1秒规划精度')
        if re.search(r"\bIMPACT\b|核心冲击",head,re.I):impact+=1
        if not re.search(r"\b\d{2,3}\s*mm(?![A-Za-z])",b,re.I) and not any(k in b for k in ('GRAPHIC','字卡','设计化开场')):errors.append(f'镜头{i}缺少焦段')
        if contract=='full' and not re.search(r"\bf\s*/\s*\d+(?:\.\d+)?\b",b,re.I) and not any(k in b for k in ('GRAPHIC','字卡','设计化开场')):warnings.append(f'镜头{i}缺少f/光圈')
        if any(t.lower() in b.lower() for t in COMPLEX):
            miss=[x for x in ('起点','触发','路径','落点','焦点') if x not in b]
            if miss:errors.append(f'镜头{i}复杂运镜缺少：'+ '、'.join(miss))
        for line in extract_dialogues(b):
            if len(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]",line))>=13 and not any(t in b for t in VISUAL_PROGRESS):warnings.append(f'镜头{i} LONG_DIALOGUE_NO_CHOREOGRAPHY：长对白可能缺少内部视觉推进')
        if any(t in b for t in ('震惊','愤怒','害怕','无语','崩溃')) and not any(t in b for t in ('手','手机','道具','呼吸','喉','肩','重心','脚步','衣料','动作停','停在半')):warnings.append(f'镜头{i} FACE_ONLY_EMOTION：抽象情绪可能缺少第二表演通道')
        if re.search(r"\bAU\s*\d+\b",b,re.I):warnings.append(f'镜头{i}直接输出FACS AU编号')
    if impact!=1:errors.append(f'核心冲击镜头应为1个，当前识别到{impact}个')
    for (pi,_,pe),(ci,cs,_) in zip(timecodes,timecodes[1:]):
        if abs(pe-cs)>.05:errors.append(f'镜头{pi}与镜头{ci}时间码不连续：{pe:g}→{cs:g}')
    if timecodes and abs(timecodes[0][1])>.05:warnings.append(f'首镜从{timecodes[0][1]:g}秒开始')
    hd=re.search(r"(?m)^#.*?｜\s*(\d+(?:\.\d+)?)\s*秒\s*$",working)
    if hd and timecodes and abs(timecodes[-1][2]-float(hd.group(1)))>.05:errors.append(f'末镜结束{timecodes[-1][2]:g}秒，与段落时长{float(hd.group(1)):g}秒不一致')
    actual=extract_dialogues(shots_sec)
    if expected_dialogues:
        if actual!=expected_dialogues:errors.append('原台词逐字或顺序不一致')
        dup=[x for x,c in Counter(actual).items() if c>1]
        if dup:errors.append('台词重复出现：'+'｜'.join(dup))
    if not any(x in sound for x in ('Room Tone','Room tone','room tone','底噪','环境声')):warnings.append('声音模块可能缺少空间底噪')
    if not any(x in sound for x in ('J-cut','L-cut','声音桥','硬切','切点','跨镜')):warnings.append('声音模块可能缺少跨镜或剪辑关系')
    if contract=='full':
        for tok in ('道具','轴线','落点'):
            if tok not in continuity:warnings.append(f'连续性底线可能缺少：{tok}')
    long_dups=[line for line,c in Counter(line.strip() for line in working.splitlines() if len(line.strip())>=20 and not line.lstrip().startswith('镜头')).items() if c>1]
    if long_dups:warnings.append(f'发现{len(long_dups)}条长句重复，检查模块去重')
    return {'errors':errors,'warnings':warnings,'stats':{'contract':contract,'shots':len(shots),'dialogues':len(actual),'references':len(items)}}

def render(r,fmt):
    if fmt=='json':return json.dumps(r,ensure_ascii=False,indent=2)
    s=r['stats'];lines=[f"契约：{s['contract']}；镜头数：{s['shots']}；台词数：{s['dialogues']}；参考资产：{s['references']}"]
    if fmt=='markdown':lines=['## 提示词审查','',f"- 契约：{s['contract']}",f"- 镜头数：{s['shots']}",f"- 台词数：{s['dialogues']}",f"- 参考资产：{s['references']}"]
    lines += [("- ERROR：" if fmt=='markdown' else 'ERROR: ')+x for x in r['errors']]
    lines += [("- WARN：" if fmt=='markdown' else 'WARN: ')+x for x in r['warnings']]
    if not r['errors'] and not r['warnings']:lines.append('PASS：V1.6模块、@绑定、声画、时长、表演、镜头与连续性检查通过。')
    return '\n'.join(lines)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('path');ap.add_argument('--contract',choices=('auto','full','quick'),default='auto');ap.add_argument('--dialogue-json');ap.add_argument('--format',choices=('text','markdown','json'),default='text');a=ap.parse_args()
    try:text=Path(a.path).read_text(encoding='utf-8');r=audit(text,load_dialogues(a.dialogue_json),a.contract)
    except (OSError,ValueError,json.JSONDecodeError) as e:print('ERROR:',e,file=sys.stderr);return 2
    print(render(r,a.format));return 1 if r['errors'] else 0
if __name__=='__main__':raise SystemExit(main())
