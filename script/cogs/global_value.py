import os
from datetime import datetime
from pathlib import Path
import sys

from dotenv import dotenv_values

BASEDIR = sys.path[1]
env = dotenv_values(Path(f"{BASEDIR}/.env"))
path = Path(f"{BASEDIR}/.git")  # GIT SHARED
post = Path(f"{BASEDIR}/_notes")
img = Path(f"{BASEDIR}/assets/img/")

# Seems to have problem with dotenv with pyto on IOS 15
try:
    vault = Path(env["vault"])
    web = env["blog"]
except KeyError:
    with open(Path(f"{BASEDIR}/.env")) as f:
        vault = Path("".join(f.readlines(1)).replace("vault=", ""))
        web = "".join(f.readlines(2)).replace("blog=", "")

def git_push(COMMIT):
    try:
        import git

        repo = git.Repo(Path(f"{BASEDIR}/.git"))
        repo.git.add(".")
        repo.git.commit("-m", f"{COMMIT}")
        origin = repo.remote("origin")
        origin.push()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {COMMIT} successfully 🎉")
    except ImportError:
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] Please, use another way to push your change 😶"
        )