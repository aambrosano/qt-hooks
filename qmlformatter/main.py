import argparse
import platform
import sys
from pathlib import Path
from subprocess import Popen

IS_WINDOWS = platform.system() == "Windows"

def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args()
    files = args.filenames
    files = [str(Path(file).resolve(True)) for file in files]
    p = Popen(args=["qmlformat", *files, "--inplace"])
    p.wait(2000)
    while p.poll() is None:
        ...
    sys.exit(p.returncode)

if __name__ == "__main__":
    main()
