# Changelog

## 1.6.1 Pro — 2026-11-04

- 开源现有Pro V1.6完整技能包，替换默认分支的社区版内容。
- 完整保留角色表演签名、道具语义状态、声音身份、画面预算、逐镜绑定和4个原版审计脚本。
- 新安装标识chuangmeng-director-pro，新增文件来源校验清单及Pro格式示例。
- v1.6.0社区历史发行保留；v2.0.0-beta.1保持原状。


## 1.6.0 — 2026-11-04

- 更名为创梦 导演skills，安装名 chuangmeng-director，保留旧触发名兼容说明。
- 新增逐镜可见性、镜头相对眼线、动作相位和声画连续规则。
- 默认单镜4秒上限、总段整数秒与严格时间码闭合审计。
- 参考表集中绑定为默认，逐镜绑定作为兼容选项。
- 修复源剧本重复台词误报，支持同一对白事件按相邻镜头子串分配。
- 提供新版启动指令、完整示例、标准库回归测试与版本化打包发布。
- 状态架构在独立 v2.0.0-beta.1 分支预览；未声称视频生成质量验证。


All notable changes to the open-source Community edition are documented here.

## [1.5.5] - 2026-09-22

### Added
- Seedance 2.5 duration profile with 16–30 second standard segments.
- Optional justified 15-second boundary segment for Seedance 2.5.
- Model-aware segmentation rules for Seedance 2.0 and 2.5.
- Dialogue Beat Map Lite.
- Reaction Ownership.
- Failed Action staging.
- Keyword visual landing.
- Lightweight reference binding for characters, scene directions, key props and audio.
- Model-aware segment timing audit.
- Examples, smoke tests and GitHub Actions CI for the open-source repository.

### Preserved
- Exact original-dialogue lock.
- Blocking, eyelines and 180-degree axis continuity.
- Cinematic camera grammar and physical action chains.
- Sound, editing and visual-impact rules from the V1.5 lineage.

### Intentionally out of scope
- Character Performance Signature.
- Full semantic prop-state machine.
- Semantic ID asset mapping.
- Quantitative Screen Attention Budget.
- Advanced Voice Identity State.
