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
        img_flags=img_flags.group(0)
        img_flags=img_flags.replace("|", "")
        img_flags=img_flags.replace("]", "")
        img_flags=img_flags.replace(")", "")
    else:
        img_flags=""
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
        final_text = (
            f"{table_start}{token_start}![{img_flags}]({final_text}){token}{table}  \n  \n"
        )
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
    check = ""
    for file in os.listdir(post):
        if filepath == file:
            check = "EXIST"
    return check


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
            file = os.path.basename(file)
            check = check_file(file)
            if check != "EXIST":
                file_convert(file)
        line_final = f"[[{destination}\|{ft}]]"
    return line_final


def file_convert(file):
    file_name = os.path.basename(file)
    if not "_notes" in file:
        if check_file(file_name) != "EXIST":
            data = open(file, "r", encoding="utf-8")
            final = open(Path(f"{BASEDIR}/_notes/{file_name}"), "w", encoding="utf-8")
            lines = data.readlines()
            if "share: false" in lines:
                return False
            data.close()
            for ln in lines:
                final_text = ln.replace("\n", "  \n")

                if re.search("\%\%(.*)\%\%", final_text):
                    #remove comments
                    final_text="  \n"
                elif re.search("==(.*)==", final_text):
                    final_text=re.sub("==", "[[", final_text, 1)
                    final_text=re.sub("( ?)==", "::highlight]] ", final_text, 2)
                elif re.search(
                    "(\[{2}|\().*\.(png|jpg|jpeg|gif)", final_text
                ):  # CONVERT IMAGE
                    final_text = move_img(final_text)
                elif (
                    "\\" in final_text.strip()
                ):  # New line when using "\n" in obsidian file
                    final_text = "  "
                elif re.search("(\[{2}|\[).*", final_text):
                    # Add internal_link to blog too !
                    ft = re.search("(\[{2}|\[).*", final_text)
                    ft = ft.group(0)
                    link = convert_internal(ft)
                    token, table, table_start, token_start = get_tab_token(
                        final_text
                    )
                    final_text = (
                        table_start
                        + token_start
                        + final_text.replace("|", "\|")
                        + token
                        + table
                        + "  \n"
                    )

                final.write(final_text)
            final.close()
            return True
        else:
            return False
    else:
        return False


def search_share(option=0):
    filespush = []
    for sub, dirs, files in os.walk(vault):
        for file in files:
            filepath = sub + os.sep + file
            if filepath.endswith(".md"):
                data = open(filepath, "r", encoding="utf-8")
                yaml=data.readlines()
                data.close()
                for ln in yaml:
                    if "share: true" in ln:
                        if option == 1:
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
            - help : print help message
            - filepath: convert just one file
            - --G : no commit and no push to github.
    """
    if len(sys.argv) >= 2:
        if sys.argv[1] == "help":
            print(help(convert_to_github))
        else:
            print("Starting convert")
            ori = sys.argv[1]
            delopt = ""
            ng = ""
            if "--F" in sys.argv:
                delopt = "--F"
            if "--G" in sys.argv:
                ng = "--G"
            if os.path.exists(ori) and ori != "--F":
                delete_file(ori)
                check = file_convert(ori)
                if check and ng != "--G":
                    COMMIT = f"{dest} to blog"
                    try:
                        import git
                        repo = git.Repo(Path(f"{BASEDIR}/.git"))
                        destination = dest(ori)
                        repo.git.add(".")
                        repo.git.commit('-m', f'git commit {ori}')
                        repo.git.push("origin", "HEAD:refs/for/master")
                        print(f"{ori} pushed successfully 🎉")
                    except ImportError:
                        print("Please, use Working Copy to push your change")
                elif check and ng == "--G":
                    print(f"converted {dest} to blog")
            elif delopt == "--F" or ori == "--F":
                new_files = search_share()
                commit = "Add to blog:"
                if len(new_files) > 0:
                    if ng !="--G":
                        try:
                            import git
                            repo = git.Repo(Path(f"{BASEDIR}/.git"))
                            for md in new_files:
                                commit = commit + "\n — " + md
                            repo.git.add(".")
                            repo.git.commit('-m', f'git commit {commit}')
                            origin = repo.remote(name='origin')
                            origin.push()
                            print(f"\n{commit}\n pushed successfully 🎉")
                        except ImportError:
                            print("Please use Working Copy to push your project")
                    else:
                        print(f"Converted {commit}")
                else:
                    print("File already exists 😶")
            elif ori == "--G" or ng =="--G" and delopt != "--F":
                new_files = search_share(1)
                commit = "Add to blog:"
                if len(new_files) > 0:
                    print(f"Converted {commit}")
                else:
                    print("File already exists 😶")
            elif ng == "--G" and delopt == "--F":
                new_files = search_share()
                commit = "Add to blog:"
                if len(new_files) > 0:
                    print(f"Converted {commit}")
                else:
                    print("File already exists 😶")
    else:
        now = datetime.now().strftime("%H:%M:%S")
        print(f"[{now}] Starting Convert")
        new_files = search_share(1)
        commit = "Add to blog :"
        if len(new_files) > 0:
            try:
                import git
                repo = git.Repo(Path(f"{BASEDIR}/.git"))
                for md in new_files:
                    commit = commit + "\n — " + md
                repo.git.add(f'{BASEDIR}/_notes/*')
                repo.git.add(f'{BASEDIR}/assets/img/*')
                repo.git.commit(m=commit)
                origin = repo.remote('origin')
                origin.push()
                now=datetime.now().strftime("%H:%M:%S")
                print(f"[{now}] {commit}\n pushed successfully 🎉")
            except ImportError:
                print("Please use working copy")
        else:
            print("File already exists 😶")


if __name__ == "__main__":
    convert_to_github()

