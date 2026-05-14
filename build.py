import subprocess
import os

def main():
    static_src = os.path.join("src", "theme", "static_src")
    
    subprocess.run(["npm", "install"], cwd=static_src, check=True)
    subprocess.run(["npm", "run", "build"], cwd=static_src, check=True)

if __name__ == "__main__":
    main()