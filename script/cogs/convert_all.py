import os
from datetime import datetime
from pathlib import Path

import frontmatter
import yaml

from . import conversion as convert
from . import file_checking as checkFile
from . import global_value
from . import metadata as mt

BASEDIR= global_value.BASEDIR
vault = global_value.vault


def diff_file(file, folder, update=0):
    file_name = os.path.basename(file)
    if checkFile.check_file(file_name, folder) == "EXIST":
        if update == 1:  # Update : False / Don't check
            return False
        notes_path = Path(f"{folder}/{file_name}")
        retro_old = checkFile.retro(notes_path)
        meta_old = frontmatter.load(notes_path)
        meta_old = mt.remove_frontmatter(meta_old.metadata)

        temp = convert.file_convert(file, folder)
        try:
            front_temp = frontmatter.loads("".join(temp))
        except yaml.parser.ParserError:
            print("ERROR : ", file)
            pass
        meta_new = mt.remove_frontmatter(front_temp.metadata)
        new_version = checkFile.retro(temp, 1)
        if new_version == retro_old and sorted(meta_old.keys()) == sorted(
            meta_new.keys()
        ):
            return False
        else:
            return True
    else:
        return True  # Si le fichier existe pas, il peut pas être identique

def search_share(option=0, stop_share=1):
    filespush = []
    check = False
    folder = "_notes"
    for sub, dirs, files in os.walk(vault):
        for file in files:
            filepath = sub + os.sep + file
            if filepath.endswith(".md") and "excalidraw" not in filepath:
                try:
                    yaml_front = frontmatter.load(filepath)
                    if "folder" in yaml_front.keys():
                        folder = yaml_front["folder"]
                        folder = checkFile.check_folder(folder)
                    else:
                        folder = checkFile.check_folder("_notes")
                    if "share" in yaml_front.keys() and yaml_front["share"] is True:
                        if option == 1:
                            if "update" in yaml_front and yaml_front["update"] is False:
                                update = 1
                            else:
                                update = 0
                            if diff_file(filepath, folder, update):
                                checkFile.delete_file(filepath, folder)
                                contents = convert.file_convert(filepath, folder)
                                check = convert.file_write(filepath, contents, folder)
                            else:
                                check = False
                        if option == 2:
                            checkFile.delete_file(filepath, folder)
                            contents = convert.file_convert(filepath, folder)
                            check = convert.file_write(filepath, contents, folder)
                        destination = checkFile.dest(filepath, folder)
                        if check:
                            filespush.append(destination)
                    else:
                        if stop_share == 1:
                            checkFile.delete_file(filepath, folder)
                except (
                    yaml.scanner.ScannerError,
                    yaml.constructor.ConstructorError,
                ) as e:
                    pass

    return filespush, folder

def convert_all(delopt=False, git=False, force=False, stop_share=0):
    if git:
        git_info = "NO PUSH"
    else:
        git_info = "PUSH"

    if delopt:  # preserve
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] STARTING CONVERT [ALL] OPTIONS :\n- {git_info}\n- PRESERVE FILES"
        )
        new_files, priv = search_share(0, stop_share)
    elif force:
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] STARTING CONVERT [ALL] OPTIONS :\n- {git_info}\n- FORCE UPDATE"
        )
        new_files, priv = search_share(2, stop_share)
    else:
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] STARTING CONVERT [ALL] OPTIONS :\n- {git_info}\n- UPDATE MODIFIED FILES"
        )
        new_files, priv = search_share(1, stop_share)
    commit = "Add to blog:\n"
    if len(new_files) > 0:
        for md in new_files:
            commit = commit + "\n - " + md
        if git is False:
            if len(new_files) == 1:
                md = "".join(new_files)
                commit = md
                convert.clipboard(md, priv)
            commit = f"Add to blog: \n {commit}"
            global_value.git_push(commit)
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 🎉 {commit}")
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] File already exists 😶")