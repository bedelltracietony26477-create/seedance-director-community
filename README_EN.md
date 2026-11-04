# 创梦 导演skills · Chuangmeng Director Skills

An open community workflow for turning complete scripts into self-contained cinematic AI-video prompts. Formerly **CineWeaver Director Engine / Seedance Director Community**. Created and maintained by **LERler-Q**.

| Release | Purpose | Download |
|---|---|---|
| v1.6.0 | Stable community workflow: shot visibility, camera-relative eyelines, physical action and dialogue continuity | [Release](../../releases/tag/v1.6.0) |
| v2.0.0-beta.1 | Preview: director's script, lightweight state ledger and local repair | [Source](../../tree/preview/v2.0) · [Release](../../releases/tag/v2.0.0-beta.1) |
| v1.5.5 | Historical community release | [Release](../../releases/tag/v1.5.5) |

The default branch remains v1.6.0. Skill release numbers are separate from video-model versions. Install one version at a time; both use the `chuangmeng-director` skill identifier. The previous name is a natural-language compatibility alias.

## Start

Download the versioned skill ZIP from Releases. Import its `chuangmeng-director/` folder into an Agent Skills-compatible environment using that platform's instructions. Entry: `SKILL.md`.

Ask `$chuangmeng-director` to read your complete script, preserve dialogue and punctuation, establish emotion and spatial blocking, then output all independent segments. Supply your target model and its current duration limit plus available references.

Default shots last 2–4 seconds with a 4-second maximum. Whole-segment durations are integers. Reference tags are centralized in the reference table by default; legacy shot-level tags are available with `--reference-policy shot` in the auditor. A continuous speech event may span adjacent shots without restarting or repeating words.

The inherited duration profiles are workflow settings, not current vendor capability guarantees. Actual platform limits take precedence. Short pickups and user-requested long takes are supported explicitly.

## Verify

All scripts use the Python standard library:

```bash
python3 tests/smoke_test.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/prompt_audit.py examples/full-prompt.txt --dialogue-json examples/dialogue.json --format json
```

Text/structure tests cannot verify generated footage, physical realism or directing quality. No generated-video benchmark is claimed for these releases.

## Scope and license

Community v2 introduces an independently implemented lightweight ledger. Private Pro performance signatures, full semantic prop machinery, quantitative attention budgets and advanced voice-identity systems are excluded.

Code: MIT. Skill instructions, methodology, documentation and textual examples: CC BY 4.0. Retain attribution to **LERler-Q**, formerly **CineWeaver Director Engine**. Independent unofficial project; no affiliation with ByteDance or Seedance.
