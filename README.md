# 创梦 导演skills

**把完整剧本转成可独立生成、剪辑后连续成戏的 AI 视频分段提示词。**

前身：CineWeaver Director Engine / Seedance Director Community。Created & maintained by **LERler-Q**。

| 版本 | 定位 | 获取 |
|---|---|---|
| **v1.6.0** | 社区稳定版：逐镜可见性、眼线、动作与声画连续 | [发布与下载](../../releases/tag/v1.6.0) |
| **v2.0.0-beta.1** | 预览版：导演版剧本前置、轻量状态账本与局部返修 | [预览源码](../../tree/preview/v2.0) · [发布与下载](../../releases/tag/v2.0.0-beta.1) |
| v1.5.5 | 历史社区版 | [旧版下载](../../releases/tag/v1.5.5) |

当前默认分支是 v1.6.0。2.0 预览版单独维护，尚未经实际生成视频对照验证。项目版本号与 Seedance 等视频模型的版本号无关。

## 开始使用

1. 从对应 Release 下载 `Chuangmeng_Director_Skills_v版本号.zip`。
2. 解压后将 `chuangmeng-director/` 导入支持 Agent Skills 的环境，入口为 `SKILL.md`。不同平台导入方式以平台说明为准。
3. 粘贴完整剧本、已有参考，以及目标模型当前支持的时长上限。

```text
使用 创梦 导演skills（$chuangmeng-director）。
保留全部原台词与剧情，先梳理情绪、动作和空间，再输出全部分段提示词。
默认单镜不超过4秒；单人镜头明确前后景和相对镜头的眼线。
动作相位接续，台词跨镜连续，每段独立可用。
目标模型及平台上限：[填写实际参数]
剧本：[粘贴完整内容]
```

旧名 `seedance-director-community` 在指令中作为兼容别名识别；Skill 元数据使用新名 `chuangmeng-director`。迁移时只安装一个版本，避免同名版本互相遮盖。无需同时安装稳定版和预览版。

## v1.6.0 改善什么

- **每镜拍到什么**：主体、前后景、入画人物与当前景别能看到的动作。
- **单人眼线**：用镜头左/右、画外及高度说明方向；固定场景锚点维持跨机位空间。
- **动作衔接**：起势、路径、接触、结果与落点；同步动作写出重叠时段。
- **对白连续**：原文逐字逐序，一句跨镜不重启；真实重复台词保留。
- **短镜节奏**：默认2–4秒一个镜头，整段整数秒，支持用户明确指定的补拍或长镜。
- **参考绑定**：默认集中于参考表；兼容旧式逐镜调用。

入口规则和脚本可检查提示词文本；它们无法保证视频模型遵守所有指令，也不能用结构测试代替成片审片。

## 时长配置

沿用项目配置：Seedance 2.0 档8–15秒，Seedance 2.5 档16–30秒，后者可用15秒边界段。**这是工作流配置，实际执行以目标平台当前支持能力为准**。局部4秒/6秒补拍按用户要求执行。对白、动作和气口容纳不下时继续拆段。

## 工具与验证

Python 标准库即可运行，无需接入视频生成服务：

```bash
python3 tests/smoke_test.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/prompt_audit.py examples/full-prompt.txt --dialogue-json examples/dialogue.json --format json
python3 scripts/dialogue_timing.py --text '我不会再退了。' --mode restrained --format json
python3 scripts/continuity_audit.py examples/continuity.json --format json
```

`prompt_audit.py` 每次检查一个执行分段，默认参考表集中绑定、单镜上限4秒；用户要求逐镜@时加 `--reference-policy shot`，要求长镜时设置 `--max-shot-seconds`。计时结果是估算，语义空间和物理动作仍需复核。

[快速启动](examples/QUICK_START_PROMPT_CN.md) · [完整示例](examples/full-prompt.txt) · [版本记录](CHANGELOG.md) · [English](README_EN.md)

## 社区版范围

社区 v1.6 与 v2.0 使用独立社区实现。v2.0 开放轻量状态交接，不包含私有 Pro 的高级表演签名、完整道具语义状态机、量化画面预算或高级声音身份系统。社区版和 Pro 版版本号不表示能力一一对应。

欢迎提交可复现的失败片段描述、提示词与审计误报。请先阅读 [贡献说明](CONTRIBUTING.md)。提交素材前请移除无权公开的剧本、人物素材与个人信息。

## 许可与署名

程序代码：MIT，见 [LICENSE-CODE](LICENSE-CODE)。Skill 指令、方法论、文档与文字示例：CC BY 4.0，见 [LICENSE-DOCS](LICENSE-DOCS)。作者署名 **LERler-Q**；前身为 **CineWeaver Director Engine**。

本项目独立、非官方，与 ByteDance / Seedance 无隶属或官方背书关系。第三方名称与商标归其权利人。
