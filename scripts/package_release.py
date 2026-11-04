"""Package the complete Pro skill and public documentation."""
from pathlib import Path
import hashlib
import zipfile
ROOT=Path(__file__).resolve().parents[1]
def main():
    version=(ROOT/'VERSION').read_text().strip()
    if version!='1.6.1':raise SystemExit('Expected Pro release 1.6.1')
    out=ROOT/'dist';out.mkdir(exist_ok=True)
    target=out/f'Chuangmeng_Director_Skills_Pro_v{version}.zip'
    roots=['SKILL.md','VERSION','SOURCE_MANIFEST.json','README.md','README_EN.md','RELEASE_NOTES.md','CHANGELOG.md','CONTRIBUTING.md','LICENSE','LICENSE-CODE','LICENSE-DOCS','CREDITS.md','agents','references','scripts','assets','examples','tests','docs']
    paths=[]
    for name in roots:
        p=ROOT/name
        paths.extend([p] if p.is_file() else (x for x in p.rglob('*') if x.is_file()))
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(paths):
            if '__pycache__' not in p.parts and p.suffix!='.pyc':
                z.write(p,Path('chuangmeng-director-pro')/p.relative_to(ROOT))
    checksum=out/f'SHA256SUMS-Pro-v{version}.txt'
    checksum.write_text(hashlib.sha256(target.read_bytes()).hexdigest()+'  '+target.name+'\n')
    print(target.name)
if __name__=='__main__':main()
