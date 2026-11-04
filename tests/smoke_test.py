from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
def run(*args):
    result=subprocess.run([sys.executable,*args],cwd=ROOT,text=True,capture_output=True)
    if result.returncode:
        raise SystemExit(result.stdout+result.stderr)
def main():
    run('scripts/dialogue_timing.py','--text','我不会再退了。','--mode','restrained','--segment-mode','standard','--format','json')
    for file in ('segments-standard.json','segments-extended.json'):
        run('scripts/segment_timing_audit.py','examples/'+file,'--format','json')
    for file,contract in (('full-prompt.txt','full'),('quick-prompt.txt','quick')):
        run('scripts/prompt_audit.py','examples/'+file,'--contract',contract,'--dialogue-json','examples/dialogue.json','--format','json')
    run('scripts/continuity_audit.py','examples/continuity.json','--format','json')
    print('Pro V1.6 smoke checks passed')
if __name__=='__main__':main()
