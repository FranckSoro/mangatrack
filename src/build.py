import subprocess
import os

def main():
    # Remonter à la racine pour trouver static_src
    static_src = os.path.join(os.path.dirname(__file__), 'theme', 'static_src')
    
    subprocess.run(
        ["npm", "install"],
        cwd=static_src,
        check=True
    )
    subprocess.run(
        ["npm", "run", "build"],
        cwd=static_src,
        check=True
    )

if __name__ == "__main__":
    main()