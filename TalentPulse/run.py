import sys
import subprocess
from pathlib import Path

portal_dir = Path(__file__).resolve().parent / "MAnaging Portal"
script = portal_dir / "run.py"

if script.exists():
    ret = subprocess.run([sys.executable, str(script)] + sys.argv[1:], cwd=str(portal_dir))
    sys.exit(ret.returncode)
else:
    print(f"Error: {script} not found.")
    sys.exit(1)
