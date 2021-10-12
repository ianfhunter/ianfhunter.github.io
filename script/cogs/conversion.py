import os
import re
import sys
from pathlib import Path

import frontmatter

from . import admonition as adm
from . import file_checking as check
from . import global_value as settings
from . import image_transform as links
from . import metadata as mt

BASEDIR = Path(settings.BASEDIR)
vault = Path(settings.vault)

def clipboard(filepath, folder):
    filename = os.path.basename(filepath)
    filename = filename.replace(".md", "")
    filename = filename.replace(" ", "-")
    folder_key = str(folder).replace(f"{settings.BASEDIR}", "")
    folder_key=folder_key.replace(os.sep, '')
    folder_key=folder_key.replace('_', '')
    clip = f"{settings.web}{folder_key}/{filename}"
    if sys.platform == "ios":
        try:
            import pasteboard  # work with pyto

            pasteboard.set_string(clip)
        except ImportError:
            try:
                import clipboard  # work with pytonista

                clipboard.set(clip)
            except ImportError:
                print(
                    "Please, report issue with your OS and configuration to check if it possible to use another clipboard manager"
                )
    else:
        try:
            # trying to use Pyperclip
            import pyperclip

            pyperclip.copy(clip)
        except ImportError:
            print(
                "Please, report issue with your OS and configuration to check if it possible to use another clipboard manager"
            )

def file_write(file, contents, folder):
    file_name = os.path.basename(file)
    if contents == "":
        return False
    else:
        path = Path(f"{folder}/{file_name}")
        if not os.path.exists(path):
            new_notes = open(path, "w", encoding="utf-8")
            for line in contents:
                new_notes.write(line)
            new_notes.close()
            mt.frontmatter_check(file_name, folder)
            return True
        else:
            meta = frontmatter.load(file)
            if not meta["share"] or meta["share"] == False:
                check.delete_file(file, folder)
            return False

def read_custom():
    css = open(f"{BASEDIR}/assets/css/custom.css", "r", encoding="utf-8")
    id = []
    css_data = css.readlines()
    for i in css_data:
        if i.startswith("#"):
            id.append(i.replace("{\n", "").strip())
    css.close()
    return id

def convert_hashtags(final_text):
    css = read_custom()
    token = re.findall("#\w+", final_text)
    token = list(set(token))
    for i in range(0, len(token)):
        if token[i] in css:
            final_text = final_text.replace(token[i], "")
            IAL = "**" + final_text.strip() + "**{: " + token[i] + "}"
            final_text = final_text.replace(final_text, IAL)
        else:
            IAL = (
                    "**"
                    + token[i].replace("#", " ").strip()
                    + "**{: "
                    + token[i].strip()
                    + "}{: .hash}"
            )
            final_text = final_text.replace(token[i], IAL, 1)
    return final_text

def file_convert(file, folder, option=0):
    final = []
    path_folder = str(folder).replace(f"{BASEDIR}", "")
    path_folder=path_folder.replace(os.sep, '')
    path_folder=path_folder.replace('_', '')
    if not path_folder in file:
        data = open(file, "r", encoding="utf-8")
        meta = frontmatter.load(file)
        lines = data.readlines()
        data.close()
        if option == 1:
            if "share" not in meta.keys() or meta["share"] is False:
                meta["share"] = True
                update = frontmatter.dumps(meta)
                meta = frontmatter.loads(update)
                mt.update_frontmatter(file, folder, 1)
            else:
                mt.update_frontmatter(file, folder, 0)
        else:
            mt.update_frontmatter(file, folder, 0)
            if "share" not in meta.keys() or meta["share"] is False:
                return final
        lines = adm.admonition_trad(lines)
        for ln in lines:
            final_text = ln.replace("  \n", "\n")
            final_text = final_text.replace("\n", "  \n")
            final_text = links.convert_to_wikilink(final_text)
            final_text = links.excalidraw_convert(final_text)
            if re.search("\^\w+", final_text) and not re.search(
                "\[\^\w+\]", final_text
            ):
                final_text = re.sub("\^\w+", "", final_text)  # remove block id
            if "embed" in meta.keys() and meta["embed"] == False:
                final_text = links.convert_to_wikilink(final_text)
                final_text = links.convert_no_embed(final_text)
            else:
                final_text = links.transluction_note(final_text)
            final_text = re.sub("\%{2}(.*)\%{2}", "", final_text)
            final_text = re.sub("^\%{2}(.*)", "", final_text)
            final_text = re.sub("(.*)\%{2}$", "", final_text)
            if re.search(r"\\U\w+", final_text) and not "Users" in final_text:
                emojiz = re.search(r"\\U\w+", final_text)
                emojiz = emojiz.group().strip().replace('"', "")
                convert_emojiz = (
                    emojiz.encode("ascii")
                    .decode("unicode-escape")
                    .encode("utf-16", "surrogatepass")
                    .decode("utf-16")
                )
                final_text = re.sub(r"\\U\w+", convert_emojiz, final_text)
            if final_text.strip().endswith("%%") or final_text.strip().startswith("%%"):
                final_text = ""
            elif re.search("[!?]{3}ad-\w+", final_text):
                final_text = final_text.replace("  \n", "\n")
            if re.search("#\w+", final_text) and not re.search("`#\w+`", final_text):
                final_text = convert_hashtags(final_text)
            elif re.search("\{\: (id=|class=|\.).*\}", final_text):
                IAL = re.search("\{\: (id=|class=|\.).*\}", final_text)
                contentIAL = re.search("(.*)\{", final_text)
                if contentIAL:
                    contentIAL = contentIAL.group().replace("{", "")
                    IAL = IAL.group()
                    IAL = IAL.replace("id=", "#")
                    IAL = IAL.replace("class=", ".")
                    if re.search("[\*\_]", contentIAL):  # markdown found
                        syntax = re.search("(\*\*|\*|_)", contentIAL)
                        new = re.sub("(\*\*|\*|_)", "", contentIAL)  # clear md syntax
                        new = syntax.group() + new + syntax.group() + IAL
                    else:
                        new = "**" + contentIAL.rstrip() + "**" + IAL
                    final_text = re.sub(
                        "(.*)\{\: (id=|class=|\.).*\}(\*\*|\*|_)( ?)", new, final_text
                    )
                if re.search("==(.*)==", final_text):
                    final_text = re.sub("==", "[[", final_text, 1)
                    final_text = re.sub("( ?)==", "::highlight]]", final_text, 2)
                    final_text = re.sub("\{\: (id=|class=|\.).*\}", "", final_text)
            elif re.search("==(.*)==", final_text):
                final_text = re.sub("==", "[[", final_text, 1)
                final_text = re.sub("( ?)==", "::highlight]] ", final_text, 2)
            elif re.search(
                "(\[{2}|\().*\.(png|jpg|jpeg|gif)", final_text
            ):  # CONVERT IMAGE
                final_text = links.move_img(final_text)
            elif re.fullmatch(
                "\\\\", final_text.strip()
            ):  # New line when using "\" in obsidian file
                final_text = "  \n"
            elif re.search("(\[{2}|\[).*", final_text):
                # Escape pipe for link name
                final_text = final_text.replace("|", "\|")
                # Remove block ID (because it doesn't work)
                final_text = re.sub("#\^(.*)]]", "]]", final_text)
                final_text = final_text + "  "
            final.append(final_text)
        return final

    else:
        return final


def file_write(file, contents, folder):
    file_name = os.path.basename(file)
    if contents == "":
        return False
    else:
        path = Path(f"{folder}/{file_name}")
        if not os.path.exists(path):
            new_notes = open(path, "w", encoding="utf-8")
            for line in contents:
                new_notes.write(line)
            new_notes.close()
            mt.frontmatter_check(file_name, folder)
            return True
        else:
            meta = frontmatter.load(file)
            if not meta["share"] or meta["share"] == False:
                check.delete_file(file, folder)
            return False
