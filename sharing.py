import re
import sys
import os
from dotenv import dotenv_values
from pathlib import Path
import shutil
from datetime import datetime


BASEDIR = os.path.abspath(os.path.dirname(__file__))
env = dotenv_values(Path(f"{BASEDIR}/.env"))
path = Path(f"{BASEDIR}/.git")  # GIT SHARED
vault = Path(env["vault"])
post = Path(f"{BASEDIR}/_notes")
img = Path(f"{BASEDIR}/assets/img/")


def get_token_end(final_text):
    token = ""
    if re.search(".+\{(.*)\}", final_text):
        token = re.search(".+\{(.*)\}", final_text)
        token = token.group(1)
        token = " {" + token + "}"
    return token


def get_token_start(final_text):
    token = ""
    if final_text.startswith("{"):
        token = re.search("\{(.*)\}.+", final_text)
        token = token.group(1)
        token = "{" + token + "} "
    return token


def get_table_end(final_text):
    table = ""
    if re.search("(\]{2}|\))(.*)", final_text):
        tab = re.search("(\]{2}|\))(.*)", final_text)
        tab = tab.group(0)
        if "|" in tab:
            table = " |"
    return table


def get_start_table(final_text):
    table = ""
    if re.search("\|[\[|\(](.*)", final_text):
        tab = re.search("\|[\[|\(](.*)", final_text)
        tab = tab.group(0)
        if "|" in tab:
            table = "| "
    return table


def get_tab_token(final_text):
    token_end = get_token_end(final_text)
    table_end = get_table_end(final_text)
    table_start = get_start_table(final_text)
    token_start = get_token_start(final_text)
    return token_end, table_end, table_start, token_start


def retro(file):
    # Yes, It's stupid, but it's work.
    # It permit to compare the file in file diff with len(file)
    # Remove newline and comment

    notes = []
    for n in file:
        if n != "  \n" or n != "  " or n != "\n":
            n = n.replace("  \n", "")
            n = n.replace("\n", "")
            notes.append(n)
    notes = [i for i in notes if i != ""]
    notes = [i for i in notes if not "%%" in i]
    notes= [i for i in notes if not "date:" in i]
    return notes


def diff_file(file):
    file_name = os.path.basename(file)
    if check_file(file_name) == "EXIST":
        vault = open(file, "r", encoding="utf-8")
        notes = open(Path(f"{BASEDIR}/_notes/{file_name}"), "r", encoding="utf-8")
        vault_data = vault.readlines()
        notes_data = notes.readlines()
        vault.close()
        notes.close()
        vault = retro(vault_data)
        notes = retro(notes_data)
        if len(vault) == len(notes):
            return False
        else:
            return True


def delete_file(filepath):
    for file in os.listdir(post):
        filepath = os.path.basename(filepath)
        filecheck = os.path.basename(file)
        if filecheck == filepath:
            os.remove(Path(f"{BASEDIR}\_notes\\{file}"))
            return True
    return False


def get_image(image):
    for sub, dirs, files in os.walk(vault):
        for file in files:
            filepath = sub + os.sep + file
            if image in file:
                return filepath


def move_img(line):
    token, table, table_start, token_start = get_tab_token(line)
    img_flags = re.search("\|(.*)(]{2}|\))", line)
    if img_flags:
        img_flags = img_flags.group(0)
        img_flags = img_flags.replace("|", "")
        img_flags = img_flags.replace("]", "")
        img_flags = img_flags.replace(")", "")
    else:
        img_flags = ""
    final_text = re.search("(\[{2}|\().*\.(png|jpg|jpeg|gif)", line)
    final_text = final_text.group(0)
    final_text = final_text.replace("(", "")
    final_text = final_text.replace("%20", " ")
    final_text = final_text.replace("[", "")
    final_text = final_text.replace("]", "")
    image_path = get_image(final_text)
    if image_path:
        shutil.copyfile(image_path, f"{img}/{final_text}")
        final_text = f"../assets/img/{final_text}"
        final_text = f"{table_start}{token_start}![{img_flags}]({final_text}){token}{table}  \n  \n"
    else:
        final_text = line
    return final_text


def relative_path(data):
    data = data.rstrip() + ".md"
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


def convert_internal(line):
    ft = line.replace("[", "")
    ft = ft.replace("]", "")
    ft = ft.replace("!", "")
    ft = ft.replace("(", "")
    ft = ft.replace(")", "")
    ft = ft.rstrip()
    file = relative_path(ft)
    destination = f"{BASEDIR}/_notes/{ft}"
    line_final = ""
    if file:
        if file.endswith(f"{ft}.md"):
            check = check_file(file)
            if check != "EXIST":
                file_convert(file)
        line_final = f"[[{destination}\|{ft}]]"
    return line_final


def transluction_note(line):
    # If file (not image) start with "![[" : transluction with lsn-transclude (exclude image from that)
    # Note : Doesn't support partial transluction for the moment ; remove title
    final_text = line
    if re.match("\!\[{2}", line) and not re.match("(png|jpg|jpeg|gif)", line):
        final_text = line.replace("!", "")  # remove "!"
        final_text = re.sub("#(.*)]]", "]]", final_text)
        final_text = re.sub("]]", "::rmn-transclude]]", final_text)
        # Add transluction_note
    return final_text


def math_replace(line):
    if re.match("\$(?!\$)(.*)\$", line) and not re.match("$$(.*)$$", line):
        line = line.replace("$", "$$")
    return line


def file_convert(file):
    file_name = os.path.basename(file)
    if not "_notes" in file:
        if not os.path.exists(Path(f"{BASEDIR}/_notes/{file_name}")):
            data = open(file, "r", encoding="utf-8")
            final = open(Path(f"{BASEDIR}/_notes/{file_name}"), "w", encoding="utf-8")
            lines = data.readlines()
            if "share: false" in lines:
                return False
            data.close()
            date= re.compile('date:(.*)')
            date_check=list(filter(date.match, lines))
            if len(date_check) == 0: #Prevent to multi add date
                lines.insert(2, f"date: {datetime.now().strftime('%d-%m-%y')}\n")
            for ln in lines:
                final_text = ln.replace("\n", "  \n")
                final_text = transluction_note(final_text)
                final_text = math_replace(final_text)
                if re.search("\%\%(.*)\%\%", final_text):
                    # remove comments
                    final_text = "  \n"
                elif re.search("==(.*)==", final_text):
                    final_text = re.sub("==", "[[", final_text, 1)
                    final_text = re.sub("( ?)==", "::highlight]] ", final_text, 2)
                elif re.search(
                    "(\[{2}|\().*\.(png|jpg|jpeg|gif)", final_text
                ):  # CONVERT IMAGE
                    final_text = move_img(final_text)
                elif (
                    "\\" in final_text.strip()
                ):  # New line when using "\n" in obsidian file
                    final_text = "  \n"
                elif re.search("(\[{2}|\[).*", final_text):
                    # Escape pipe for link name
                    final_text = final_text.replace("|", "\|") + "  \n"
                final.write(final_text)
            final.close()
            return True
        else:
            return False
    else:
        return False


def search_share(option=0):
    filespush = []
    check = False
    for sub, dirs, files in os.walk(vault):
        for file in files:
            filepath = sub + os.sep + file
            if filepath.endswith(".md"):
                data = open(filepath, "r", encoding="utf-8")
                yaml = data.readlines()
                data.close()
                for ln in yaml:
                    if "share: true" in ln:
                        if option == 1:
                            if diff_file(filepath):
                                delete_file(filepath)
                        if option == 2:
                            delete_file(filepath)
                        check = file_convert(filepath)
                        destination = dest(filepath)
                        if check:
                            filespush.append(destination)
    return filespush


def convert_to_github():
    """
    Create file in _notes, move image in assets, convert to relative path, add share support, and push to git
    ----
    Usage
    -----
        python3 sharing (filepath) (options)
        Optional option:
            - --F : Don't delete file if already exist (prevent update)
            - --f : Force update (delete all file and reform)
            - help : print help message
            - filepath: convert just one file
            - --G : no commit and no push to github.
    """
    if len(sys.argv) >= 2:
        if sys.argv[1] == "help":
            print(help(convert_to_github))
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting convert")
            ori = sys.argv[1]
            delopt = ""
            ng = ""
            if "--F" in sys.argv:
                delopt = "--F"
            elif "--f" in sys.argv:
                delopt = "--f"
            if "--G" in sys.argv:
                ng = "--G"
            if os.path.exists(ori):
                if delopt != "--F":
                    print(
                        f"[{datetime.now().strftime('%H:%M:%S')}] Convert {ori} with update"
                    )
                    delete_file(ori)
                else:
                    print(
                        f"[{datetime.now().strftime('%H:%M:%S')}] Convert {ori} (without update)"
                    )
                check = file_convert(ori)
                if check and ng != "--G":
                    print(
                        f"[{datetime.now().strftime('%H:%M:%S')}] Add {ori} to github"
                    )
                    COMMIT = f"{ori} to blog"
                    try:
                        import git

                        repo = git.Repo(Path(f"{BASEDIR}/.git"))
                        destination = dest(ori)
                        repo.git.add(".")
                        repo.git.commit("-m", f"{COMMIT}")
                        repo.git.push("origin", "HEAD:refs/for/master")
                        print(
                            f"[{datetime.now().strftime('%H:%M:%S')}] {ori} pushed successfully 🎉"
                        )
                    except ImportError:
                        print(
                            "[{datetime.now().strftime('%H:%M:%S')}] Please, use another way to push your change"
                        )
                elif check and ng == "--G":
                    print(
                        f"[{datetime.now().strftime('%H:%M:%S')}] 🎉 Successfully converted {ori}"
                    )
                else:
                    print(
                        f"[{datetime.now().strftime('%H:%M:%S')}] Ori already converted"
                    )

            else:
                if delopt == "--F":
                    print(
                        f"[{datetime.now().strftime('%H:%M:%S')}] Convert without update"
                    )
                    new_files = search_share()
                elif delopt == "--f":
                    print(
                        f"[{datetime.now().strftime('%H:%M:%S')}] Convert with force update"
                    )
                    new_files = search_share(2)
                else:
                    print(
                        f"[{datetime.now().strftime('%H:%M:%S')}] Convert with update"
                    )
                    new_files = search_share(1)
                commit = "Add to blog:\n"
                if len(new_files) > 0:
                    for md in new_files:
                        commit = commit + "\n — " + md
                    if ng != "--G":
                        try:
                            import git
                            repo = git.Repo(Path(f"{BASEDIR}/.git"))
                            repo.git.add(".")
                            repo.git.commit("-m", f"git commit {commit}")
                            origin = repo.remote(name="origin")
                            origin.push()
                            print(
                                f"[{datetime.now().strftime('%H:%M:%S')} {commit}\n pushed successfully 🎉"
                            )
                        except ImportError:
                            print(
                                f"[{datetime.now().strftime('%H:%M:%S')}] Please use another way to push your project"
                            )
                    else:
                        print(
                            f"[{datetime.now().strftime('%H:%M:%S')}] 🎉 Converted {commit}"
                        )
                else:
                    print(
                        f"[{datetime.now().strftime('%H:%M:%S')}] File already exists 😶"
                    )

    else:
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] Starting Convert with update and push "
        )
        new_files = search_share(1)
        commit = "Add to blog :\n"
        if len(new_files) > 0:
            try:
                import git

                repo = git.Repo(Path(f"{BASEDIR}/.git"))
                for md in new_files:
                    commit = commit + "\n — " + md
                repo.git.add(A=True)
                repo.git.commit(m=commit)
                origin = repo.remote("origin")
                origin.push()
                print(
                    f"[{datetime.now().strftime('%H:%M:%S')}] {commit}\n pushed successfully 🎉"
                )
            except ImportError:
                print(
                    f"[{datetime.now().strftime('%H:%M:%S')}] Please use working copy"
                )
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] File already exists 😶")


if __name__ == "__main__":
    convert_to_github()
