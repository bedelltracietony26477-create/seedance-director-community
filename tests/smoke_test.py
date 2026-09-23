from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> None:
    proc = subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        raise SystemExit(
            f"command failed: {' '.join(args)}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )


def main() -> None:
    run("scripts/dialogue_timing.py", "--text", "我不会再退了。", "--mode", "restrained", "--format", "json")
    run("scripts/segment_timing_audit.py", "examples/segments-seedance2.0.json", "--format", "json")
    run("scripts/segment_timing_audit.py", "examples/segments-seedance2.5.json", "--format", "json")
    run("scripts/prompt_audit.py", "examples/quick-prompt.txt", "--contract", "quick", "--format", "json")
    run("scripts/continuity_audit.py", "examples/continuity.json", "--format", "json")
    print("smoke tests passed")


if __name__ == "__main__":
    main()
