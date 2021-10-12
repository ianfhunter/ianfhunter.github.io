import os
from datetime import datetime

import frontmatter

from . import conversion as convert
from . import file_checking as checkFile
from . import global_value as gl


def convert_one(ori, delopt, git):
    file_name = os.path.basename(ori).upper()
    yaml_front = frontmatter.load(ori)
    priv = "_notes"
    if "folder" in yaml_front.keys():
        priv = yaml_front["folder"]
        priv=checkFile.check_folder(priv)
    if delopt is False:
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] STARTING CONVERT [{file_name}] OPTIONS :\n- UPDATE "
        )
        checkFile.delete_file(ori, priv)
    else:
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] STARTING CONVERT [{file_name}] OPTIONS :\n- PRESERVE"
        )
    contents = convert.file_convert(ori, priv, 1)
    check = convert.file_write(ori, contents, priv)
    if check and not git:
        COMMIT = f"Pushed {file_name.lower()} to blog"
        gl.git_push(COMMIT)
        convert.clipboard(ori, priv)
    elif check and git:
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] 🎉 Successfully converted {file_name.lower()}"
        )
    else:
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] {file_name.lower()} already converted 😶"
        )
