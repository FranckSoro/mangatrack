import subprocess
import os
import sys

def main():
    static_src = os.path.join(os.path.dirname(__file__), 'theme', 'static_src')
    
    # 1. Compiler Tailwind
    subprocess.run(["npm", "install"], cwd=static_src, check=True)
    subprocess.run(["npm", "run", "build"], cwd=static_src, check=True)
    
    # 2. Forcer collectstatic après la compilation
    subprocess.run(
        [sys.executable, "manage.py", "collectstatic", "--noinput"],
        cwd=os.path.dirname(__file__),
        check=True
    )

if __name__ == "__main__":
    main()