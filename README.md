<div align="center">

<img src="assets/icon.svg" width="92" alt="CineWeaver Director Engine" />

# CineWeaver Director Engine

### AI can generate shots. CineWeaver directs the scene.

**把完整剧本变成 AI 可以直接拍的一场戏。**

完整剧本 → 人物表演 → 对白编舞 → 场面调度 → 镜头设计 → 连续性 → Seedance 可执行提示词

**谁该入镜 · 怎么演 · 怎么站 · 什么时候切 · 下一段怎么接**

**Community v1.5.5 · Seedance 2.0 / 2.5 · Created & maintained by LERler-Q**

[⭐ **Star CineWeaver**](../../stargazers)
&nbsp;&nbsp;·&nbsp;&nbsp;
[⬇️ **Download v1.5.5**](../../releases/download/v1.5.5/Seedance_Director_Community_v1.5.5.zip)
&nbsp;&nbsp;·&nbsp;&nbsp;
[📦 **Release**](../../releases/tag/v1.5.5)
&nbsp;&nbsp;·&nbsp;&nbsp;
[English](README_EN.md)

<br>

![Release](https://img.shields.io/badge/release-v1.5.5-blue)
[![CI](../../actions/workflows/ci.yml/badge.svg)](../../actions/workflows/ci.yml)
![Seedance](https://img.shields.io/badge/Seedance-2.0%20%7C%202.5-black)
![Python](https://img.shields.io/badge/Python-standard%20library%20only-blue)
![License](https://img.shields.io/badge/license-MIT%20%2B%20CC%20BY%204.0-green)

</div>

---

## 为什么需要 CineWeaver？

AI 视频模型已经越来越会生成漂亮画面。

但**会生成画面，不等于会导演一场戏。**

你很可能遇到过这些问题：

- **谁说话就拍谁**：真正被一句话击中的人，反而没有反应镜头。
- **长对白像站桩念词**：一个近景从头念到尾，人物关系和权力没有变化。
- **动作突然发生**：人物没有起势、接触、中断和结果，像从一个状态瞬移到另一个状态。
- **多人戏空间混乱**：站位、视线、左右关系和 180° 轴线不断漂移。
- **跨段生成像“失忆”**：上一段手机还在右手，下一段道具、姿态或人物位置突然重置。
- **Prompt 越写越长，戏却没有变好**：描述很多，但模型不知道这一刻最重要的戏剧变化是什么。

**CineWeaver 解决的不是“怎么把 Prompt 写得更长”。**

它解决的是：

> **这一刻到底该拍谁？人物为什么这样演？摄影机为什么现在切？动作怎么发生？下一段从什么状态继续？**

---

## Without CineWeaver / With CineWeaver

| 导演问题 | 普通 Prompt 常见结果 | CineWeaver |
|---|---|---|
| 一句狠话该拍谁 | 默认一直拍说话者 | 判断**谁真正被这句话改变**，把关键画面给 Reaction Owner |
| 长对白怎么拍 | 一个近景念到底 | 用 **Dialogue Beat Map** 把对白拆成信息、攻击、证据、转折、结论等视觉节拍 |
| 动作怎么发生 | “突然抓住 / 突然跪下 / 突然转身” | 写成**意图 → 启动 → 接触 / 中断 → 结果** |
| 情绪怎么表现 | 只写眼神和表情 | 把情绪落到呼吸、手、道具、喉部、重心、脚步和未完成动作 |
| 多人物怎么站 | 角色围着台词随机移动 | 先锁 Blocking、Eyeline、相对距离、前后层级和 180° 轴线 |
| 多段怎么接 | 每段都像重新开机 | 用 Entry / Exit State 继承人物、道具、动作和空间状态 |
| 参考素材怎么绑定 | 图越多越容易错绑 | 人物、场景方向、关键道具、音频按**独立分段本地绑定** |
| 2.0 / 2.5 怎么分段 | 同一套时长逻辑 | 根据模型能力使用不同 Duration Profile |

### 一句话理解

**普通 Prompt 主要描述“画面里有什么”。**

**CineWeaver 先决定“这场戏应该怎么演、怎么拍”，再生成 Prompt。**

---

## 它怎么工作？

~~~text
FULL SCRIPT
    ↓
Story / Conflict / Power
    ↓
Performance Direction
    ↓
Dialogue Choreography
    ↓
Blocking & Eyelines
    ↓
Camera Direction
    ↓
Reference Binding
    ↓
Continuity
    ↓
Audit
    ↓
SEEDANCE 2.0 / 2.5 PROMPTS
~~~

目标不是把所有专业术语塞进提示词。

目标是让模型更明确地知道：

**谁在做什么、为什么现在发生、摄影机应该看哪里、这一段结束后下一段从哪里继续。**

---

## 2 分钟开始使用

### 1. 下载

### **[⬇️ Download CineWeaver Community v1.5.5](../../releases/download/v1.5.5/Seedance_Director_Community_v1.5.5.zip)**

导入支持 Agent Skills / Skills 的环境。

入口文件：

\`SKILL.md\`

### 2. 粘贴完整剧本

不需要先自己把剧本拆成几十条镜头 Prompt。

把完整场景、完整一集或需要修复的剧情段落直接交给 CineWeaver。

### 3. 告诉它目标模型

例如：

~~~text
使用 CineWeaver Director Engine 处理下面这场戏。

目标模型：Seedance 2.5。
保留全部原台词。
重新估算合理时长。

不要站桩式对白。
根据真正被台词改变的人设计 Reaction Shot。
保持人物、道具、眼线、轴线和动作状态连续。

输出可直接用于生成的完整版分段导演提示词。
~~~

如果不指定模型，Community v1.5.5 默认按 **Seedance 2.0** 的短段逻辑执行。

> 一行 Skills 安装命令会在 GitHub 账号完成 **LERler-Q** 品牌迁移后补上，避免现在把旧用户名重新写回文档。

---

## ⭐ 为什么值得先 Star？

如果你正在做：

- AI 短剧
- AI 漫剧
- 多人物对白
- 连续剧情
- Seedance 2.0 / 2.5
- AI 影视工作流

那么你以后大概率还会遇到同一批问题：

**站桩对白、动作断裂、镜头看错人、参考错绑、空间混乱、跨段失忆。**

CineWeaver 会持续把真实生成中的失败案例，整理成**可以复用、可以审计的导演规则**。

### **[⭐ Star CineWeaver — 把它留到下一次拿到剧本时](../..)**

Star 不只是支持项目。

它更像是把一个**“生成式视频的导演层”**先收藏起来。

---

## CineWeaver 的核心导演能力

### 👁 关键台词到底拍谁｜Reaction Ownership

关键台词不一定应该拍说话的人。

CineWeaver 会判断：

> **这一句话真正改变了谁？**

然后把最重要的画面资源交给真正承担变化的人。

---

### 🎭 长对白不站桩｜Dialogue Choreography

连续对白不会默认“一镜念到底”。

系统会按自然语义节点组织：

**称呼 → 信息 → 逼问 → 攻击 → 证据 → 转折 → 结论**

并把台词、动作、听者反应和镜头变化组织成连续视觉节拍。

---

### ✋ 没做完的动作也是表演｜Failed Action

现实表演里，很多最有力量的动作并没有真正完成。

例如：

~~~text
想跪下
→ 屈膝
→ 被一句话打断
→ 停在半蹲
→ 情绪结果

想挂电话
→ 手指靠近按钮
→ 听见关键信息
→ 手停住

想阻止
→ 抬手
→ 对方已经完成动作
→ 手悬在半空
~~~

这种“未完成状态”可以直接成为下一镜或下一段的连续性接口。

---

### 🎥 先排戏，再放摄影机｜Blocking / Eyeline / Axis

CineWeaver 会先明确：

- 谁在画面左 / 右
- 身体朝向
- 视线目标
- 人物相对距离
- 前后景层级
- 行动路径
- 180° 轴线
- 下一镜如何承接

再决定景别、焦段、机位和运动。

---

### 🔗 多段生成不再每次重启｜Continuity

每个独立分段都会建立自己的进入 / 退出状态。

重点检查：

- 人物位置
- 身体朝向
- 左右手
- 关键道具
- 动作完成度
- 视线目标
- 场景方向
- 参考绑定

这样下一段不是从“随机初始状态”重新生成。

---

### 🧩 参考素材按段绑定｜Lightweight Reference Binding

Community Edition 支持轻量绑定：

- 人物参考
- 场景参考
- 正 / 反打方向
- 关键道具
- 人物声音

每个独立生成段重新建立本地参考编号，降低长项目中的参考错绑概率。

---

## 两套模型时长逻辑

| Target | 标准分段 | 更适合 |
|---|---:|---|
| **Seedance 2.0** | **8–15 秒** | 高频短剧、单一冲突、快速对白、紧凑动作链 |
| **Seedance 2.5** | **16–30 秒** | 长对白、连续调度、多阶段动作、复杂关系对抗 |

### Seedance 2.0

优先保证：

- 单段目标清晰
- 高频信息推进
- 镜头切换紧凑
- 超过 15 秒继续拆段

### Seedance 2.5

长段不是把两个 15 秒 Prompt 粘起来。

20 秒以上段落需要维持**一个主要戏剧目标**，内部形成约 **2–4 个连续 microbeats**：

~~~text
建立 → 升级 → 冲击 → 余震
~~~

剧情边界合理时允许约 15 秒边界段。

---

## 不只是生成 Prompt，还会审计 Prompt

CineWeaver 附带 4 个**零第三方依赖**的 Python 工具：

| Tool | 用途 |
|---|---|
| \`dialogue_timing.py\` | 估算对白时长与表演余量 |
| \`segment_timing_audit.py\` | 检查 2.0 / 2.5 分段容量和时长规则 |
| \`prompt_audit.py\` | 检查输出模块、参考调用和 Prompt 契约 |
| \`continuity_audit.py\` | 检查相邻分段人物 / 道具基础连续性 |

快速测试：

~~~bash
python3 scripts/dialogue_timing.py --text '我不会再退了。' --mode restrained --format markdown
python3 scripts/segment_timing_audit.py examples/segments-seedance2.0.json --format markdown
python3 scripts/segment_timing_audit.py examples/segments-seedance2.5.json --format markdown
python3 scripts/prompt_audit.py examples/quick-prompt.txt --contract quick --format markdown
python3 scripts/continuity_audit.py examples/continuity.json --format markdown
~~~

所有审计脚本仅使用 Python 标准库。

---

## 它适合谁？

CineWeaver 更适合：

- AI 短剧导演 / 制作人
- Seedance 视频创作者
- AI 分镜与提示词工程师
- 多人物、长对白、动作或情绪戏
- 需要连续处理多个剧情段落的工作流
- 正在搭建 AI 影视生产 Pipeline 的开发者

如果你只需要生成一张漂亮画面，它可能有些重。

如果你需要**连续拍一场戏**，它才开始体现价值。

---

## Community v1.5.5 包含什么？

~~~text
.
├── SKILL.md
├── agents/
├── assets/
├── references/
├── scripts/
├── examples/
├── tests/
└── .github/
~~~

核心规则包括：

- Exact Dialogue Lock
- Dialogue Beat Map Lite
- Reaction Ownership
- Failed Action
- Short-drama Visual Impact
- Blocking / Eyeline / Axis
- Emotion & Physical Performance
- Camera Grammar
- Seedance 2.0 / 2.5 Duration Profiles
- Lightweight Reference Binding
- Crowd / Sound / Editing
- Quality Gates
- Final Output Contract

---

## Community Edition 的边界

v1.5.5 是一套**完整可用**的开源导演工作流，同时有意保持轻量。

当前 Community Edition 不包含更重型的高级状态系统，例如：

- Character Performance Signature
- Full Semantic Prop State Machine
- Semantic ID Asset Layer
- Quantitative Screen Attention Budget
- Advanced Voice Identity State

这样可以让 Community 版保持更容易理解、修改和二次开发。

---

## 使用入口

- [⚡ Quick Start Prompt｜快速启动提示词](examples/QUICK_START_PROMPT_CN.md)
- [🎬 Advanced Starter Prompt｜专业导演启动提示词](examples/ADVANCED_STARTER_PROMPT_CN.md)
- [📦 Changelog](CHANGELOG.md)
- [🤝 Contributing](CONTRIBUTING.md)

---

## Contributing

尤其欢迎：

- Seedance 2.0 / 2.5 的真实失败案例
- 不同短剧类型的可复现实例
- 审计脚本误报 / 漏报修复
- Blocking / Reference Binding / Continuity 改进
- 中英文文档改进

贡献前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 加入 CineWeaver 社区

如果你正在做 AI 短剧、Seedance、AI 视频导演或提示词工作流，欢迎加入 CineWeaver 社区，一起交流真实生成案例、失败修复、导演方法和工作流迭代。

<div align="center">

<img src="assets/community-qr.png" width="260" alt="CineWeaver Community QR Code" />

**扫码加入 AI 视频制作交流群**

二维码如已过期，请添加微信：**LERler-Q**  
添加时可备注：**CineWeaver / AI视频**

</div>

---

## License

本项目采用双许可：

- **程序代码**（\`scripts/\`、\`tests/\` 等）：MIT License，见 [LICENSE-CODE](LICENSE-CODE)
- **Skill 指令 / 方法论 / 文档 / 文字示例**：CC BY 4.0，见 [LICENSE-DOCS](LICENSE-DOCS)

第三方商标、产品名与模型名归各自权利人所有。

---

## Disclaimer

**CineWeaver Director Engine 是独立的非官方社区项目。**

本项目与 ByteDance、Seedance 团队不存在隶属、赞助或官方背书关系。

---

<div align="center">

### CineWeaver Director Engine

**AI can generate shots. CineWeaver directs the scene.**

[⭐ **Star**](../..)
·
[⬇️ **Download**](../../releases/latest)
·
[🐛 **Report an Issue**](../../issues)

**Created & maintained by LERler-Q**

</div>
