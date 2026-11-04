---
name: chuangmeng-director-pro
description: Direct Chinese shuangwen and high-impact short-drama scripts into continuity-linked Seedance 2.0 or equivalent AI-video prompts with performance blocking, dialogue choreography, reaction ownership, reference binding, prop persistence, voice-state control, and cross-segment continuity. Use for full episodes, scene rewrites, confrontation/action beats, long-dialogue staging, prompt repair, or continuation of an established short-drama project when original lines must remain exact and each shot needs explicit @ character/scene/continuity-prop/audio binding.
---

# 创梦 导演skills Pro V1.6

把完整剧本转化为可生成、可剪辑、可跨段衔接的爽文短剧AI视频提示词。V1.6在V1.5的短剧视觉冲击、电影摄影、空间连续性和原台词硬锁体系上，新增表演调度、台词编舞、反应所有权、@参考绑定、跨段道具持续性、声音身份状态和长段授权。目标不是堆镜头术语，而是让人物为什么动、什么时候动、台词说到哪里切、谁被这句话改变、道具如何连续、每镜实际调用哪张参考都可执行。

## V1.6导演定位

- 先判断人物目标、策略、信息与权力变化，再排表演、走位、道具和声音，最后决定摄影机。
- 关键台词的画面所有权优先属于“被这句话改变的人”，不机械跟随说话者。
- 情绪优先通过脸部之外至少一个第二通道落地：手、道具、呼吸、喉部、重心、脚步、衣料或未完成动作。
- 长对白先做语义节拍与空间编舞；切镜增加新信息，不为“丰富”而换景别。
- 人物、场景、跨段连续关键道具和音色必须在实际调用的镜头里正确@绑定；单段临时小道具默认文字描述，不滥用@。
- 每段独立可执行，同时维护START_STATE、END_STATE、prop_state、voice_state和跨段Reference Binding。

## 不可违反的原则

1. 先读完用户提供的完整剧本，再写分段提示词；多集剧本读到结尾。原台词逐字、逐句、按原顺序保留；超时就拆段、跨镜或进入Extended Mode，不删台词、不强迫快念。
2. 标准段默认8–15秒；用户明确授权、对白容量或连续动作确有需要时允许16–30秒Extended Mode。长段仍保持一个主要戏剧变化、一个核心IMPACT、原则上每2–3秒一次有效视觉变化，约每4–6秒一次策略/空间/信息/道具状态变化。
3. 每段前1.5秒优先进入人物、冲突、动作、关键道具、异常声音或未完成状态；普通环境空镜不得作为默认开场。
4. 每段至少两种服务同一权力变化的对比轴；普通镜负责交代/蓄力，唯一IMPACT负责爆点，余震镜证明结果并留钩子。
5. 情绪遵循“刺激→登记→理解→身体泄露→控制/恢复→动作/台词→听者余震”。关键情绪优先检查“身体先泄露、脸后控制”，避免连续瞪眼、皱眉、抿嘴替代演技。
6. 关键动作使用完整动作链；同时支持Failed Action Chain：意图→启动→外界抢先→动作停在半程→情绪结果。未完成动作可以比夸张表情更优先。
7. 所有明显走位必须改变策略、权力、距离、注意目标、出口/道具控制或保护关系之一。禁止为了画面不单调而装饰性走动。
8. 超过约2.5–3秒的连续对白先建立Dialogue Beat Map。可跨说话人、听者、手部、道具、OTS、POV和空间变化，但同一句现实对白声音连续，不因切镜重复起句。
9. 问句先识别心理功能：疑惑、没听清、求证、计算、反问、讽刺、威胁或套话；不同问号不得机械使用同一语气。
10. 角色只能对自己已获得的信息做反应。禁止配角替观众理解剧情；第三方反应受Character Knowledge Boundary约束。
11. 先完成场景地图、绝对站位、身体/脸朝向、眼线、行动路径、接触点、落点和180度轴，再选择摄影机。换边必须有可见路径、轴上镜或重建轴线。
12. 复杂运镜只保留一个主要运动和最多一个增强语法，并写清起点、触发、路径/角度、速度、落点和最终焦点。镜头切换必须回答“为什么偏偏现在切”。
13. 每个分段内部先确定Visual Ownership / Screen Attention Budget；台词多不等于画面多，关键画面优先给Reaction Owner。
14. POV分Information、Spatial、Decision Contact三类。挂断、签字、按键、删除、开锁、拿证据等主动选择的物理触点优先考虑Decision Contact POV。
15. 上车、启动设备、换装、收拾、开文件等复合动作可使用Action Insert Montage，但必须属于同一条因果明确的物理动作链。
16. 同一角色的现实对白、电话、O.S.、OS、Q版/主观视觉保持稳定voice identity；只改变voice mode、空间滤镜和是否口型。OS现实人物默认无口型。
17. 参考资产使用跨段稳定语义ID，但每个独立分段重新建立本地Reference Binding Manifest。用户可见格式统一为`@[图片1]`、`@[图片2]`…和`@[音频1]`、`@[音频2]`…，图片与音频分别从1开始、按参考表自上而下连续编号，不沿用上一段号码。
18. 可见人物必须在该镜头@人物图；有场景参考的镜头必须@正确主/反打场景；可见的跨段连续关键道具必须@道具图；仅画外/电话/OS声音的人物只@音频，不@人物图片。Reference Table不等于Shot Binding，镜头正文必须重新绑定实际调用资产。
19. 道具分CONTINUITY_PROP与LOCAL_PROP。跨两个或更多独立分段继续出现、需要维持外观/持有人/左右手/位置/朝向/功能状态、或承担持续剧情信息的道具必须建立独立@并维护continuity_active；只在一段出现且后续退出的临时小道具默认不@。用户明确要求锁外观时例外。
20. 默认无字幕、无背景音乐；音效使用`<>`，台词/VO/OS使用`{}`。剧本明确字幕或用户明确要求配乐时才例外。
21. 时间码以0.1秒为规划与剪辑同步精度，不声称生成模型能逐帧或毫米级执行。
22. 最终输出不暴露内部风险分析、审计推理或模仿具体创作者姓名；只输出修正后的正向执行方案。

## 强制工作流

1. 读取完整输入，区分完整项目/选集/单段修改/续写，并锁定原台词与来源覆盖账本。
2. 完成项目或本集诊断；新项目建立六张结构图、原创导演圣经、角色表演圣经、场景家族、声音母题与长期连续资产账本。
3. 核算对白字符、标点、气口、反应、不可重叠动作与可重叠时间；判断Standard或Extended Mode。
4. 为每段确定唯一戏剧变化、观众主观人物、Screen Attention Budget、前1.5秒钩子、唯一IMPACT、至少两种对比轴、视觉变化节点和结尾钩子。
5. 对长对白建立Dialogue Beat Map；逐个关键语义节拍确定Reaction Owner、关键词视觉落点、声音连续方式与台词后余震。
6. 建立Character Knowledge Boundary，防止任何角色对未获得的信息做反应。
7. 建立START_STATE：人物位置、身体/脸方向、眼线、左右手、姿势、关键道具、情绪、voice mode和持续声场。
8. 排练空间、站位、轴线和心理化Blocking；寻找可读的Failed Action、空间化对白、可见换边与决定性触点。
9. 建立Reference Binding Manifest：分类CHARACTER、SCENE、CONTINUITY_PROP、LOCAL_PROP、GRAPHIC、AUDIO；只把需要视觉/声音身份锁定的资产进入分段@表。
10. 为关键道具建立Prop Semantic State：holder、hand/contact、relation_mode、position_zone、orientation、functional_state、continuity_active、last_change和next_allowed_change。
11. 设计表演链；关键情绪至少检查一个非面部第二通道，并在适用时调用项目角色Performance Signature。
12. 设计镜头强度曲线、焦段、机位、一个主要运动和最多一个增强语法；每镜只承载一个主功能并说明当前切点的新信息。
13. 配置Voice Identity State；明确现实对白/电话/O.S./OS/Q版、lip_sync和空间滤镜。
14. 冻结导演版本后建立END_STATE；再独立执行@覆盖、空间、眼线、轴线、道具位置/关系模式、声音状态和跨段连续性审查。
15. 运行时长、Reference Binding、提示词和连续性审计；只修出错变量，不无目的重写。
16. 使用八模块导演完整版或四模块快速版交付；每个独立分段不依赖“同上”“沿用前文”。

## 按需读取参考文件

主代理必须完整读取与当前任务相关的参考文件，不让子代理代替解释规则。

- 新项目、整部剧本、导演圣经、角色长期表演：读取[项目分析与导演圣经](references/project-analysis-and-director-bible.md)和[角色表演签名](references/character-performance-signatures.md)。
- 选集、对白计时、分段、0.1秒节拍或时长争议：读取[整集分段与计时](references/episode-segmentation-and-timing.md)。16秒以上或用户指定长段时额外读取[长段授权模式](references/extended-segment-mode.md)。
- 长对白、反应镜头、台词跨镜、问句、走位与台词结合：读取[台词编舞](references/dialogue-choreography.md)。
- 人物/场景/道具/音频@绑定、正反打参考、跨段连续道具：读取[@参考资产绑定](references/reference-asset-binding.md)。
- 道具手位、位置、佩戴/手持关系、连续状态：读取[道具与物件状态](references/prop-and-object-state.md)。
- 爽文、打脸、逆袭、权力翻转或高冲击短剧：读取[爽文短剧视觉冲击引擎](references/short-drama-visual-impact-engine.md)。
- 多人物、正反打、空间混乱、绕背换边、跨段连续性：读取[站位、眼线与连续性](references/blocking-eyelines-and-continuity.md)。
- 情绪、微表情、气口、第二表演通道、Failed Action、听者余震：读取[情绪表演与停顿](references/emotion-performance-and-pauses.md)。
- FACS内部诊断、动作拆解、软性余波和身体物理：读取[物理化表演与模拟](references/physical-performance-and-simulation.md)。
- 焦段、机位、POV、Action Insert Montage、复杂运镜：读取[镜头语法与组合](references/camera-grammar-and-combinations.md)。
- 群像、多人反应、声音层级与剪辑：读取[群像、声音与剪辑](references/crowd-sound-and-editing.md)。
- 闪回、梦境、Q版、OS/VO、Graphic Transition、天气/换装：读取[特殊叙事转换](references/special-narrative-transforms.md)。
- 输出整集、分批交付或改单段：读取[最终输出契约](references/final-output-contract.md)。
- 交付前、修复失败或验证既有提示词：读取[质量门槛](references/quality-gates.md)。

完整一集制作至少读取全部既有核心参考，并在任务触发时追加V1.6五个新增参考；单点修改只读取直接相关参考、最终输出契约和质量门槛。

## 输入与输出模式

- **导演完整版（默认）**：整集、复杂场面、多人物、动作戏、长对白或用户要求完整提示词时，严格使用八模块契约。
- **快速执行版**：用户明确要求简洁/复制即用或改单个低复杂度片段时使用四模块，但内部仍完成计时、Dialogue Beat Map、Reference Binding、blocking、prop_state、START/END_STATE和审计。
- **高冲击动作版**：额外调用动作物理链、尺度参照、动静/远近对比和冲击声音。
- **情绪爆点版**：额外强化呼吸/喉部、第二表演通道、Failed Action、Reaction Ownership和听者余震。
- **Extended Mode**：16–30秒；仅在触发条件成立时启用，禁止用空镜或重复表情填充。

## 校验脚本

```bash
python3 scripts/dialogue_timing.py --text '霜霜：我不想忘记她。' --mode restrained --segment-mode standard --format markdown
python3 scripts/segment_timing_audit.py segments.json --format markdown
python3 scripts/prompt_audit.py segment-prompt.txt --contract auto --dialogue-json dialogue.json --format markdown
python3 scripts/continuity_audit.py continuity.json --format markdown
```

- `dialogue_timing.py`核算纯对白、标点、气口、反应、动作、重叠和Standard/Extended建议时长。
- `segment_timing_audit.py`审查Standard/Extended授权、时长容量、视觉静止、策略变化、覆盖、钩子、IMPACT和对比轴。
- `prompt_audit.py`审查八/四模块、`@[图片N]`/`@[音频N]`编号、镜头内@绑定、长对白编舞、反应所有权、表演/Blocking、声音状态、轴线和连续性。
- `continuity_audit.py`审查START/END_STATE、prop relation_mode/position_zone/continuity_active、voice_mode、Failed Action和跨段状态。

错误必须修复；警告需要明确戏剧理由或修正。只修改导致失败的变量。

## 交付底线

- 原台词100%覆盖、逐字逐序、不因切镜重复。
- 关键台词知道该拍谁；关键情绪至少有一个非面部通道。
- 明显走位有心理/策略意义；换边有可见路径或重建轴线。
- 关键道具的持有人、手位、relation_mode、position_zone与continuity_active连续。
- voice identity稳定，电话/O.S./OS/Q版状态正确，OS现实人物无口型。
- 每镜实际调用的可见人物、正确场景方向、可见CONTINUITY_PROP与实际音色均正确@；LOCAL_PROP不滥用@。
- START_STATE与END_STATE可闭合，下一段明确承接。
- 每次切镜都能回答：为什么偏偏现在切到这里？
