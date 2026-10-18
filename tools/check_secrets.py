"""Fail if a value from .env appears in the staged changes (the repository is public, D-015).

Host, port and user names are not secrets and are skipped. Without .env (CI)
there is nothing to compare; there the git history is scanned with gitleaks.

Usage: python tools/check_secrets.py
"""
import subprocess
import sys

from pg import read_env

NON_SECRET_SUFFIXES = ("HOST", "PORT", "USER")
MIN_LENGTH = 8


def main():
    values = {key: value for key, value in read_env().items()
              if len(value) >= MIN_LENGTH and not key.endswith(NON_SECRET_SUFFIXES)}
    if not values:
        print("secrets: no .env values to look for")
        return 0
    diff = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True,
                          encoding="utf-8", errors="replace", check=True).stdout
    hits = sorted(key for key, value in values.items() if value in diff)
    if hits:
        print(f"secrets: the staged changes contain the .env value of {', '.join(hits)}")
        return 1
    print(f"secrets: OK ({len(diff.splitlines())} staged diff lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
