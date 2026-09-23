# Seedance Director Community v1.5.5

An open-source directing Skill for AI short-drama production. It turns scripts into executable, auditable and continuity-aware prompts for Seedance 2.0 / 2.5 or equivalent video models.

**Unofficial community project.** This repository is not affiliated with, sponsored by, or endorsed by ByteDance or the Seedance team.

## Highlights

- Exact dialogue preservation and timing estimation
- Seedance 2.0 profile: 8–15 second segments
- Seedance 2.5 profile: 16–30 second segments, with a justified 15-second boundary case
- Dialogue Beat Map for long dialogue
- Reaction Ownership for deciding who should be on screen at a key line
- Failed Action staging for interrupted or unfinished actions
- Blocking, eyelines, 180-degree axis and basic cross-segment continuity
- Lightweight character / scene-direction / key-prop / audio reference binding
- Camera, lens, movement, sound and editing design
- Four standard-library-only Python audit tools

## Community scope

V1.5.5 is intentionally lightweight. It does not include heavier systems such as character performance signatures, a full semantic prop-state machine, Semantic ID asset mapping, quantitative Screen Attention Budget, or advanced Voice State.

## Installation

Download the packaged ZIP from Releases and import it using a Skills-compatible environment. `SKILL.md` at the repository root is the entrypoint.

## Audit commands

```bash
python3 scripts/dialogue_timing.py --text 'I will not back down.' --mode neutral --format markdown
python3 scripts/segment_timing_audit.py examples/segments-seedance2.0.json --format markdown
python3 scripts/segment_timing_audit.py examples/segments-seedance2.5.json --format markdown
python3 scripts/prompt_audit.py examples/quick-prompt.txt --contract quick --format markdown
python3 scripts/continuity_audit.py examples/continuity.json --format markdown
```

## License

Dual licensed:

- Program code under the MIT License (`LICENSE-CODE`)
- Skill instructions, documentation, methodology and textual examples under CC BY 4.0 (`LICENSE-DOCS`)

Third-party trademarks, product names and model names remain the property of their respective owners.
