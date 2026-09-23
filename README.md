# Seedance Director Community v1.5.5

> 面向 AI 短剧生产的开源导演 Skill：把剧本转化为可执行、可审计、可跨段衔接的 Seedance 2.0 / 2.5 视频提示词。

**非官方社区项目。** 本项目与 ByteDance、Seedance 团队不存在隶属、赞助或官方背书关系。

[English README](README_EN.md)

## 为什么做这个项目

很多 AI 视频提示词只解决“画面描述”，但短剧真正难的是：原台词不能丢、人物不能站桩、反应镜头要拍对人、动作必须有起点与落点、参考图不能错绑、连续分段还要能接得上。

Seedance Director Community 把这些问题整理成一个可复用的导演工作流，并附带 4 个零第三方依赖的 Python 审计脚本。

## 核心能力

- 原台词逐字硬锁与对白时长估算
- Seedance 2.0：8–15 秒短段
- Seedance 2.5：16–30 秒长段，可在合理情况下使用 15 秒边界段
- Dialogue Beat Map：长对白按语义节拍推进，而不是一镜念到底
- Reaction Ownership：关键台词优先拍真正被改变的人
- Failed Action：把“想做但没做完”的动作变成戏剧张力
- Blocking、眼线、180°轴线与基础跨段连续性
- 人物 / 场景方向 / 关键道具 / 音频的轻量参考绑定
- 焦段、机位、镜头运动、声音与剪辑设计
- 生成前后的结构化质量审计

## 模型时长档

| 目标模型 | 标准分段 | 推荐用途 |
|---|---:|---|
| Seedance 2.0 | 8–15 秒 | 高密度短剧、快速冲突、单一动作或对白推进 |
| Seedance 2.5 | 16–30 秒 | 长对白、连续调度、复杂对抗、2–4 个内部微节拍 |

2.5 的长段不是把两个 15 秒段机械拼起来。单段必须维持一个主要戏剧目标，并在内部完成建立、升级、冲击、余震中的连续推进。

## Community 版的边界

V1.5.5 是一个完整可用的开源版本，但有意保持轻量。它不包含更重型的角色表演签名、完整道具语义状态机、Semantic ID 资产层、量化 Screen Attention Budget 或高级 Voice State。

## 安装

### 方式一：作为 ChatGPT Skill 使用

下载 Release 中的 `Seedance_Director_Community_v1.5.5.zip`，通过支持 Skills 的环境导入。Skill 入口文件是仓库根目录的 `SKILL.md`。

### 方式二：直接阅读 / 二次开发

克隆仓库后，核心目录如下：

```text
.
├── SKILL.md
├── agents/
├── assets/
├── references/
├── scripts/
├── examples/
└── tests/
```

## 快速使用

可以直接这样请求：

```text
使用 Seedance Director Community 分析下面这场戏。
目标模型：Seedance 2.5。
保留全部原台词，重新估算时长，并输出可直接复制的完整版分段提示词。
```

如果没有指定模型，Skill 默认使用 Seedance 2.0 的 8–15 秒档。

## 审计工具

所有脚本仅依赖 Python 标准库。

```bash
python3 scripts/dialogue_timing.py --text '我不会再退了。' --mode restrained --format markdown
python3 scripts/segment_timing_audit.py examples/segments-seedance2.0.json --format markdown
python3 scripts/segment_timing_audit.py examples/segments-seedance2.5.json --format markdown
python3 scripts/prompt_audit.py examples/quick-prompt.txt --contract quick --format markdown
python3 scripts/continuity_audit.py examples/continuity.json --format markdown
```

## 设计原则

1. 先读懂戏，再设计镜头。
2. 台词不改，节拍可以重新组织。
3. 关键台词不一定拍说话者，要判断谁真正被改变。
4. 动作要写“意图 → 启动 → 接触 / 中断 → 结果”。
5. 每个独立分段都必须能单独执行。
6. 参考素材按分段本地编号，避免跨段错绑。
7. 时长服从模型能力和戏剧边界，而不是为了凑秒数。

## 项目结构

- `SKILL.md`：核心控制面与触发说明
- `references/`：导演方法、时长档、对白编舞、摄影、表演、连续性等规则
- `scripts/`：对白、分段、Prompt、连续性审计
- `examples/`：可运行示例
- `tests/`：Smoke tests
- `.github/workflows/ci.yml`：自动编译与审计测试

## 版本

当前开源版本：**v1.5.5 Community**。

版本变化见 [CHANGELOG.md](CHANGELOG.md)。

## 贡献

欢迎提交 Issue 和 Pull Request。请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。重点欢迎：

- 不同短剧类型的可复现实例
- Seedance 2.0 / 2.5 的失败案例与修复规则
- 审计脚本误报 / 漏报修复
- 更清晰的参考绑定与连续性规则
- 中英文文档改进

## License

本项目采用双许可：

- `scripts/` 与程序代码：MIT License，见 [LICENSE-CODE](LICENSE-CODE)
- `SKILL.md`、`references/`、README、示例文字与方法论：CC BY 4.0，见 [LICENSE-DOCS](LICENSE-DOCS)

第三方商标、产品名与模型名归各自权利人所有。
