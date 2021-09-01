import os
from dotenv import dotenv_values
from pathlib import Path
import shutil
BASEDIR = os.path.abspath(os.path.dirname(__file__))
env = dotenv_values(Path(f"{BASEDIR}/.env"))
path = Path(f"{BASEDIR}/.git")  # GIT SHARED
vault = Path(env["vault"])

def search_share(option=0):
    for sub, dirs, files in os.walk(vault):
        for file in files:
            filepath = sub + os.sep + file
            print(filepath)

search_share()