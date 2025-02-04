import argparse
import os
import shutil
import sys
from pathlib import Path
from subprocess import Popen

def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args()
    files = args.filenames
    files = [str(Path(file).resolve(True)) for file in files]

    # allow qmlformat tool to be injected through the environment so we can use
    # different version of qmlformat than whatever Qt version we have on PATH
    qmlformat_env_cmd = Path(os.environ.get("PRECOMMIT_QT_HOOKS_QMLFORMAT", None))
    qmlformat_cmd = "qmlformat"

    if qmlformat_env_cmd is not None:
        if not Path.exists(qmlformat_env_cmd) or not Path.is_file(qmlformat_env_cmd):
            print("PRECOMMIT_QT_HOOKS_QMLFORMAT points to an invalid file, ignoring.")
        else:
            qmlformat_cmd = qmlformat_env_cmd

    if not shutil.which(qmlformat_cmd):
        print(f"Couldn't find qmlformat when running \"{qmlformat_cmd}\", either make it available " +
               "in PATH, or explicitly set it through the env variable PRECOMMIT_QT_HOOKS_QMLFORMAT")
        return 1

    p = Popen(args=[qmlformat_cmd, *files, "--inplace"])
    p.wait(2000)
    while p.poll() is None:
        ...
    return p.returncode

if __name__ == "__main__":
    sys.exit(main())
