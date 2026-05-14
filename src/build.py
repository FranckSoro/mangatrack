import subprocess

def main():
    # Compiler Tailwind CSS
    subprocess.run(
        ["npm", "install"],
        cwd="src/theme/static_src",
        check=True
    )
    subprocess.run(
        ["npm", "run", "build"],
        cwd="src/theme/static_src",
        check=True
    )

if __name__ == "__main__":
    main()