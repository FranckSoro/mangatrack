import subprocess
import sys

def main():
    print("Building Tailwind CSS...")
    subprocess.run(
        [sys.executable, "src/manage.py", "tailwind", "install"],
        check=True
    )
    subprocess.run(
        [sys.executable, "src/manage.py", "tailwind", "build"],
        check=True
    )
    print("Build complete!")

if __name__ == "__main__":
    main()
