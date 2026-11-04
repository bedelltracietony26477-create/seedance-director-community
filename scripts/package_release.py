"""Build a source-only, single-root skill archive; no external dependencies."""
import hashlib
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]

def main():
    version = (ROOT / "VERSION").read_text().strip()
    import re
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:-[a-z]+\.[0-9]+)?", version):
        raise SystemExit("Invalid VERSION")
    out = ROOT / "dist"
    out.mkdir(exist_ok=True)
    target = out / f"Chuangmeng_Director_Skills_v{version}.zip"
    roots = ["SKILL.md", "VERSION", "README.md", "README_EN.md", "LICENSE", "LICENSE-CODE", "LICENSE-DOCS", "CREDITS.md", "agents", "references", "scripts", "assets", "examples"]
    paths = []
    for name in roots:
        p = ROOT / name
        paths.extend([p] if p.is_file() else (x for x in p.rglob("*") if x.is_file()))
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for p in sorted(paths):
            if "__pycache__" not in p.parts and p.suffix != ".pyc":
                archive.write(p, Path("chuangmeng-director") / p.relative_to(ROOT))
    checksum = out / f"SHA256SUMS-v{version}.txt"
    checksum.write_text(hashlib.sha256(target.read_bytes()).hexdigest() + "  " + target.name + "\n")
    print(target.name)

if __name__ == "__main__":
    main()
