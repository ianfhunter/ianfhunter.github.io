import glob
import os
from pathlib import Path

import frontmatter

from . import global_value as settings

BASEDIR = settings.BASEDIR
post = settings.post
vault = settings.vault

def check_folder(folder_key):
    path = Path(f"{BASEDIR}/_{folder_key}")
    if os.path.isdir(path):
        return path
    else:
        return post

def retro(filepath, opt=0):
    notes = []
    if opt == 0:
        metadata = frontmatter.load(filepath)
    else:
        metadata = frontmatter.loads("".join(filepath))
    file = metadata.content.split("\n")
    for n in file:
        notes.append(n)
    return notes

# PATH WORKING #
def delete_file(filepath, folder):
    path = Path(folder)
    for file in os.listdir(path):
        filepath = os.path.basename(filepath)
        filecheck = os.path.basename(file)
        if filecheck == filepath:
            os.remove(Path(f"{path}/{file}"))
            return True
    return False


def delete_not_exist():
    # for file in poste : if file not in vault : delete file
    vault_file = []
    important_folder=["_includes", "_layout", "_site", "assets", "script"]
    for filename in glob.iglob(f"{vault}**/**", recursive=True):
        vault_file.append(os.path.basename(filename))
    for file in glob.iglob(f"{BASEDIR}/_*/**"):
        if not any(folder in file for folder in important_folder) and os.path.basename(file) not in vault_file:
            os.remove(Path(file))


def check_file(filepath, folder):
    post_file = []
    folder = Path(folder)
    for file in glob.iglob(f"{folder}/**"):
        post_file.append(os.path.basename(file))
    if filepath in post_file:
        return "EXIST"
    else:
        return "NE"


def dest(filepath, folder):
    file_name = os.path.basename(filepath)
    dest = Path(f"{folder}/{file_name}")
    return str(dest)