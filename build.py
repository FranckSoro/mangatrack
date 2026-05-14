import subprocess
import os
import sys

def main():
    base_dir = os.path.dirname(__file__)
    static_src = os.path.join(base_dir, 'theme', 'static_src')
    
    # 1. Compiler Tailwind
    print("==> Compiling Tailwind CSS...")
    subprocess.run(["npm", "install"], cwd=static_src, check=True)
    subprocess.run(["npm", "run", "build"], cwd=static_src, check=True)
    
    # 2. Collecter les statics APRES la compilation
    print("==> Running collectstatic...")
    subprocess.run(
        [sys.executable, "manage.py", "collectstatic", "--noinput"],
        cwd=base_dir,
        check=True
    )

if __name__ == "__main__":
    main()