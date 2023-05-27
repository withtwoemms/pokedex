import subprocess


def tests():
    subprocess.run(["python", "-u", "-m", "unittest", "discover", "tests/"])


def lint():
    subprocess.run(["pre-commit", "run", "--all-files"])


def check():
    tests()
    lint()
