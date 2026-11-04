# 创梦 导演skills Pro V1.6

**完整Pro导演系统：把剧本组织成有表演、有空间、有动作因果、有声画与跨段连续性的AI视频提示词。**

开源发行 **v1.6.1 Pro** · 作者 **LERler-Q** · 前身 **CineWeaver Director Engine**

[下载Pro完整版](../../releases/tag/v1.6.1) · [English](README_EN.md) · [Skill入口](SKILL.md)

## 当前版本

本次以现有 **Pro V1.6完整原包** 为源发布，完整保留导演规则、参考文档和4个审计脚本。项目名称、安装标识和公开说明已适配“创梦 导演skills”。

| 版本 | 内容 | 入口 |
|---|---|---|
| **v1.6.1 Pro** | 原Pro V1.6完整能力，本次默认发行 | [发布与下载](../../releases/tag/v1.6.1) |
| v1.6.0 Community | 之前的社区稳定版，保留历史发行 | [历史下载](../../releases/tag/v1.6.0) |
| v2.0.0-beta.1 Community | 现有社区状态流程预览版，保持原状 | [发布与下载](../../releases/tag/v2.0.0-beta.1) |
| v1.5.5 Community | 历史轻量社区版 | [详细介绍](docs/releases/v1.5.5.md) · [下载](../../releases/tag/v1.5.5) |

Pro V1.6是导演系统版本，v1.6.1是本次开源发行号；它们与Seedance等视频模型的版本号分别记录。

## 完整Pro有哪些能力？

| 能力 | 制作中的用途 |
|---|---|
| 原台词硬锁与原文覆盖账本 | 保留台词、顺序及剧情事件，容量不足时重新分段 |
| Character Performance Signature | 保存角色长期表演习惯，按触发条件与强度调用 |
| Dialogue Choreography | 按语义节拍编排对白、动作、反应与镜头切点 |
| Reaction Ownership | 将关键画面交给真正承担信息和情绪变化的人 |
| Failed Action | 写清被打断的动作、停在半程的姿态及后果 |
| Character Knowledge Boundary | 约束人物依据已获得的信息产生反应 |
| Screen Attention Budget | 根据人物策略和权力变化分配画面注意力 |
| Prop Semantic State | 维护持有人、手位、接触、佩戴/手持/放置关系、位置区域、朝向和功能 |
| Voice Identity State | 统一角色音色，区分现实、电话、O.S.、OS与VO的空间和口型模式 |
| Semantic ID / Reference Manifest | 跨段保持素材身份，独立分段重新建立本地编号 |
| 实际镜头内@绑定 | 绑定本镜可见人物、正确场景方向、可见连续道具及实际音色 |
| Decision Contact POV | 拍清按键、签字、解锁、拿证据等决定性物理触点 |
| Action Insert Montage | 将复合动作编排为同一条因果明确的动作链 |
| START_STATE / END_STATE | 记录并衔接人物、道具、动作、声音与已知信息 |

## 如何工作？

1. 读完指定范围，建立原台词与剧情节点覆盖记录。
2. 梳理情绪、人物目标、信息边界、策略与权力变化。
3. 新项目建立导演圣经、角色表演签名、场景与长期资产。
4. 核算对白、气口、反应、动作与可重叠时间，给出完整分段总表。
5. 排站位、身体/面部朝向、眼线、路径、道具与轴线，再选择摄影机。
6. 建立本段参考清单，在实际镜头中绑定可见/可听素材。
7. 编排表演、镜头、声音和剪辑，生成完整START_STATE与END_STATE。
8. 使用原版审计工具检查时长、绑定与连续性交接。

## Pro参考绑定方式

Pro保留原始逐镜绑定规则：**参考表定义编号，镜头正文重新调用实际素材。**

- 每个独立段的图片、音频分别从 `@[图片1]`、`@[音频1]` 连续编号。
- 可见人物绑定人物图；有场景参考时绑定实际摄影方向。
- 可见的CONTINUITY_PROP绑定独立道具图；LOCAL_PROP默认文字描述。
- 实际发声绑定音色；只通过画外/电话/OS出现的角色不强行绑定人物图。
- Semantic ID跨段稳定，本地上传编号可以重建。

[完整参考绑定规则](references/reference-asset-binding.md) · [道具状态](references/prop-and-object-state.md)

## 输出格式

| 八模块完整版 | 内容 |
|---|---|
| `[声画硬锁]` | 声画、原台词、环境声与发声规则 |
| `[参考图 / 音频对应表]` | 本段实际使用的参考 |
| `[本段任务]` | 戏剧变化、冲突、时长、冲击、对比与钩子 |
| `[人物状态、站位、面部朝向、轴线与群像]` | 人物、空间、路径和初始道具状态 |
| `[风格、光影与氛围]` | 摄影语法、真实光源和场景质感 |
| `[镜头时间轴]` | 逐镜绑定、动作、表演、原台词、声音与切点 |
| `[声音与剪辑]` | 持续声场、对白跨镜、声音桥与剪辑 |
| `[连续性底线]` | 退出状态及相邻段交接 |

简洁任务使用 `[STYLELOCK]`、`[REFERENCE]`、`[SHOT]`、`[BEATS]` 四模块快速版。Pro快速版的逐镜节拍位于BEATS模块。

[完整版示例](examples/full-prompt.txt) · [快速版示例](examples/quick-prompt.txt) · [原版输出契约](references/final-output-contract.md)

## 安装与启动

下载 `Chuangmeng_Director_Skills_Pro_v1.6.1.zip`，解压后按平台Agent Skills安装方式导入 `chuangmeng-director-pro/`，入口为 `SKILL.md`。

安装标识是 **`chuangmeng-director-pro`**，原Pro技能名为 `direct-episode-to-seedance-prompts-pro-v1-6`。社区版使用 `chuangmeng-director`；同时存在时请明确选择Pro。

```text
使用 $chuangmeng-director-pro 处理完整剧本。
目标平台与当前上限：[填写]
画幅及媒介：[填写]
保留全部原台词，先排表演、对白编舞、站位、道具与声音，再设计摄影机。
启用角色表演签名、Screen Attention Budget、Prop Semantic State与Voice Identity State。
建立Semantic ID与每段本地Reference Binding Manifest，在实际镜头中绑定素材。
按Standard/Extended核算时长，先给完整分段表，再给全部八模块提示词与连续性交接。
剧本、参考及已有状态：[粘贴]
```

Standard默认8–15秒；用户授权且平台支持时可用16–30秒Extended。目标平台支持能力决定实际上限。Pro保留原始节奏与计时逻辑，不套用此前社区版新增的单镜4秒硬上限或参考表集中调用策略。

## 原版工具

| 脚本 | 用途 |
|---|---|
| `dialogue_timing.py` | 对白、气口、反应、动作、重叠与分段建议 |
| `segment_timing_audit.py` | Standard/Extended容量、覆盖、冲击与密度 |
| `prompt_audit.py` | 八/四模块、逐镜@、对白、摄影与声音规则 |
| `continuity_audit.py` | 人物、道具语义、声音身份、知识与交接 |

```bash
python3 scripts/dialogue_timing.py --text '我不会再退了。' --mode restrained --segment-mode standard --format json
python3 scripts/segment_timing_audit.py examples/segments-standard.json --format json
python3 scripts/prompt_audit.py examples/full-prompt.txt --dialogue-json examples/dialogue.json --format json
python3 scripts/continuity_audit.py examples/continuity.json --format json
```

## 完整性与来源

[SOURCE_MANIFEST.json](SOURCE_MANIFEST.json) 记录原Pro包每个文件的SHA-256及导出方式。全部原始参考文档、4个审计脚本与原图标逐字节包含；SKILL.md仅更换安装名与标题，界面元数据同步品牌和调用名。

[角色表演签名](references/character-performance-signatures.md) · [长段模式](references/extended-segment-mode.md) · [对白编舞](references/dialogue-choreography.md) · [版本记录](CHANGELOG.md)

## 许可与作者

程序代码采用[MIT](LICENSE-CODE)；Skill指令、方法论、文档及文字示例采用[CC BY 4.0](LICENSE-DOCS)。作者署名 **LERler-Q**，项目名“创梦 导演skills”，前身CineWeaver Director Engine。

本项目为独立、非官方项目，第三方模型、产品名称与商标归其权利人。
