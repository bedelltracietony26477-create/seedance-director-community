<div align="center">

# 创梦 导演skills

### Chuangmeng Director Skills

**Turn complete scripts into cinematic AI-video prompts with clear shots, playable performances and continuous scenes.**

Exact dialogue · Shot visibility · Performance · Physical action · Blocking and eyelines · Sound continuity · Segment handoffs

**Community v1.6.0 stable / v2.0.0-beta.1 preview**

Created & maintained by **LERler-Q**

[Stable release](https://github.com/bedelltracietony26477-create/seedance-director-community/releases/tag/v1.6.0) · [v2 preview](https://github.com/bedelltracietony26477-create/seedance-director-community/releases/tag/v2.0.0-beta.1) · [中文](README.md) · [Issues](https://github.com/bedelltracietony26477-create/seedance-director-community/issues)

</div>

> **This page: v1.6.0 stable.** v2.0.0-beta.1 is maintained on a separate preview branch.

Formerly **CineWeaver Director Engine / Seedance Director Community**. The existing repository address and historical releases remain available. The installed skill identifier is now `chuangmeng-director`.

## What it does

Chuangmeng is a directing workflow for an AI assistant in an Agent Skills-compatible environment, accompanied by local Python audit tools.

Provide a script, available references and production requirements. The workflow establishes emotion, physical action and spatial blocking before organizing performance, shots, dialogue, sound and segment continuity. Its output is a set of prompts for your chosen video-generation platform.

Each segment should make clear **who the camera sees, what is visible, how the action happens, how speech continues and which state the next segment inherits**.

The project consists of **skill instructions, directing references, examples and audit scripts**. Video generation takes place on your selected platform. This repository does not include a video-generation service, automatically upload assets or call a model to render footage.

## Production problems addressed

| Common problem | Workflow approach |
|---|---|
| Long dialogue becomes a static close-up | Organize semantic beats, actions, reactions and cuts while preserving the speech event |
| A solo shot says only “looks at another character” | Specify camera-relative direction, off-screen position and eyeline height |
| A facial close-up is asked to show feet and hands | Restrict actions to the visible framing; use appropriate inserts when required |
| Connected actions become separate waiting steps | Specify preparation, path, contact, result, overlap and action phase at the cut |
| Dialogue restarts after a cut | Preserve one continuous sound event, with O.S. attribution where appropriate |
| Reverse shots cause random seat changes | Separate fixed scene anchors from the current camera's screen coordinates |
| Props change hands or seated characters start kneeling | Rebuild entry/exit states; the v2 preview adds a structured ledger |
| A long prompt leaves the actual frame unclear | State the subject, visible cast, foreground/background, action, movement and landing |

These are workflow and review objectives. Actual results still depend on the model, references, instruction execution and editing.

## Choose a release

| Capability | v1.6.0 stable | v2.0.0-beta.1 preview |
|---|---|---|
| Dialogue, punctuation and source-order preservation rules | Included | Inherited |
| Shot visibility, camera-relative eyelines and connected action | Included | Inherited |
| Default 2–4 second shots; integer segment duration | Included | Inherited |
| Centralized reference mapping; continuous speech across cuts | Included | Inherited |
| Independent prompts and entry/exit descriptions | Included | Further structured |
| Source/director-script separation | Source coverage and action supplementation | Explicit SOURCE → DIRECTOR_SCRIPT → STATE → EVENT workflow |
| State tracking | Basic character/prop handoffs | Lightweight physical, prop, action, emotion and knowledge ledger |
| Shot-event replay and strict boundary comparison | New ledger auditor not included | `state_ledger_audit.py` |
| Local repair | Targeted edits and neighboring interfaces | Additional repair routing by source, action, space, state and sound |
| Intended use | Default for everyday use | Experimentation and feedback on the state workflow |
| Existing checks | 11 regression tests + smoke checks | 23 regression tests + smoke checks |

**Start with v1.6.0. Choose the preview to try structured state tracking and the repair workflow.** Neither release has a generated-video comparison benchmark; regression tests cover text and structure.

Skill versions are independent of model versions: **Chuangmeng v2.0 is not Seedance 2.0**. Community version numbers also do not map one-to-one to private Pro capabilities.

[Stable download](https://github.com/bedelltracietony26477-create/seedance-director-community/releases/tag/v1.6.0) · [Preview download](https://github.com/bedelltracietony26477-create/seedance-director-community/releases/tag/v2.0.0-beta.1) · [Preview source](https://github.com/bedelltracietony26477-create/seedance-director-community/tree/preview/v2.0) · [Historical v1.5.5](https://github.com/bedelltracietony26477-create/seedance-director-community/releases/tag/v1.5.5)

## From script to executable prompts

| Stage | Decisions |
|---|---|
| Read the complete requested scope | Scenes, relationships, original dialogue, actions and revelations; disclose missing material |
| Establish emotion and physical action | Emotional progression and visible action processes without adding story facts |
| Establish space | Fixed anchors, seats, body direction, eyelines, props, paths and the 180° axis |
| Segment and estimate duration | Dramatic changes, dialogue, breath, action, reactions and permitted overlap |
| Direct individual shots | Subject, framing, foreground/background, performance, movement, sound and cut |
| Audit and hand off | Source coverage, timing, references, action phases and neighboring states |

For a complete episode, create the full segment table before writing all segment prompts. For a local revision, preserve dialogue, reference mappings and final landing states outside the authorized change.

## Directing principles

### Exact dialogue and continuous sound

Preserve the original speaker, words, punctuation and order. Do not delete words or force faster delivery to fit a segment. A dialogue event appears once in the execution timeline; genuinely repeated source lines remain repeated.

One sentence may be split into consecutive source substrings across neighboring shots, provided they reconstruct the original event. **Cut ≠ Voice Reset**: use same-scene O.S. over the listener, then resume the visible speaker at the current spoken position.

Use `{}` for dialogue and `<>` for effects. Default to no subtitles, no background music and no added narration. Retain source VO/narration or explicit user requirements as applicable.

### Visible shots and playable performance

Describe the subject, visible cast, framing, foreground/background and only actions that the framing can show. Do not invent a shoulder, head or off-screen character as a foreground object.

In solo shots, specify an eyeline such as “camera-right, off-screen, slightly above the lens.” Shared shots can identify visible characters looking at each other. Use an insert or wider framing when an important action would otherwise be invisible.

### Connected physical action

Organize preparation → force/path → contact → result → landing. Make overlap explicit for simultaneous actions. Continue the current action phase after a cut rather than restarting or repeating the event.

For an interrupted action, preserve its halfway state and consequence. Express emotion through visible breath, fingers, throat, balance or bodily control without making natural speech impossible.

### Space before camera

Fixed anchors such as “the chair on the left side of the desk” record physical location; screen-left/right describe the current shot. A reverse angle can alter screen coordinates without changing a character's seat.

Movement needs a visible path. Crossing the axis requires visible movement, an on-axis shot or a spatial re-establishment. Give each shot one main attention center and one main camera movement; cut for information, an action stage, a reaction or an attention shift.

### Centralized reference binding

Each independent segment retains a reference table listing only supplied assets actually used: characters, scene directions, key props and voices. By default, `@` tags appear only there; shot prose uses semantic names.

When numbering is not specified, image and audio references each start at `@[图片1]` and `@[音频1]`. Honor explicit user numbering. State missing references rather than inventing assets. Legacy shot-level tags remain available when explicitly requested.

## Output format

The full format uses these eight modules, with Chinese headings retained for compatibility with the skill and auditors:

| Module | Content |
|---|---|
| `[声画硬锁]` | Format, time, scene and speech constraints |
| `[参考图 / 音频对应表]` | Segment-local reference identities and numbering |
| `[本段任务]` | Dramatic change, emotional start/end, duration and overlap |
| `[人物状态、站位、轴线与群像]` | Complete entry state, blocking, hands, props and paths |
| `[风格、光影与氛围]` | Actual lighting sources, direction, color and material |
| `[镜头时间轴]` | Shot times, framing, action, performance, dialogue, one-off sounds and cuts |
| `[声音与剪辑]` | Continuous ambience, sound perspective, speech bridges and editing |
| `[连续性底线]` | Complete exit state and physical/emotional handoff |

When explicitly requested, the compact format uses `[STYLELOCK]`, `[REFERENCE]`, `[SHOT]`, `[BEATS]`. It compresses presentation while retaining dialogue, essential action, space and exit states.

[Full example](examples/full-prompt.txt) · [Quick example](examples/quick-prompt.txt) · [Output contract](references/final-output-contract.md)

## Example of clearer action direction

This illustrates action wording only; it is not a complete prompt or a generated-video comparison.

| Brief source action | Visible execution |
|---|---|
| “A puts down the pen and looks up at B.” | Hand insert: the held pen descends continuously to the desk; fingers remain pressing it. Cut to A alone, entering with the same lowered gaze and raising the eyeline camera-right off-screen. Do not pick up the pen again or change the seated posture. |
| “B starts to reach, then withdraws.” | Establish the hand's initial position, the reach direction, the interruption before contact, the return path and the final rest position. Continue from that result in the next shot. |

Supplement the physical process, not the story facts. Motivation and knowledge must remain grounded in the source.

## Install and start

### Download one version

Use the corresponding Release asset:

- `Chuangmeng_Director_Skills_v1.6.0.zip`
- `Chuangmeng_Director_Skills_v2.0.0-beta.1.zip`

The extracted entry is `chuangmeng-director/SKILL.md`. Import that folder according to your platform's Agent Skills instructions; use direct ZIP import only when the platform supports it.

Both versions use the same identifier, `chuangmeng-director`. Keep one installed version at a time. The old `seedance-director-community` name is a natural-language compatibility alias; platform skill selectors should use the new installed identifier.

### Prepare the input

| Input | Useful details |
|---|---|
| Script | Complete target episode or explicit excerpt, including original dialogue and action |
| Generation settings | Actual target model, current platform duration limit, aspect ratio and medium |
| References | Available character, main/reverse scene, key prop and blocking references; text-only input is also possible |
| Continuity | Previous exit and following entry states when repairing or continuing a segment |
| Current requirements | Full/compact output, pacing, shot preferences and authorized revision scope |

### Starter instruction

```text
Use 创梦 导演skills ($chuangmeng-director).
Target model: [actual model]
Current maximum segment duration: [platform limit]
Aspect ratio and medium: [for example 16:9, live action / 3D animation]
Scope: [episode / scene / excerpt]

Read the complete requested scope. Preserve story facts, dialogue, punctuation and order.
Establish the emotional curve, director's action version and spatial blocking first.
Then provide the complete segment table and all eight-module segment prompts.
Use integer segment durations and default 2–4 second shots, no shot above 4 seconds.
Make visible subjects, foreground/background and camera-relative eyelines explicit.
Connect action phases and overlap; keep one speech event continuous across cuts.
Centralize supplied reference tags in the table and rebuild each entry/exit state fully.

Script: [paste]
References and existing states: [provide]
```

[Quick starter in Chinese](examples/QUICK_START_PROMPT_CN.md) · [Production starter in Chinese](examples/ADVANCED_STARTER_PROMPT_CN.md)

## Duration profiles

These inherited profiles are **repository workflow settings, not current vendor capability guarantees**:

| Profile | Segment range | Behavior |
|---|---|---|
| Seedance 2.0 profile | 8–15 seconds | Split again if the confirmed platform limit is exceeded |
| Seedance 2.5 profile | 16–30 seconds | A 15-second boundary segment may be used when justified; keep one main dramatic objective |
| Local pickup | Explicit requested duration | Do not pad a 4/6-second repair to a default minimum |

Actual platform limits take precedence. Where longer segments are confirmed, 20–25 seconds may be preferred, never exceeding actual capability or 30 seconds.

Shot length differs from segment length: a 24-second segment can contain several 2–4 second shots. An explicitly requested long take can override the default shot limit. Planning timecodes at 0.1-second resolution does not imply frame-exact model execution.

## v2 preview: lightweight state ledger

The v2 workflow separates source facts, the director's action script, scene states and shot events. It uses the ledger to rebuild independent prompts; the audit script validates structure and does not automatically compile JSON into natural-language prompts.

| Category | Recorded state |
|---|---|
| Characters | Fixed position, posture, body direction, eyeline, hands and action phase |
| Props | Holder, hand, location, orientation and functional state |
| Emotion and knowledge | Current emotion and already acquired fact IDs |
| Shot events | The shot containing a change and its before/after values |
| Segment boundary | Complete `entry` and `exit` states |

```text
entry + ordered shot changes = declared exit
previous exit = next entry
```

The next segment's opening action belongs in its first shot event; it cannot excuse an already mismatched entry. Keep off-screen characters and props in the scene ledger.

**The current beta supports one continuous scene and a fixed character/prop roster.** A new scene, entity or explicit time jump requires a separate ledger. The tool cannot determine natural-language physical plausibility, infer whether knowledge is justified, or prove agreement between ledger, prompt and footage.

[State and repair guide](https://github.com/bedelltracietony26477-create/seedance-director-community/blob/preview/v2.0/references/community-state-workflow.md) · [Runnable ledger](https://github.com/bedelltracietony26477-create/seedance-director-community/blob/preview/v2.0/examples/state-ledger.json)

## Audit tools and verification

All audit tools use the **Python standard library**. Running Python is optional for using the skill to write prompts; the scripts provide additional checks on text and explicit state.

| Tool | Availability | Scope |
|---|---|---|
| `dialogue_timing.py` | Both versions | Chinese dialogue duration, punctuation, breath and reaction estimates |
| `segment_timing_audit.py` | Both | Duration profiles, capacity and related beat settings |
| `prompt_audit.py` | Both | One segment's modules, references, source dialogue, shot timecodes and limit |
| `continuity_audit.py` | Both | Basic character/prop state and segment handoffs |
| `state_ledger_audit.py` | v2 preview only | State fields, event replay, exit results and strict boundary equality |

From the extracted skill folder or the matching source checkout:

```bash
python3 scripts/dialogue_timing.py --text '我不会再退了。' --mode restrained --format json
python3 scripts/prompt_audit.py examples/full-prompt.txt --dialogue-json examples/dialogue.json --format json
python3 scripts/segment_timing_audit.py examples/segments-seedance2.0.json --format json
python3 scripts/continuity_audit.py examples/continuity.json --format json
```

In the **v2 preview** only:

```bash
python3 scripts/state_ledger_audit.py examples/state-ledger.json --format json
```

`prompt_audit.py` accepts one executable segment at a time. Match the expected dialogue list to its speech scope. One source event may span consecutive shot substrings, with no event reordering. Use `--reference-policy shot` for explicitly requested shot-level tags; use `--max-shot-seconds` for an explicitly requested longer take.

Run the full regression suite from a **source checkout**; Skill installation ZIPs do not include `tests/`:

```bash
python3 tests/smoke_test.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

Stable tests cover genuine dialogue repetition, speech fragments, missing/reordered words, dialogue outside the timeline, timecode gaps, start/end closure and reference policies. Preview tests additionally cover boundary drift, missing characters, invalid events, unrecorded changes and malformed ledger inputs.

Passing tests means the corresponding text/structure checks passed. Dialogue-only estimates are not final running time. The scripts do not evaluate footage, physical realism, spatial semantics or acting quality.

## Use cases and boundaries

Use for complete episodes, individual scenes, multi-character dialogue, emotional conflict, continuous action, local pickups and narrative prompts requiring cross-segment handoffs. Live-action and animation media can be specified; style and assets should follow the script, references and user requirements.

Community remains readable, editable and reusable. The v2 lightweight ledger is an independent community implementation. Private Pro performance signatures, full semantic prop machinery, quantitative attention budgets and advanced voice-identity systems are excluded.

Neither release currently provides a generated-video comparison experiment or quantified success-rate, cost-saving or image-quality claims. Review source, prompts, ledgers and footage together.

## Examples, documentation and feedback

- [Skill entry](SKILL.md)
- [Full example](examples/full-prompt.txt) / [Quick example](examples/quick-prompt.txt)
- [Shot execution rules](references/shot-execution.md) / [Output contract](references/final-output-contract.md)
- [Stable changelog](https://github.com/bedelltracietony26477-create/seedance-director-community/blob/main/CHANGELOG.md) / [Preview changelog](https://github.com/bedelltracietony26477-create/seedance-director-community/blob/preview/v2.0/CHANGELOG.md)
- [Contributing](https://github.com/bedelltracietony26477-create/seedance-director-community/blob/main/CONTRIBUTING.md) / [Issues](https://github.com/bedelltracietony26477-create/seedance-director-community/issues)

Report the version, target model and limit, expected behavior, observed result and minimal reproduction. Share only material you may disclose and remove personal information.

## License and credit

| Material | License |
|---|---|
| Program code | MIT: [LICENSE-CODE](LICENSE-CODE) |
| Skill instructions, methodology, documentation and textual examples | CC BY 4.0: [LICENSE-DOCS](LICENSE-DOCS) |

Retain credit to **LERler-Q**, formerly **CineWeaver Director Engine**, and follow the corresponding license requirements for attribution, license links and modification notices.

Independent unofficial community project; no affiliation with, sponsorship from or endorsement by ByteDance or the Seedance team. Third-party names and trademarks belong to their respective owners.
