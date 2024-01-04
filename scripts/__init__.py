import subprocess


def tests():
    run_tests_and_configure_coverage = [
        # black ignore formatting:
        # fmt: off
        "python", "-m",
        "coverage", "run", "--source", ".", "--branch", "--omit", "**tests/*,**/__*__.py",
        "-m", "unittest", "discover", "-t", "."
        # fmt: on
    ]
    subprocess.run(run_tests_and_configure_coverage)


def coverage():
    compile_coverage_report = [
        # black ignore formatting:
        # fmt: off
        "python", "-m",
        "coverage", "report", "-m", "--skip-empty", "--fail-under=80"
        # fmt: on
    ]
    completed_proc = subprocess.run(compile_coverage_report)
    if completed_proc.returncode != 0:
        exit(completed_proc.returncode)


def lint():
    subprocess.run(["pre-commit", "run", "--all-files"])


def check():
    tests()
    print()
    coverage()
    print()
    lint()
