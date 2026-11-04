# 安装创梦 导演skills Pro

[English](#english)

## Skills CLI 安装

需要 Node.js 22.20 或更新版本。在要使用技能的项目目录打开终端：

```bash
npx skills add bedelltracietony26477-create/seedance-director-community --skill chuangmeng-director-pro
```

按提示选择目标工具和安装方式。默认安装到当前项目，技能标识为 `chuangmeng-director-pro`。

## 指定目标工具

### Codex

```bash
npx skills add bedelltracietony26477-create/seedance-director-community --skill chuangmeng-director-pro -a codex
```

### Claude Code

```bash
npx skills add bedelltracietony26477-create/seedance-director-community --skill chuangmeng-director-pro -a claude-code
```

安装后，向助手提供剧本并调用 `$chuangmeng-director-pro`。不同工具的技能选择方式以其界面为准。

## 多项目使用

添加 `-g` 安装到用户级技能目录：

```bash
npx skills add bedelltracietony26477-create/seedance-director-community --skill chuangmeng-director-pro -g
```

如需指定工具，可同时添加 `-a codex` 或 `-a claude-code`。

## 查看技能与更新

只查看仓库中可安装的技能：

```bash
npx skills add bedelltracietony26477-create/seedance-director-community --list
```

查看本项目已安装的技能：

```bash
npx skills list
```

查看用户级安装：

```bash
npx skills list -g
```

检查并更新通过 Skills CLI 安装的技能：

```bash
npx skills check
npx skills update
```

更新命令会处理 CLI 管理的已安装技能。CLI 从仓库主分支获取当前 Pro 内容；如需固定的发行版本，可使用对应 Release 的 ZIP 安装包。

## ZIP 安装

从 [v1.6.1 Pro 发布页](https://github.com/bedelltracietony26477-create/seedance-director-community/releases/tag/v1.6.1) 下载 `Chuangmeng_Director_Skills_Pro_v1.6.1.zip`。

解压后，按平台的 Agent Skills 安装方式导入 `chuangmeng-director-pro/`。入口文件为 `SKILL.md`。

## 开始制作

```text
使用 $chuangmeng-director-pro。

目标平台与单段时长上限：[填写]
画幅和媒介：[填写]
完整剧本与参考素材：[粘贴]

保留全部原台词，先梳理情绪、人物表演、对白编舞、空间、道具与声音，
再输出完整分段表、八模块提示词和连续性交接。
```

[返回项目首页](../README.md) · [完整使用示例](../examples/full-prompt.txt) · [Skills CLI 文档](https://skills.sh/docs/cli)

## English

Requires Node.js 22.20 or later. Run from your project:

```bash
npx skills add bedelltracietony26477-create/seedance-director-community --skill chuangmeng-director-pro
```

Choose your target agent when prompted. Use `-a codex` or `-a claude-code` to select one directly, and add `-g` for user-level installation across projects.

To inspect the repository without installing:

```bash
npx skills add bedelltracietony26477-create/seedance-director-community --list
```

Use `npx skills list` for project installations or `npx skills list -g` for user-level installations. Use `npx skills check` and `npx skills update` to check and update CLI-managed skills.

CLI installs use the current Pro content on the default branch. For a fixed release, download the corresponding ZIP from [Releases](https://github.com/bedelltracietony26477-create/seedance-director-community/releases/tag/v1.6.1) and import its `chuangmeng-director-pro/` folder according to your platform's instructions.

After installing, provide your script, references and production requirements, then invoke `$chuangmeng-director-pro`.

[Project overview](../README_EN.md) · [Full example](../examples/full-prompt.txt) · [Skills CLI documentation](https://skills.sh/docs/cli)
