import os
import re
from datetime import datetime
from pathlib import Path

import frontmatter

from . import global_value as settings

BASEDIR = Path(settings.BASEDIR)
web = settings.web

def remove_frontmatter(meta):
    meta.pop("date", None)
    meta.pop("title", None)
    meta.pop("created", None)
    meta.pop("update", None)
    meta.pop("link", None)
    return meta

def frontmatter_check(filename, folder):
    metadata = open(Path(f"{folder}/{filename}"), "r", encoding="utf-8")
    meta = frontmatter.load(metadata)
    update = frontmatter.dumps(meta)
    folder_key = str(folder).replace(f"{BASEDIR}", "")
    folder_key=folder_key.replace(os.sep, '')
    folder_key=folder_key.replace('_', '')
    metadata.close()
    final = open(Path(f"{folder}/{filename}"), "w", encoding="utf-8")
    now = datetime.now().strftime("%d-%m-%Y")
    if not "current" in meta.keys() or meta["current"] != False:
        meta["date"] = now
        update = frontmatter.dumps(meta)
        meta = frontmatter.loads(update)
    if not "title" in meta.keys():
        meta["title"] = filename.replace(".md", "")
        update = frontmatter.dumps(meta)
    if not "link" in meta.keys():
        filename = filename.replace(".md", "")
        filename = filename.replace(" ", "-")
        clip = f"{web}{folder_key}/{filename}"
        meta["link"] = clip
        update = frontmatter.dumps(meta)
    final.write(update)
    final.close()
    return


def update_frontmatter(file, folder, share=0):
    metadata = open(file, "r", encoding="utf8")
    meta = frontmatter.load(metadata)
    metadata.close()
    folder_key = str(folder).replace(f"{BASEDIR}", "")
    folder_key=folder_key.replace(os.sep, '')
    folder_key=folder_key.replace('_', '')
    if "tag" in meta.keys():
        tag = meta["tag"]
    elif "tags" in meta.keys():
        tag = meta["tags"]
    else:
        tag = ""
    meta.metadata.pop("tag", None)
    meta.metadata.pop("tags", None)
    with open(file, "w", encoding="utf-8") as f:
        filename = os.path.basename(file)
        filename = filename.replace(".md", "")
        filename = filename.replace(" ", "-")
        clip = f"{web}{folder_key}/{filename}"
        meta["link"] = clip
        update = frontmatter.dumps(meta, sort_keys=False)
        meta = frontmatter.loads(update)
        if share == 1 and ("share" not in meta.keys() or meta["share"] == "false"):
            meta["share"] = "true"
            update = frontmatter.dumps(meta, sort_keys=False)
            meta = frontmatter.loads(update)
        if tag != "":
            meta["tag"] = tag
        update = frontmatter.dumps(meta, sort_keys=False)
        if re.search(r"\\U\w+", update):
            emojiz = re.search(r"\\U\w+", update)
            emojiz = emojiz.group().strip()
            raw=r'{}'.format(emojiz)
            convert_emojiz = (
                raw.encode("ascii")
                .decode('unicode_escape')
                .encode("utf-16", "surrogatepass")
                .decode("utf-16")
            )
            update = re.sub(r'"\\U\w+"', convert_emojiz, update)
        f.write(update)
    return