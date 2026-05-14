# src/build.py
#!/usr/bin/env python
"""Build script for Vercel deployment"""
import os
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def run_command(cmd, cwd=None):
    """Exécute une commande shell et affiche la sortie"""
    print(f"🔧 Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    result = subprocess.run(
        cmd if isinstance(cmd, list) else cmd.split(),
        cwd=cwd,
        capture_output=True,
        text=True
    )
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=os.sys.stderr)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")

def main():
    # 1. Compiler Tailwind CSS (si les sources existent)
    tailwind_src = BASE_DIR / "theme" / "static_src"
    if (tailwind_src / "package.json").exists():
        print("🎨 Compiling Tailwind CSS...")
        run_command(["npm", "run", "build"], cwd=tailwind_src)
    
    # 2. Collecter les fichiers statiques Django
    print("📦 Collecting static files...")
    run_command(["python", "manage.py", "collectstatic", "--noinput"])
    
    print("✅ Build completed successfully!")

if __name__ == "__main__":
    main()