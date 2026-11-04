<div align="center">

# 创梦 导演skills

### Chuangmeng Director Skills

**把完整剧本转成有表演、有调度、镜头清楚、前后连续的 AI 视频分段提示词。**

原台词保留 · 逐镜可见性 · 人物表演 · 动作衔接 · 空间眼线 · 声画连续 · 分段交接

**Community v1.5.5 历史版 / v1.6.0 稳定版 / v2.0.0-beta.1 预览版**

Created & maintained by **LERler-Q**

[下载稳定版](https://github.com/bedelltracietony26477-create/seedance-director-community/releases/tag/v1.6.0) · [体验 2.0 预览版](https://github.com/bedelltracietony26477-create/seedance-director-community/releases/tag/v2.0.0-beta.1) · [English](README_EN.md) · [反馈问题](https://github.com/bedelltracietony26477-create/seedance-director-community/issues)

</div>

> **当前页面：v1.6.0 稳定版。** v2.0.0-beta.1 在独立预览分支维护。

前身为 **CineWeaver Director Engine / Seedance Director Community**。项目名称更新为“创梦 导演skills”，现有仓库地址与历史版本保留；Skill 安装标识更新为 `chuangmeng-director`。

## 这是什么？

创梦 导演skills 是一套供支持 Agent Skills 的 AI 助手读取和执行的**影视导演工作流**，附带可在本地运行的 Python 审计工具。

你提供剧本、参考素材和制作要求，工作流先梳理这场戏的情绪、动作与空间，再组织人物表演、镜头、对白、声音和跨段连续性，输出可交给目标视频生成平台的提示词。

它的制作目标是让每个分段都回答清楚：**这一刻拍谁、画面能看到什么、人物怎么动、声音怎么接、下一段从什么状态开始。**

当前交付形式为 **Skill 指令 + 导演参考文档 + 示例 + 审计脚本**。视频生成仍需在你选择的平台完成；本项目没有内置视频生成服务，也不会自动上传素材或调用模型生成影片。

## 它针对哪些制作问题？

| 常见问题 | 工作流如何处理 |
|---|---|
| 长对白只有一个近景，人物站着念词 | 先分析语义节拍，安排动作、反应、注意目标与切点；跨镜声音保持连续 |
| 单人镜头写“看向某人”，模型不清楚方向 | 写成相对镜头的左/右、画内/画外和视线高度，并与场景轴线对应 |
| 特写中同时要求脚步、全身动作和手部细节 | 按当前景别筛选真正可见的行为，需要时补合适的局部镜头 |
| 两个连续动作被生成成先后等待 | 标明动作起势、路径、接触、落点与重叠窗口，下一镜从当前动作相位接入 |
| 一切镜就重复起句或重新吸气 | 把跨镜对白作为同一次声音事件；画外发声用 O.S. 等模式标明归属 |
| 反打后左右混乱、人物无故换座 | 用固定场景锚点记录真实站位，再分别描述每个机位的构图和眼线 |
| 下一段道具换手、坐姿变跪姿 | 重建完整进入/退出状态；2.0 预览版增加结构化状态账本辅助检查 |
| 提示词很长，却说不清镜头里有什么 | 明确每镜主体、实际入画者、前后景、可见动作、一个主要运镜和动作落点 |

制作时可根据剧本、参考素材和目标平台调整镜头与分段。

## 选择哪个版本？

| 能力 / 使用方式 | v1.5.5 历史社区版 | v1.6.0 稳定版 | v2.0.0-beta.1 预览版 |
|---|---|---|---|
| 安装标识 | `seedance-director-community` | `chuangmeng-director` | `chuangmeng-director` |
| 原台词与对白编舞 | 原台词硬锁、Beat Map Lite、Reaction Ownership | 继承并完善执行与审计 | 继承1.6 |
| 可见性、眼线与动作 | 已有空间、表演与动作过程规则 | 加强逐镜可见性、镜头相对眼线、动作相位 | 继承1.6 |
| 镜头节奏 | 约2–3秒有效视觉变化，可有动机延长 | 默认2–4秒单镜且不超过4秒；整段整数秒 | 继承1.6 |
| 参考绑定 | 参考表定义 + 实际镜头调用 | 默认参考表集中，逐镜调用为兼容策略 | 继承1.6 |
| 独立分段与基础状态 | 人物、手位、道具与进入/退出交接 | 继承并明确执行约束 | 进一步结构化 |
| 导演版剧本 | 原文覆盖、表演与动作梳理 | 明确动作补充与原文事实边界 | SOURCE → DIRECTOR_SCRIPT → STATE → EVENT 流程 |
| 状态账本与事件回放 | 无新增账本审计器 | 无新增账本审计器 | `state_ledger_audit.py`，含情绪/知识等显式状态 |
| 审计工具 | 4个历史标准库工具 | 4个工具及新版对白/时码/参考校验 | 增加第5个账本工具 |
| 版本定位 | 旧项目复现、沿用旧工作流 | 日常使用的默认选择 | 状态流程试用、反馈与迭代 |

**第一次使用，建议选 v1.6.0；需要试用结构化状态记录与局部返修流程时，再选择 v2.0.0-beta.1。**

项目版本号与视频模型版本号独立：**创梦 v2.0 不等于 Seedance 2.0**，社区版也不与私有 Pro 版按版本号逐项对齐。

- [v1.6.0 发布与安装包](https://github.com/bedelltracietony26477-create/seedance-director-community/releases/tag/v1.6.0)
- [v2.0.0-beta.1 发布与安装包](https://github.com/bedelltracietony26477-create/seedance-director-community/releases/tag/v2.0.0-beta.1)
- [v2.0 预览分支](https://github.com/bedelltracietony26477-create/seedance-director-community/tree/preview/v2.0)
- [v1.5.5 历史版本](https://github.com/bedelltracietony26477-create/seedance-director-community/releases/tag/v1.5.5)

## v1.5.5 历史版说明

v1.5.5 已有原台词硬锁、轻量对白编舞、Reaction Ownership、Failed Action、空间摄影、逐镜参考绑定和基础跨段交接。原安装标识为 `seedance-director-community`，原附件为 `Seedance_Director_Community_v1.5.5.zip`。

[查看 v1.5.5 详细说明](https://github.com/bedelltracietony26477-create/seedance-director-community/blob/main/docs/releases/v1.5.5.md) · [历史发布与下载](https://github.com/bedelltracietony26477-create/seedance-director-community/releases/tag/v1.5.5)

历史版保留原内容与使用方式；上文三版本对照列出新增规则，使用旧包时请以旧版文档和参数为准。旧名与新名不同可能导致两版同时安装，需在平台中明确选择当前使用版本。

## 从剧本到执行提示词

| 阶段 | 需要明确的内容 |
|---|---|
| 1. 读完指定范围 | 场次、人物关系、原台词、动作事件、信息揭示；材料缺失时说明实际读取范围 |
| 2. 定情绪与动作 | 情绪起点、升级、爆点、峰值、回落、收尾；补清动作过程，不新增剧情事实 |
| 3. 建立空间 | 固定场景锚点、座位、身体方向、视线、道具、行动路径和 180° 轴线 |
| 4. 分段与计时 | 按戏剧变化切段，核算对白、气口、动作、反应和可重叠时间 |
| 5. 编排逐镜执行 | 决定每镜主体、景别、前后景、表演、运镜、声音和切点 |
| 6. 检查与交接 | 对照原文，检查时间轴、参考绑定、动作相位及相邻段状态；只修出错变量 |

处理整集时，先建立完整分段总表，再输出全部分段。只改单段时缩小工作范围，保留未授权修改的原台词、参考映射与最终落点。

## 核心导演规则

### 原台词与声音事件

原台词按原人物、原字、原标点、原顺序组织，不靠删词或加速念词塞进时长。台词只在执行时间轴发声一次；源剧本确实重复的台词仍按原文保留。

长句可以按连续原文拆到相邻镜头中，串接后必须还原完整原句。**Cut ≠ Voice Reset**：切到听者时，说话者可保持同场 O.S.；重新入画后从当前发声位置接续口型。

默认对白使用 `{}`、音效使用 `<>`；默认无字幕、无背景音乐、无额外旁白。原剧本已有 VO/旁白或用户明确指定时按要求保留。

### 镜头里真正能看到什么

每镜写清景别、主体、实际入画者、前景与后景，以及当前景别可见的表演。没有人物遮挡时直接写清，不凭空加肩膀、人头或画外人物。

单人镜头的眼线使用“镜头右侧画外、略高于镜头”等具体方向。多人镜头可以描述入画人物之间的相互看向。面部特写不承担桌下脚步等不可见动作，需要时切到合适景别。

### 动作有过程，剪辑接得上

关键动作按**起势 → 发力/路径 → 接触 → 结果 → 落点**展开，同时发生的动作注明重叠时段。跨镜保留当前动作相位，避免重新起手或重复完成同一个事件。

未完成动作也有连续性：伸手、欲起身、欲离开等动作被打断后，要保留停在半程的姿态与后果。情绪通过呼吸、手指、喉部、重心或身体控制表现，表演不能干扰台词自然发声。

### 空间先成立，再决定摄影机

固定场景锚点负责真实位置，例如“桌左椅”；镜头左/右负责当前画面构图。正反打可能改变屏幕左右，不能据此让人物无故换座。

明显走位要有路径；换边需要可见越轴、轴上镜或重新建立空间。每镜保留一个主要注意中心和一个主要运镜，切镜应带来新信息、动作阶段、反应或注意目标。

### 参考素材集中绑定

每个独立分段都保留参考表，仅列真实提供且本段使用的人物、场景方向、关键道具和声音素材。默认所有 `@` 集中在参考表，镜头正文使用语义名称。

未指定编号时，图片与音频分别从 `@[图片1]`、`@[音频1]` 连续编号；用户已有明确编号时服从其设置。没有参考素材时明确说明，不能补造编号。逐镜 `@` 调用作为用户明确要求时的兼容策略保留。

## 最终会得到什么？

默认每个分段使用以下八个模块：

| 模块 | 用途 |
|---|---|
| `[声画硬锁]` | 画幅、时段、场景与发声规则 |
| `[参考图 / 音频对应表]` | 本段素材身份与本地编号；缺失素材如实说明 |
| `[本段任务]` | 唯一戏剧变化、情绪起终点、段长与必要气口/动作重叠 |
| `[人物状态、站位、轴线与群像]` | 完整进入状态、座位、朝向、手位、道具与行动路径 |
| `[风格、光影与氛围]` | 实际光源、方向、冷暖、材质与景深层级 |
| `[镜头时间轴]` | 各镜头时间码、景别、构图、动作、表演、原台词、单次声音与切点 |
| `[声音与剪辑]` | 持续底噪、空间处理、对白跨镜与声桥 |
| `[连续性底线]` | 完整退出状态及下一段需要继承的物理和情绪状态 |

用户明确要求简洁时可用四模块快速版：`[STYLELOCK]`、`[REFERENCE]`、`[SHOT]`、`[BEATS]`。快速版压缩呈现，仍需保留原台词、必要动作、空间与退出状态。

[查看八模块完整示例](examples/full-prompt.txt) · [查看快速版示例](examples/quick-prompt.txt) · [输出契约](references/final-output-contract.md)

## 一个动作如何写得更可执行？

以下用两个动作说明如何补清可见过程：

| 简略动作 | 补清可见过程 |
|---|---|
| “甲放下笔，抬眼看向乙。” | 手部局部：右手仍握笔，笔身连续下降并接触桌面；手指保持压住笔。随后切甲单人近景，从低位视线接入，抬眼至镜头右侧画外。笔不重新拿起，坐姿不变。 |
| “乙想伸手，最后收回。” | 先建立手的起点；向明确方向伸出，未接触前停在半程；沿可见路径收回并落定。下一镜从收回后的状态开始。 |

补充的范围是已有事件的动作路径、接触和衔接；人物为何行动、掌握什么信息，仍需以原剧本为依据。

## 安装与第一次使用

### 1. 选择并下载版本

从 Release 下载对应安装包：

- 稳定版：`Chuangmeng_Director_Skills_v1.6.0.zip`
- 预览版：`Chuangmeng_Director_Skills_v2.0.0-beta.1.zip`

解压后入口为 `chuangmeng-director/SKILL.md`。按你所用平台的 Agent Skills 安装方式导入该目录；如平台支持直接导入 ZIP，按其说明操作。

两个版本使用相同安装标识 `chuangmeng-director`，切换版本时只保留一个，避免互相遮盖。旧名 `seedance-director-community` 在指令中作为自然语言兼容别名识别；平台的技能选择器仍应使用新安装标识。

### 2. 准备输入

| 输入 | 建议提供的内容 |
|---|---|
| 剧本 | 完整目标集或明确选段，包含原台词和动作描述 |
| 生成参数 | 实际目标模型、平台当前时长上限、画幅与媒介 |
| 视觉参考 | 已有人物、场景主/反打、关键道具或站位图；没有时也可按文字执行 |
| 连续性信息 | 改单段或续接时，提供前段退出、后段进入及已确定的状态 |
| 本次要求 | 完整版/简洁版、节奏、镜头偏好与允许修改的范围 |

### 3. 复制启动指令

```text
使用 创梦 导演skills（$chuangmeng-director）。

目标模型：[填写实际模型]
平台当前支持的单段时长上限：[填写]
画幅与媒介：[例如16:9，真人写实 / 3D动画]
处理范围：[整集 / 场次 / 指定选段]

完整读取指定范围，保留原剧情、原台词、标点和顺序。
先梳理情绪曲线、导演版动作和场景空间，再给完整分段总表与全部提示词。
每段为整数秒，默认单镜2–4秒且不超过4秒；超时继续拆段。
单人镜头明确实际入画者、前后景及相对镜头的眼线。
连续动作写清相位与重叠窗口，台词跨镜保持同一次发声事件。
参考素材集中在对应表绑定，每段完整重建进入和退出状态。
默认输出八模块完整版。

剧本：[粘贴完整内容]
参考与已有状态：[补充素材及连续性信息]
```

[快速启动指令](examples/QUICK_START_PROMPT_CN.md) · [制作启动指令](examples/ADVANCED_STARTER_PROMPT_CN.md)

## 时长与模型适配

项目提供以下时长工作档，实际分段以目标平台当前支持的上限为准：

| 工作档 | 分段范围 | 说明 |
|---|---|---|
| Seedance 2.0 档 | 8–15 秒 | 超出已确认上限时继续拆分 |
| Seedance 2.5 档 | 16–30 秒 | 必要时可用 15 秒边界段；长段维持一个主要戏剧目标 |
| 局部补拍 | 按用户要求 | 4秒、6秒等短补拍不强行凑到默认下限 |

实际执行以用户界面或官方规格当前支持的上限为准。确认平台支持长段时，可优先安排 20–25 秒，最长不超过实际能力与 30 秒。

**单镜时长与单段时长是两回事**：一个 24 秒分段可以由多个 2–4 秒镜头组成。用户明确要求长镜头时可调整默认上限。时间码按 0.1 秒规划，用于组织动作、发声与剪辑点。

## v2.0 预览：轻量状态账本

v2.0 将原文事实、导演版动作、场景状态与逐镜事件分层处理。工作流依据账本重建各段完整提示词；审计脚本检查账本字段与状态交接，导演据此组织各段执行内容。

| 状态类别 | 记录内容 |
|---|---|
| 人物身体 | 固定位置、坐/站姿、身体方向、眼线、左右手与动作相位 |
| 关键道具 | 持有人、持有手、位置、朝向和功能状态 |
| 情绪与信息 | 当前情绪、已经获得的事实ID |
| 镜头事件 | 哪一镜发生什么变化、变化前值与变化后值 |
| 分段接口 | 完整 `entry` 和 `exit`，用于相邻段交接 |

账本审计的两条核心关系：

```text
本段 entry + 按时间排序的镜头 changes = 本段声明的 exit
上一段 exit = 下一段 entry
```

下一段的首动作变化发生在首镜事件中，不能用“首动作会改变”提前豁免入口不一致。画外人物和未入画道具仍保留在场景账本中。

**当前 beta 范围为同一连续场景、固定角色与道具集合。** 新场景、新增实体或明确时间跳跃需另建账本。

[状态流程与返修指南](https://github.com/bedelltracietony26477-create/seedance-director-community/blob/preview/v2.0/references/community-state-workflow.md) · [可运行账本](https://github.com/bedelltracietony26477-create/seedance-director-community/blob/preview/v2.0/examples/state-ledger.json)

## 审计工具与使用示例

所有审计脚本使用 **Python 标准库**。使用 Skill 生成提示词不以运行 Python 为前提；脚本用于进一步检查结构与显式状态。

| 工具 | 版本 | 检查范围 |
|---|---|---|
| `dialogue_timing.py` | 两版 | 估算中文对白、标点停顿、气口与反应时长 |
| `segment_timing_audit.py` | 两版 | 分段时长档、容量与相关节拍配置 |
| `prompt_audit.py` | 两版 | 单段模块、参考编号、对白原文、镜头时间码与上限 |
| `continuity_audit.py` | 两版 | 基础人物/道具状态与相邻段交接 |
| `state_ledger_audit.py` | 仅 2.0 预览版 | 账本字段、镜头事件回放、退出结果与跨段入口一致性 |

在安装包解压后的 `chuangmeng-director/` 或对应版本的仓库源码根目录，可运行：

```bash
python3 scripts/dialogue_timing.py --text '我不会再退了。' --mode restrained --format json
python3 scripts/prompt_audit.py examples/full-prompt.txt --dialogue-json examples/dialogue.json --format json
python3 scripts/segment_timing_audit.py examples/segments-seedance2.0.json --format json
python3 scripts/continuity_audit.py examples/continuity.json --format json
```

仅在 **2.0 预览版**目录运行状态账本检查：

```bash
python3 scripts/state_ledger_audit.py examples/state-ledger.json --format json
```

`prompt_audit.py` 一次接收一个执行分段。期望台词列表应对应该段的实际发声范围；连续一句可拆成相邻镜头子串，不能跨事件重排。要求逐镜参考调用时加 `--reference-policy shot`；明确要求长镜时用 `--max-shot-seconds` 设置对应上限。

## 适用场景与社区版范围

适合完整单集、单场戏、多人物对白、情绪冲突、连续动作、局部补拍，以及需要跨段衔接的叙事影像提示词制作。可以指定真人、动画等媒介，具体风格与资产应由剧本、参考和用户要求确定。

社区版保持可读、可修改、可复用。v2.0 的轻量账本是独立社区实现，不包含私有 Pro 的高级角色表演签名、完整道具语义状态机、量化画面预算或高级声音身份系统。

## 示例、文档与反馈

- [Skill 入口](SKILL.md)
- [完整执行示例](examples/full-prompt.txt) / [快速版示例](examples/quick-prompt.txt)
- [逐镜执行规则](references/shot-execution.md) / [输出契约](references/final-output-contract.md)
- [版本记录](https://github.com/bedelltracietony26477-create/seedance-director-community/blob/main/CHANGELOG.md) / [2.0 预览版记录](https://github.com/bedelltracietony26477-create/seedance-director-community/blob/preview/v2.0/CHANGELOG.md)
- [贡献说明](https://github.com/bedelltracietony26477-create/seedance-director-community/blob/main/CONTRIBUTING.md) / [提交问题](https://github.com/bedelltracietony26477-create/seedance-director-community/issues)

欢迎提供可复现的提示词、审计误报与生成失败描述。反馈时请写明版本、目标模型和时长上限、预期行为、实际现象及最小复现材料；仅提交你有权公开的素材，并移除个人信息。

## 许可与署名

| 内容 | 许可 |
|---|---|
| 程序代码 | MIT，见 [LICENSE-CODE](LICENSE-CODE) |
| Skill 指令、方法论、文档与文字示例 | CC BY 4.0，见 [LICENSE-DOCS](LICENSE-DOCS) |

保留作者署名 **LERler-Q**，前身项目为 **CineWeaver Director Engine**。再分发或修改时按相应许可证要求署名、链接许可并说明修改。

本项目为独立、非官方社区项目，与 ByteDance / Seedance 团队不存在隶属、赞助或官方背书关系。第三方模型名、产品名与商标归其权利人所有。
