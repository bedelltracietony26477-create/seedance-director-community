# 创梦 导演skills Pro

**从剧本到镜头，组织人物表演、动作、对白与连续性。**

创梦 导演skills 是面向 AI 影视创作者的开源导演 Skill。输入完整剧本和参考素材，即可围绕人物目标、情绪变化、空间关系与动作因果，编排分段视频提示词。

适用于短剧、单场对白、情绪冲突、连续动作和局部补拍。

**v1.6.1 Pro · 作者 LERler-Q**

[下载 Pro](../../releases/tag/v1.6.1) · [快速开始](#快速开始) · [使用示例](examples/full-prompt.txt) · [English](README_EN.md)

## 选择版本

| 版本 | 主要功能 | 获取 |
|---|---|---|
| **v1.6.1 Pro** | 角色表演、对白编舞、逐镜参考绑定、人物与道具声音连续性 | [下载 Pro](../../releases/tag/v1.6.1) |
| v2.0.0-beta.1 Community | 轻量状态账本、镜头事件记录与局部返修流程 | [查看预览版](../../releases/tag/v2.0.0-beta.1) |
| v1.6.0 Community | 逐镜可见性、动作衔接、眼线与声画连续 | [下载社区版](../../releases/tag/v1.6.0) |
| v1.5.5 Community | 轻量对白编舞、参考绑定与基础跨段交接 | [了解更多](docs/releases/v1.5.5.md) · [下载](../../releases/tag/v1.5.5) |

Pro 适合需要系统安排人物表演、道具、声音与镜头关系的制作任务。Community 提供更轻量的工作流；2.0 预览版可用于体验结构化状态记录与返修。

## 让一场戏拍得清楚、演得连贯

### 先排戏，再决定摄影机

先梳理人物目标、阻力、策略和权力变化，再安排站位、视线、行动路径与摄影机。每次走位和切镜都围绕戏剧变化展开。

### 让人物有自己的表演方式

角色表演签名记录人物的眼神路线、气口、手部习惯和身体控制，按具体刺激与情绪强度调用。人物跨段、跨集的表演拥有可延续的行为依据。

### 把长对白变成可观看的戏

按信息、逼问、证据、转折等语义节拍编排对白。关键画面可以落在说话者、听者、手部、道具或空间结果上；同一句对白跨镜接续，保持声音事件连续。

### 动作有起点，也有落点

写清起势、发力、路径、接触和结果，连接相邻镜头的动作相位。被打断的伸手、欲起身或按键动作，可以停在半程并成为下一镜的起点。

### 道具与声音跟着剧情走

道具记录持有人、手位、接触方式、位置区域与功能状态。声音区分现实对白、电话、同场画外、内心与旁白模式，同时维持角色声音身份。

## Pro 导演能力

| 能力 | 用途 |
|---|---|
| 原台词硬锁与原文覆盖账本 | 保留台词、顺序和剧情事件，按容量安排分段 |
| Character Performance Signature | 组织角色长期表演习惯与轻、中、重强度变体 |
| Dialogue Choreography | 编排对白、动作、听者反应和镜头切点 |
| Reaction Ownership | 确定谁承担一句话带来的信息与情绪变化 |
| Failed Action | 设计动作中断、停顿与后果 |
| Character Knowledge Boundary | 让人物根据已经获得的信息反应 |
| Screen Attention Budget | 根据人物策略和权力变化安排画面注意力 |
| Prop Semantic State | 管理手持、佩戴、放置等关系及道具持续状态 |
| Voice Identity State | 组织角色音色、发声模式、口型与空间处理 |
| Semantic ID / Reference Manifest | 维护素材身份，建立每段本地参考映射 |
| 逐镜参考绑定 | 调用本镜可见人物、正确场景方向、连续道具与实际音色 |
| Decision Contact POV | 呈现按键、签字、解锁、拿证据等决定性触点 |
| Action Insert Montage | 将复合动作组织为因果连贯的局部镜头 |
| START_STATE / END_STATE | 衔接人物、道具、动作、声音和已知信息 |

## 制作流程

1. **读取剧本**：建立原台词、动作事件和剧情节点的覆盖记录。
2. **梳理戏剧**：明确情绪、人物目标、信息边界与策略变化。
3. **建立项目设定**：组织导演圣经、角色表演签名、场景与长期资产。
4. **分段计时**：核算对白、气口、反应、动作及重叠时间。
5. **排空间与表演**：安排站位、面部朝向、眼线、道具、路径和轴线。
6. **设计镜头与声音**：建立本段参考映射，编排逐镜动作、发声与切点。
7. **交接连续状态**：写清每段的进入、退出与下一段承接关系。

## 输出格式

每个分段提供八模块完整版提示词：

| 模块 | 内容 |
|---|---|
| `[声画硬锁]` | 声画、原台词、环境声与发声规则 |
| `[参考图 / 音频对应表]` | 本段实际使用的人物、场景、道具与声音参考 |
| `[本段任务]` | 戏剧变化、冲突、时长、冲击、对比与钩子 |
| `[人物状态、站位、面部朝向、轴线与群像]` | 人物、空间、行动路径和初始道具状态 |
| `[风格、光影与氛围]` | 摄影语法、光源与场景质感 |
| `[镜头时间轴]` | 逐镜参考、动作、表演、原台词、声音与切点 |
| `[声音与剪辑]` | 持续声场、对白跨镜与声音桥 |
| `[连续性底线]` | 退出状态与相邻段交接 |

简洁任务可使用 `[STYLELOCK]`、`[REFERENCE]`、`[SHOT]`、`[BEATS]` 四模块快速版。

[完整版示例](examples/full-prompt.txt) · [快速版示例](examples/quick-prompt.txt) · [输出格式说明](references/final-output-contract.md)

## 快速开始

1. 下载 [v1.6.1 Pro 安装包](../../releases/tag/v1.6.1)。
2. 解压后，按所用平台的 Agent Skills 安装方式导入 `chuangmeng-director-pro/`。
3. 提供完整剧本、已有参考、目标平台与时长要求，调用 `$chuangmeng-director-pro`。

入口文件：`SKILL.md`。Pro 的安装标识为 **`chuangmeng-director-pro`**。

```text
使用 $chuangmeng-director-pro 处理以下完整剧本。

目标平台与单段时长上限：[填写]
画幅及媒介：[填写]
处理范围：[整集 / 单场 / 指定选段]

保留全部原台词及剧情事件。
先梳理情绪、人物表演、对白编舞、空间、道具与声音，再设计镜头。
使用角色表演签名、画面注意力预算、道具语义状态与声音身份状态。
建立每段参考映射，并在实际镜头中绑定素材。
先给完整分段表，再给全部八模块提示词与连续性交接。

剧本：[粘贴]
参考素材与已有状态：[补充]
```

[快速启动指令](examples/QUICK_START_PROMPT_CN.md) · [制作启动指令](examples/ADVANCED_STARTER_PROMPT_CN.md)

## 参考素材怎么使用？

参考表建立本段编号，镜头正文调用实际入画、发声的素材：

- 图片和音频分别从 `@[图片1]`、`@[音频1]` 连续编号。
- 人物入画时绑定人物图，场景参考匹配当前摄影方向。
- 可见的连续关键道具使用独立道具图，临时道具按需要用文字描述。
- 实际发声时调用音色；仅通过画外、电话或内心声音出现的角色使用声音参考。
- 跨段使用稳定的素材身份，每段重新建立本地编号。

[参考绑定指南](references/reference-asset-binding.md) · [道具状态指南](references/prop-and-object-state.md)

## 分段与节奏

Standard 模式默认使用 8–15 秒分段；目标平台支持长段、且任务需要时，可使用 16–30 秒 Extended 模式。

按戏剧变化安排镜头长度，用动作相位、视线和声音连接切点。对白、气口与动作的实际容量决定分段，连续长段围绕一个主要戏剧目标推进。

[长段模式](references/extended-segment-mode.md) · [对白编舞](references/dialogue-choreography.md)

## 制作辅助工具

提供四个 Python 标准库脚本：

| 工具 | 用途 |
|---|---|
| `dialogue_timing.py` | 对白、气口、反应、动作与重叠时间估算 |
| `segment_timing_audit.py` | 分段容量、剧情覆盖、冲击与节奏检查 |
| `prompt_audit.py` | 提示词模块、逐镜参考、对白、摄影与声音规则检查 |
| `continuity_audit.py` | 人物、道具、声音与信息状态交接检查 |

```bash
python3 scripts/dialogue_timing.py --text '我不会再退了。' --mode restrained --segment-mode standard --format json
python3 scripts/segment_timing_audit.py examples/segments-standard.json --format json
python3 scripts/prompt_audit.py examples/full-prompt.txt --dialogue-json examples/dialogue.json --format json
python3 scripts/continuity_audit.py examples/continuity.json --format json
```

## 文档与交流

[角色表演签名](references/character-performance-signatures.md) · [镜头语言](references/camera-grammar-and-combinations.md) · [版本记录](CHANGELOG.md) · [贡献说明](CONTRIBUTING.md) · [反馈问题](../../issues)

欢迎交流具体的分镜、表演、素材绑定与连续性问题。反馈时可附版本、目标平台、提示词片段及预期画面，方便讨论与复现。

## 作者与许可

作者：**LERler-Q**。项目原名 **CineWeaver Director Engine**。

代码采用 [MIT](LICENSE-CODE)；Skill 指令、方法论、文档与文字示例采用 [CC BY 4.0](LICENSE-DOCS)。

创梦 导演skills 为独立、非官方项目。第三方模型、产品名称与商标归其权利人。
