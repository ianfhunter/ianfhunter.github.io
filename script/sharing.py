# -*- coding: utf-8 -*-

import re
import sys
import os
from dotenv import dotenv_values
from pathlib import Path
from pathlib import PurePath
import shutil
from datetime import datetime
import frontmatter
import yaml
import argparse

sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")

BASEDIR = os.path.abspath(os.path.dirname(__file__))
if "script" in BASEDIR:
    BASEDIR = PurePath(BASEDIR).parents[0]
env = dotenv_values(Path(f"{BASEDIR}/.env"))
path = Path(f"{BASEDIR}/.git")  # GIT SHARED
post = Path(f"{BASEDIR}/_notes")
img = Path(f"{BASEDIR}/assets/img/")

# Seems to have problem with dotenv with pyto on IOS 15
try:
    vault = Path(env["vault"])
    blog = env["blog"]
except KeyError:
    with open(Path(f"{BASEDIR}/.env")) as f:
        vault = Path("".join(f.readlines(1)).replace("vault=", ""))
        blog = "".join(f.readlines(2)).replace("blog=", "")


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

def remove_frontmatter(meta):
    meta.pop('date', None)
    meta.pop('title', None)
    meta.pop('created', None)
    return meta

def diff_file(file, update=0):
    file_name = os.path.basename(file)
    if check_file(file_name) == "EXIST" :
        if update == 1 : #Update : False / Don't check
            return False
        notes_path = Path(f"{BASEDIR}/_notes/{file_name}")
        retro_old = retro(notes_path)
        meta_old= frontmatter.load(notes_path)
        meta_old = remove_frontmatter(meta_old.metadata)

        temp = file_convert(file)
        front_temp = frontmatter.loads(''.join(temp))
        meta_new = remove_frontmatter(front_temp.metadata)
        new_version = retro(temp, 1)
        if new_version == retro_old and sorted(meta_old.keys()) == sorted(meta_new.keys()):
            return False
        else:
            return True
    else:
        return True #Si le fichier existe pas, il peut pas être identique

# PATH WORKING #

def delete_file(filepath):
    for file in os.listdir(post):
        filepath = os.path.basename(filepath)
        filecheck = os.path.basename(file)
        if filecheck == filepath:
            os.remove(Path(f"{BASEDIR}/_notes/{file}"))
            return True
    return False

def relative_path(data):
    data = data.rstrip() + ".md"
    data = os.path.basename(data)
    for sub, dirs, files in os.walk(vault):
        for file in files:
            filepath = sub + os.sep + file
            if data == file:
                return filepath
def check_file(filepath):
    for file in os.listdir(post):
        if filepath == file:
            return "EXIST"
    return "NE"
def dest(filepath):
    file_name = os.path.basename(filepath)
    dest = Path(f"{BASEDIR}/_notes/{file_name}")
    return str(dest)

def frontmatter_check(filename):
    metadata = open(Path(f"{BASEDIR}/_notes/{filename}"), "r", encoding="utf-8")
    meta = frontmatter.load(metadata)
    update = frontmatter.dumps(meta)
    metadata.close()
    final = open(Path(f"{BASEDIR}/_notes/{filename}"), "w", encoding="utf-8")
    now = datetime.now().strftime("%d-%m-%Y")
    if not 'current' in meta.keys() or meta['current'] != False:
        meta["date"] = now
        update = frontmatter.dumps(meta)
        meta = frontmatter.loads(update)
    if not "title" in meta.keys():
        meta["title"] = filename.replace(".md", "")
        update = frontmatter.dumps(meta)
    final.write(update)
    final.close()
    return


# ADMONITION CURSED THINGS
def admonition_trad_type(line):
    # Admonition Obsidian : blockquote + ad-
    # Admonition md template : ```ad-type <content> ```
    # build dictionnary for different types
    admonition = {
        "note": "note",
        "seealso": "note",
        "abstract": "abstract",
        "summary": "abstract",
        "tldr": "abstract",
        "info": "todo",
        "todo": "todo",
        "tip": "tip",
        "hint": "tip",
        "important": "tip",
        "success": "done",
        "check": "done",
        "done": "done",
        "question": "question",
        "help": "question",
        "faq": "question",
        "warning": "warning",
        "caution": "warning",
        "attention": "warning",
        "failure": "failure",
        "fail": "failure",
        "missing": "failure",
        "danger": "danger",
        "error": "danger",
        "bug": "bug",
        "example": "example",
        "exemple": "example",
        "quote": "quote",
        "cite": "quote",
    }
    admonition_type = re.search("```ad-(.*)", line)
    ad_type = line
    content_type = ""
    admo_format = 'block'
    if admonition_type:
        admonition_type = admonition_type.group(1)
        if admonition_type.lower() in admonition.keys():  # found type
            content_type = admonition[admonition_type]
            ad_type = "\n{: ." + content_type + "}  \n"
        else:
            ad_type = "\n{: .note}  \n"
            content_type = (
                "custom" + admonition_type
            )  # if admonition "personnal" type, use note by default
    elif re.search('(!{3}|\?{3})\+? ad-\w+(.*)', line): #Non-block admonition
        admo_format='MT'
        admonition_type=re.search('ad-\w+', line).group()
        admonition_type = admonition_type.replace('ad-', '')
        if admonition_type.lower() in admonition.keys():
            content_type=admonition[admonition_type]
            ad_type="\n{: ." + content_type + "}  \n"
        else:
            ad_type = "\n{: .note}  \n"
            content_type = (
                "custom" + admonition_type
            )
    return ad_type, content_type, admo_format

def admonition_title_MT(line):
    title_group = re.search('ad-\w+(.*)', line)
    if title_group:
        title_group=title_group.group(1)
        if re.search('\w+', title_group):
            title_MT = title_group
        else:
            title_MT = 'inline'
    else:
        title_MT = 'not'
    return title_MT

def admonition_title_block (line):
    ad_title = re.search("title:(.*)", line)
    if ad_title:
        ad_title=ad_title.group(1)
        if len(ad_title) > 0:
            title_block = ad_title
        else:
            title_block = 'inline'
    else:
        title_block = 'not'
    return title_block

def admonition_title(title, content_type, format):
    # ⚠ Nous sommes sur la DEUXIÈME LIGNE (ad_start+1) : Il n'y aura JAMAIS le content type ici, qui est TOUJOURS sur ad_start
    # trois type de format :
        # inline = {: .content_type} \n > line
        # not : = {: .content_type} \n **content_type**{: .ad-title-type}
        # title : = '{: .content_type} \n **title**{: .ad-title-type}
    if title == 'inline':
        admo_title = '>' + title
    elif title == 'not':
        if 'custom' in content_type:
            content_type=content_type.replace("custom", '')
            title_format='[' + content_type.strip().title() + ']'
            content_type = 'note'
        else:
            title_format = content_type.strip().title()
        admo_title = '> **' + title_format + "**{: .ad-title-" + content_type.strip() + '}'
    else:
        if 'custom' in content_type:
            content_type=content_type.replace('custom', '')
            title_format='[' + content_type.strip().title() + '] ' + title.strip()
            admo_title = '> **' + title_format + '**{: .ad-title-note}\n'
        else:
            title_format = title.strip()
            admo_title = '> **'+ title_format +'**{: .ad-title-' + content_type.strip() + '}\n'
    return admo_title


def admonition_trad_content(line):
    if "collapse:" in line:
        title = ""
    elif "icon:" in line:
        title = ""
    elif "color:" in line:
        title = ""
    elif len(line) == 1:
        title = ""
    else:
        if line[-1] == "\n":
            title = "\t" + line + ""
        else:
            title = "\t" + line + "\n"
    return title


def admonition_trad(file_data):
    code_index = 0
    code_dict = {}
    start_list = []
    end_list = []
    for i in range(0, len(file_data)):
        if re.search("```ad-(.*)", file_data[i]) or re.search('(!{3}|\?{3})\+? ad-\w+(.*)', file_data[i]):
            start = i
            start_list.append(start)
        elif re.match("```", file_data[i]) or re.match('--- admonition', file_data[i]):
            end = i
            end_list.append(end)
    for i, j in zip(start_list, end_list):
        code = {code_index: (i, j)}
        code_index = code_index + 1
        code_dict.update(code)
    for ad, ln in code_dict.items():
        ad_start = ln[0]
        ad_end = ln[1]
        file_data[ad_start], ad_type, ad_format = admonition_trad_type(file_data[ad_start])
        inter=ad_start
        if ad_format == 'MT':
            inter = ad_start+2
            if ad_format == 'MT':
                title = admonition_title_MT(file_data[ad_start])
                if title != 'not':
                    file_data[ad_start + 1] = admonition_title(title, ad_type, ad_format) # title
                else:
                    file_data[ad_start+1] = admonition_title(title, ad_type, ad_format) + '\n' + admonition_trad_content(file_data[ad_start+1])
                    file_data[ad_start + 1] = file_data[ad_start + 1]
        elif ad_format == 'block':
            inter = ad_start+2
            title = admonition_title_block(file_data[ad_start+1])
            if title != 'not':
                file_data[ad_start + 1] = admonition_title(title, ad_type, ad_format)
            else:
                file_data[ad_start + 1] = admonition_title(title, ad_type, ad_format) + '\n' + admonition_trad_content(file_data[ad_start + 1])
                file_data[ad_start + 1] = file_data[ad_start + 1]
        code_block = [x for x in range(inter, ad_end)]
        for fl in code_block:
            data = admonition_trad_content(file_data[fl].strip())
            if data.strip() != '':
                file_data[fl] = data
        file_data[ad_end]='  '
    return file_data


# IMAGES

def get_image(image):
    image = os.path.basename(image)
    for sub, dirs, files in os.walk(vault):
        for file in files:
            filepath = sub + os.sep + file
            if image in file:
                return filepath

def move_img(line):
    img_flags = re.search("[\|\+\-](.*)[]{1,2})]", line)
    if img_flags and not re.search('\-\d+', line):
        img_flags = img_flags.group(0)
        img_flags = img_flags.replace("|", "")
        img_flags = img_flags.replace("]", "")
        img_flags = img_flags.replace(")", "")
        img_flags.replace("(", "")
    else:
        img_flags = ""
    final_text = re.search("(\[{2}|\().*\.(png|jpg|jpeg|gif)", line)
    final_text = final_text.group(0)
    final_text = final_text.replace("(", "")
    final_text = final_text.replace("%20", " ")
    final_text = final_text.replace("[", "")
    final_text = final_text.replace("]", "")
    final_text = final_text.replace(")", "")
    image_path = get_image(final_text)
    final_text = os.path.basename(final_text)
    img_flags = img_flags.replace(final_text, "")
    img_flags = img_flags.replace("(", "")
    if image_path:
        shutil.copyfile(image_path, f"{img}/{final_text}")
        final_text = f"../assets/img/{final_text}"
        final_text = f"![{img_flags}]({final_text})"
        final_text = re.sub(
            "!?(\[{1,2}|\().*\.(png|jpg|jpeg|gif)(.*)(\]{2}|\))", final_text, line
        )
    else:
        final_text = line
    return final_text




def excalidraw_convert(line):
    if '.excalidraw' in line:
        #take the png img from excalidraw
        line = line.replace('.excalidraw', '.excalidraw.png')
        line = line.replace('.md', '')
    return line

def convert_no_embed(line):
    final_text = line
    if re.match("\!\[{2}", line) and not re.match("(.*)\.(png|jpg|jpeg|gif)", line):
        final_text = line.replace("!", "")  # remove "!"
        final_text = re.sub("#\^(.*)", "]]", final_text)  # Link to block doesn't work
    return final_text


def convert_to_wikilink(line):
    final_text = line
    if (
        not re.search("\[\[", final_text)
        and re.search("\[(.*)]\((.*)\)", final_text)
        and not re.search("https", final_text)
    ):  # link : [name](file#title) (and not convert external_link)
        title = re.search("\[(.*)]", final_text)
        title = title.group(1)
        link = re.search("\((.*)\)", final_text)
        link = link.group(1)
        link = link.replace("%20", " ")
        wiki = f"[[{link.replace('.md', '')}|{title}]] "
        final_text = re.sub("\[(.*)]\((.*)\)", wiki, final_text)

    return final_text


def transluction_note(line):
    # If file (not image) start with "![[" : transluction with rmn-transclude (exclude
    # image from that)
    # Note : Doesn't support partial transluction for the moment ; remove title
    final_text = line
    if re.search("\!\[", line) and not re.search("(png|jpg|jpeg|gif)", line) and not re.search('https', line):
        final_text = line.replace("!", "")  # remove "!"
        final_text = re.sub("#(.*)", "]]", final_text)
        final_text = re.sub("\\|(.*)", "]]", final_text)  # remove Alternative title
        final_text = re.sub("]]", "::rmn-transclude]]", final_text)
    return final_text


def clipboard(filepath):
    filename = os.path.basename(filepath)
    filename = filename.replace(".md", "")
    filename = filename.replace(" ", "-")
    clip = f"{blog}{filename}"
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

def file_write(file, contents):
    file_name = os.path.basename(file)
    if contents == '':
        return False
    else:
        if not os.path.exists(Path(f"{BASEDIR}/_notes/{file_name}")):
            new_notes = open(Path(f"{BASEDIR}/_notes/{file_name}"), "w", encoding="utf-8")
            for line in contents:
                new_notes.write(line)
            new_notes.close()
            frontmatter_check(file_name)
            return True
        else:
            meta = frontmatter.load(file)
            if not meta["share"] or meta["share"] == False:
                delete_file(file)
            return False

def file_convert(file, option=0):
    final =[]
    file_name = os.path.basename(file)
    if not "_notes" in file:
        data = open(file, "r", encoding="utf-8")
        meta = frontmatter.load(file)
        lines = data.readlines()
        data.close()
        if option == 1:
            if "share" not in meta.keys() or meta["share"] is False:
                meta["share"] = True
                update = frontmatter.dumps(meta)
                meta = frontmatter.loads(update)
        else:
            if "share" not in meta.keys() or meta["share"] is False :
                return final
        lines = admonition_trad(lines)
        for ln in lines:
            final_text = ln.replace("  \n", '\n')
            final_text = final_text.replace("\n", "  \n")
            final_text = convert_to_wikilink(final_text)
            final_text=excalidraw_convert(final_text)
            if re.search("\^\w+", final_text) and not re.search('\[\^\w+\]', final_text):
                final_text = re.sub("\^\w+", "", final_text)  # remove block id
            if "embed" in meta.keys() and meta["embed"] == False:
                final_text = convert_to_wikilink(final_text)
                final_text = convert_no_embed(final_text)
            else:
                final_text = transluction_note(final_text)
            if re.search("\%{2}(.*)\%{2}", final_text, re.DOTALL):
                final_text = re.sub('\%{2}(.*)\%{2}', '', final_text)
            elif re.search("==(.*)==", final_text):
                final_text = re.sub("==", "[[", final_text, 1)
                final_text = re.sub("( ?)==", "::highlight]] ", final_text, 2)
            elif re.search(
                "(\[{2}|\().*\.(png|jpg|jpeg|gif)", final_text
            ):  # CONVERT IMAGE
                final_text = move_img(final_text)
            elif (
                re.fullmatch('\\\\', final_text.strip())
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


def search_share(option=0):
    filespush = []
    update = 0
    check = False
    for sub, dirs, files in os.walk(vault):
        for file in files:
            filepath = sub + os.sep + file
            if filepath.endswith(".md") and "excalidraw" not in filepath:
                try:
                    yaml_front = frontmatter.load(filepath)
                    if "share" in yaml_front and yaml_front["share"] is True :
                        if option == 1:
                            if 'update' in yaml_front and yaml_front['update'] is False:
                                update = 1
                            else:
                                update = 0
                            if diff_file(filepath, update):
                                delete_file(filepath)
                                contents = file_convert(filepath)
                                check = file_write(filepath, contents)
                            else:
                                check = False
                        if option == 2:
                            delete_file(filepath)
                            contents = file_convert(filepath)
                            check = file_write(filepath, contents)
                        destination = dest(filepath)
                        if check:
                            filespush.append(destination)
                except (
                    yaml.scanner.ScannerError,
                    yaml.constructor.ConstructorError,
                ) as e:
                    pass

    return filespush


def git_push(COMMIT):
    try:
        import git

        repo = git.Repo(Path(f"{BASEDIR}/.git"))
        repo.git.add(".")
        repo.git.commit("-m", f"{COMMIT}")
        origin = repo.remote('origin')
        origin.push()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {COMMIT} successfully 🎉")
    except ImportError:
        print(
            "[{datetime.now().strftime('%H:%M:%S')}] Please, use another way to push your change 😶"
        )


def convert_one(ori, delopt, git):
    file_name = os.path.basename(ori).upper()
    if delopt is False:
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] STARTING CONVERT [{file_name}] OPTIONS :\n- UPDATE "
        )
        delete_file(ori)
    else:
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] STARTING CONVERT [{file_name}] OPTIONS :\n- PRESERVE"
        )
    contents = file_convert(ori, 1)
    check = file_write(ori, contents)
    if check and not git:
        COMMIT = f"Pushed {file_name.lower()} to blog"
        git_push(COMMIT)
        clipboard(ori)
    elif check and git:
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] 🎉 Successfully converted {file_name.lower()}"
        )
    else:
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] {file_name.lower()} already converted 😶"
        )


def convert_all(delopt=False, git=False, force=False):
    if git:
        git_info = "NO PUSH"
    else:
        git_info = "PUSH"

    if delopt:  # preserve
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] STARTING CONVERT [ALL] OPTIONS :\n- {git_info}\n- PRESERVE FILES"
        )
        new_files = search_share()
    elif force:
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] STARTING CONVERT [ALL] OPTIONS :\n- {git_info}\n- FORCE UPDATE"
        )
        new_files = search_share(2)
    else:
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] STARTING CONVERT [ALL] OPTIONS :\n- {git_info}\n- UPDATE MODIFIED FILES"
        )
        new_files = search_share(1)
    commit = "Add to blog:\n"
    if len(new_files) > 0:
        for md in new_files:
            commit = commit + "\n - " + md
        if git is False:
            if len(new_files) == 1:
                md = "".join(new_files)
                commit = md
                clipboard(md)
            commit = f"Add to blog: \n {commit}"
            git_push(commit)
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 🎉 {commit}")
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] File already exists 😶")


def blog():
    parser = argparse.ArgumentParser(
        description="Create file in _notes, move image in assets, convert to relative path, add share support, and push to git"
    )
    group_f = parser.add_mutually_exclusive_group()
    group_f.add_argument(
        "--preserve",
        "--P",
        help="Don't delete file if already exist",
        action="store_true",
    )
    group_f.add_argument(
        "--update",
        "--U",
        help="force update : delete all file and reform.",
        action="store_true")
    parser.add_argument(
        "--filepath",
        "--F",
        help="Filepath of the file you want to convert",
        action="store",
        required=False,
    )
    parser.add_argument(
        "--Git", "--G", help="No commit and no push to git", action="store_true"
    )
    args = parser.parse_args()
    ori = args.filepath
    delopt = False
    if args.preserve:
        delopt = True
    force = args.update
    ng = args.Git
    if ori :
        if os.path.exists(ori): #Share ONE
            convert_one(ori, delopt, ng)
        else:
            print(f"Error : {ori} doesn't exist.")
            return
    else:
        convert_all(delopt, ng, force)


if __name__ == "__main__":
    blog()
