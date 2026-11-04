# 创梦 导演skills Pro V1.6 · Chuangmeng Director Skills

**The complete original Pro V1.6 directing package, published as release v1.6.1.** Created and maintained by **LERler-Q**. Formerly CineWeaver Director Engine.

[Download Pro](../../releases/tag/v1.6.1) · [中文](README.md) · [Skill entry](SKILL.md)

## Releases

| Version | Edition |
|---|---|
| v1.6.1 Pro | Complete original Pro V1.6 package; current release |
| v1.6.0 Community | Historical community release |
| v2.0.0-beta.1 Community | Existing preview, unchanged |
| v1.5.5 Community | Historical lightweight release |

## Complete Pro capabilities

- Exact dialogue and source coverage; dialogue choreography and reaction ownership.
- Character Performance Signatures with trigger conditions and intensity variations.
- Failed Action, Character Knowledge Boundary and Screen Attention Budget.
- Prop Semantic State: holder, hand/contact, relation mode, position zone, orientation, functional state and continuity lifecycle.
- Voice Identity State: identity, dialogue/phone/O.S./OS/VO mode, lip sync and spatial processing.
- Stable semantic asset IDs, local Reference Binding Manifest and actual shot-level bindings.
- Decision Contact POV, Action Insert Montage and connected physical action.
- Independent START_STATE/END_STATE, Standard/Extended segmentation and continuity handoffs.

All original directing references, four audit scripts and the original icon are included. Only the skill name/title and UI installation metadata are adapted for the public project. The file-by-file source checksums and export policy are in [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json).

## Install and use

Download `Chuangmeng_Director_Skills_Pro_v1.6.1.zip`, then import its `chuangmeng-director-pro/` folder according to your platform's Agent Skills instructions. Entry: `SKILL.md`. Invoke **`$chuangmeng-director-pro`**. The original skill identifier is `direct-episode-to-seedance-prompts-pro-v1-6`; the community edition uses `chuangmeng-director`.

Provide the complete script, target platform/current duration limit, format and available references. Ask Pro to preserve dialogue, plan emotion, performance, blocking, props and voices before choosing shots, and output all segments and continuity handoffs.

Pro uses its original reference policy: the table defines local indices, and each shot binds the visible character, correct scene direction, visible continuity prop and actual voice. Off-screen-only speakers use their audio reference without forcing a character image. Local props are described in prose unless explicitly promoted to locked assets.

Standard segments default to 8–15 seconds; authorized Extended segments may use 16–30 seconds where the platform supports them. Pro retains its original pacing and timing rules; the earlier community edition's 4-second shot cap and centralized-only reference policy do not replace the Pro rules.

## Output and tools

The full contract contains eight modules for sound/picture constraints, references, dramatic task, character/blocking/face/axis state, style/light, shot timeline, sound/editing and continuity. The compact contract uses `[STYLELOCK]`, `[REFERENCE]`, `[SHOT]`, `[BEATS]`; its shot beats belong in BEATS.

[Full example](examples/full-prompt.txt) · [Quick example](examples/quick-prompt.txt) · [Original output contract](references/final-output-contract.md)

```bash
python3 scripts/dialogue_timing.py --text '我不会再退了。' --mode restrained --segment-mode standard --format json
python3 scripts/segment_timing_audit.py examples/segments-standard.json --format json
python3 scripts/prompt_audit.py examples/full-prompt.txt --dialogue-json examples/dialogue.json --format json
python3 scripts/continuity_audit.py examples/continuity.json --format json
```

The original scripts cover dialogue timing, Standard/Extended capacity, prompt/shot binding and character/prop/voice/knowledge continuity.

## License

Code: [MIT](LICENSE-CODE). Skill instructions, methodology, documentation and textual examples: [CC BY 4.0](LICENSE-DOCS). Credit **LERler-Q**, formerly CineWeaver Director Engine. Independent unofficial project; third-party names and trademarks belong to their owners.
