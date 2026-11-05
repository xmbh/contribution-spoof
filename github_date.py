
import os
import subprocess
from pathlib import Path

GITHUB_USER = "xmbh"
REPO_NAME = "contribution-spoof"
COMMIT_DATE = "1970-01-01T12:00:00 +0000"

REPO_DIR = Path.cwd() / REPO_NAME

def run(*args, env=None):
    subprocess.run(
        list(args),
        check=True,
        env=env
    )

def main():
    print("GitHub Contribution Graph")
    print(f"Account: {GITHUB_USER}")
    print(f"Commit date: {COMMIT_DATE}")

    # Verify GitHub authentication
    run("gh", "auth", "status")

    # Verify account
    result = subprocess.run(
        ["gh", "api", "user", "--jq", ".login"],
        capture_output=True,
        text=True,
        check=True
    )
    if result.stdout.strip().lower() != GITHUB_USER.lower():
        raise RuntimeError("Wrong GitHub account!")

    if REPO_DIR.exists():
        raise RuntimeError("Repository folder already exists!")

    REPO_DIR.mkdir()
    os.chdir(REPO_DIR)

    # Initialize repository
    run("git", "init", "-b", "main")

    # Create README
    Path("README.md").write_text(
        "# Contribution Graph\n\n"
        f"Historical commit: {COMMIT_DATE}\n",
        encoding="utf-8"
    )

    run("git", "add", "README.md")

    # Set both Git timestamps
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = COMMIT_DATE
    env["GIT_COMMITTER_DATE"] = COMMIT_DATE

    run("git", "commit", "-m", "Historical commit", env=env)

    # Create and push GitHub repository
    run(
        "gh", "repo", "create",
        f"{GITHUB_USER}/{REPO_NAME}",
        "--public",
        "--source", ".",
        "--remote", "origin",
        "--push"
    )

    print("\nSUCCESS!")
    print(f"https://github.com/{GITHUB_USER}/{REPO_NAME}")

if __name__ == "__main__":
    main()
