# 创梦 导演skills Pro · Chuangmeng Director Skills

**Direct performance, action, dialogue and continuity from script to shot.**

An open-source directing Skill for AI filmmakers. Start with a complete script and available references, then organize character objectives, emotion, space and physical action into segmented video prompts.

Use it for short dramas, dialogue scenes, emotional confrontations, connected action and local pickups.

**v1.6.1 Pro · By LERler-Q**

[Download Pro](../../releases/tag/v1.6.1) · [中文](README.md) · [Example](examples/full-prompt.txt) · [Skill entry](SKILL.md)

## Choose a version

| Version | Main capabilities | Get it |
|---|---|---|
| **v1.6.1 Pro** | Performance, dialogue choreography, shot-level references and character/prop/voice continuity | [Download Pro](../../releases/tag/v1.6.1) |
| v2.0.0-beta.1 Community | Lightweight state ledger, shot-event records and local repair workflow | [Explore the preview](../../releases/tag/v2.0.0-beta.1) |
| v1.6.0 Community | Shot visibility, connected action, eyelines and sound continuity | [Download Community](../../releases/tag/v1.6.0) |
| v1.5.5 Community | Lightweight dialogue choreography, references and basic handoffs | [Learn more](docs/releases/v1.5.5.md) · [Download](../../releases/tag/v1.5.5) |

Choose Pro for coordinated performance, props, voices and shot direction. Community offers lighter workflows; the v2 preview introduces structured state records and repair.

## Direct a connected scene

**Stage the drama before choosing the camera.** Establish objectives, obstacles, strategy and power shifts, then arrange blocking, eyelines, paths and shots.

**Give characters consistent performance habits.** Performance Signatures record eye routes, breath, hand behavior and bodily control, selected by the actual stimulus and emotional intensity.

**Turn long dialogue into visible drama.** Organize semantic beats around information, pressure, evidence and reversals. Give the picture to the speaker, listener, hands, props or spatial outcome while preserving the continuous speech event.

**Connect action across cuts.** Describe preparation, force, path, contact and result. Preserve action phases, including gestures that stop halfway.

**Keep props and voices in the scene.** Track holders, hands, contact, position and function. Distinguish dialogue, phone, same-scene O.S., internal voice and narration while maintaining voice identity.

## Pro directing capabilities

| Capability | Purpose |
|---|---|
| Exact dialogue and source coverage | Preserve dialogue, order and story events within segment capacity |
| Character Performance Signature | Organize lasting performance habits and intensity variations |
| Dialogue Choreography | Coordinate speech, action, reactions and cuts |
| Reaction Ownership | Identify who carries a line's informational and emotional change |
| Failed Action | Direct interruptions and their visible consequences |
| Character Knowledge Boundary | Ground reactions in information a character has acquired |
| Screen Attention Budget | Allocate attention around strategy and power changes |
| Prop Semantic State | Track held, worn, placed and other prop relationships |
| Voice Identity State | Coordinate voice identity, mode, lip sync and sound perspective |
| Semantic ID / Reference Manifest | Maintain asset identity and local segment mappings |
| Shot-level reference binding | Call visible characters, correct scene directions, key props and voices |
| Decision Contact POV | Show decisive physical contacts such as signing or unlocking |
| Action Insert Montage | Organize related physical actions into a causal sequence |
| START_STATE / END_STATE | Connect character, prop, action, sound and knowledge states |

## Workflow

1. Read the requested script and record dialogue, action and story coverage.
2. Establish emotion, objectives, knowledge boundaries and strategy.
3. Build the director's bible, performance signatures, scenes and recurring assets.
4. Estimate dialogue, breath, reactions, action and overlap.
5. Stage positions, face direction, eyelines, props, paths and axes.
6. Bind references and direct shots, speech and editing.
7. Hand off complete entry and exit states between segments.

## Output

The full format provides eight modules: sound/picture constraints; references; dramatic task; character/blocking/face/axis state; style and lighting; shot timeline; sound/editing; continuity.

Compact tasks use `[STYLELOCK]`, `[REFERENCE]`, `[SHOT]`, `[BEATS]`.

[Full example](examples/full-prompt.txt) · [Quick example](examples/quick-prompt.txt) · [Output guide](references/final-output-contract.md)

## Quick start

1. Download the [v1.6.1 Pro package](../../releases/tag/v1.6.1).
2. Import its `chuangmeng-director-pro/` folder using your platform's Agent Skills installation instructions.
3. Supply a complete script, references, target platform and duration requirements. Invoke `$chuangmeng-director-pro`.

Entry: `SKILL.md`. Installed identifier: **`chuangmeng-director-pro`**.

```text
Use $chuangmeng-director-pro.
Target platform and maximum segment duration: [fill in]
Aspect ratio and medium: [fill in]
Scope: [episode / scene / excerpt]

Preserve original dialogue and story events.
Plan emotion, performance, dialogue, blocking, props and voices before shots.
Use performance signatures, attention budgeting, prop states and voice states.
Build each segment's reference mapping and bind assets in the actual shots.
Provide the full segment table, all eight-module prompts and continuity handoffs.

Script: [paste]
References and existing states: [provide]
```

## Reference binding

The reference table defines local numbering; each shot calls the assets actually visible or heard.

- Number image and audio references separately from `@[图片1]` and `@[音频1]`.
- Bind visible characters and the scene direction matching the camera.
- Give visible continuity props their own references; describe local props as needed.
- Call the actual voice; off-screen-only speakers use audio references.
- Maintain stable asset identities across segments and rebuild local numbering per segment.

[Reference guide](references/reference-asset-binding.md) · [Prop-state guide](references/prop-and-object-state.md)

## Duration and pacing

Standard segments default to 8–15 seconds. Use 16–30 second Extended segments when the target platform supports them and the task calls for a longer passage.

Choose shot length around dramatic changes. Connect cuts with action phases, eyelines and sound; allocate time for dialogue, breath and movement. Keep one main dramatic objective through a long segment.

[Extended mode](references/extended-segment-mode.md) · [Dialogue choreography](references/dialogue-choreography.md)

## Production tools

Four Python standard-library scripts support the workflow:

| Tool | Purpose |
|---|---|
| `dialogue_timing.py` | Estimate dialogue, breath, reactions, action and overlap |
| `segment_timing_audit.py` | Check segment capacity, coverage, impact and pacing |
| `prompt_audit.py` | Check modules, shot-level references, dialogue, camera and sound rules |
| `continuity_audit.py` | Check character, prop, voice and knowledge handoffs |

```bash
python3 scripts/dialogue_timing.py --text '我不会再退了。' --mode restrained --segment-mode standard --format json
python3 scripts/segment_timing_audit.py examples/segments-standard.json --format json
python3 scripts/prompt_audit.py examples/full-prompt.txt --dialogue-json examples/dialogue.json --format json
python3 scripts/continuity_audit.py examples/continuity.json --format json
```

## Documentation and community

[Performance signatures](references/character-performance-signatures.md) · [Camera language](references/camera-grammar-and-combinations.md) · [Changelog](CHANGELOG.md) · [Contributing](CONTRIBUTING.md) · [Issues](../../issues)

Share directing, performance, binding and continuity questions with the version, target platform, prompt excerpt and intended shot.

## Author and license

Created and maintained by **LERler-Q**. Formerly **CineWeaver Director Engine**.

Code: [MIT](LICENSE-CODE). Skill instructions, methodology, documentation and textual examples: [CC BY 4.0](LICENSE-DOCS).

Independent unofficial project. Third-party names and trademarks belong to their owners.
