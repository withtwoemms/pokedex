import subprocess


def test():
    subprocess.run(["python", "-u", "-m", "unittest", "discover"])


def lint():
    subprocess.run(["pre-commit", "run", "--all-files"])
