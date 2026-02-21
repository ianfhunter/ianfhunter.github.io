from ast import Bytes
import re
import frontmatter
from datetime import datetime, timezone
import dateutil.parser as dp
import calendar
from yaml.constructor import ConstructorError
from os import walk, path, rename, sep, mkdir
from shutil import copyfile, rmtree
from io import BytesIO

JEKYLL_POSTS_FOLDER = "_posts/"
JEKYLL_ASSET_FOLDER = "assets/img/notes/"
OBSIDIAN_ASSET_FOLDER = "my-vault/00-09 System/00 Assets"

def get_new_name(f, old_f):
    post_format = lambda x : x.lower().replace(" ", "-")

    acceptable_pattern = r"[0-9][0-9][0-9][0-9]\-[0-9][0-9]\-[0-9][0-9]\-[^\s]*\.md"
    p = re.compile(acceptable_pattern)
    valid_form = p.match(f)
    new_f = f
    if not valid_form:
        post = frontmatter.load(old_f)
        date = post.get("date", None)
        if date is None:
            uxt = path.getmtime(old_f)
            date = datetime.fromtimestamp(uxt).strftime("%Y-%m-%d")
            
        date = dp.parse(date).strftime("%Y-%m-%d")
        ff = f"{date}-{post_format(f)}"

        new_f = path.join(JEKYLL_POSTS_FOLDER, ff)

        assert p.match(ff)

        # rename(old_f, new_f)
    return new_f

def copy_over_published_markdown(f, d):
    old_f = path.join(d, f)
    print(f"Copy Published Markdown::File: {old_f}")
    try:
        post = frontmatter.load(old_f)
        publishable = post.get("share", False)
        if publishable:
            print(f"{f}:")
            new_f = get_new_name(f, old_f)

            print("\t[name]", new_f)
            copyfile(old_f, new_f)
            return new_f
    except ConstructorError:
        print("Error parsing:", old_f)
        return None
        
def improve_metadata(f):
    post = frontmatter.load(f)
    post["author"] = "ianfhunter"
    post["math"] = True
    post["mermaid"] = True
    # post["title"] = 
    # post["date"] = 
    # with open(f,"w") as w:
    b = BytesIO()
    frontmatter.dump(post, b)
    with open(f, "wb") as w:
        w.write(b.getbuffer())
    

def copy_over_referenced_images(f):
    with open(f,"r") as r:
        content = r.read()
        # print(content)
        markdown_pattern = r"\!\[\[([a-zA-Z0-9\_\s]+\.(png|gif|jpg))\]\]"
        p = re.compile(markdown_pattern)
        g = re.findall(p, content)
        if len(g) > 0:
            for img, ext in g:
                print(f"\t[img]: {img}")
                src_path = path.join(OBSIDIAN_ASSET_FOLDER, img)
                dst_path = path.join(JEKYLL_ASSET_FOLDER, img)
                
                if path.exists(src_path):
                    copyfile(src_path, dst_path)
                
                # print("Before:", content)
                content = re.sub(p, f"<img src='/assets/img/notes/{img}' />", content, 1)

    with open(f, "w") as w:
        w.write(content)

def fix_internal_links(f):
    # Replace [[Internal]] and [[Internal|Text]] 
    # With
    # [Text](AbsoluteInternal)

    linkify = lambda x : "../"+ x.lower().replace(" ","-")

    with open(f,"r") as r:
        content = r.read()
        markdown_pattern = r"\[\[([a-zA-Z0-9\_\s]+)\|?([a-zA-Z0-9\_\s]*)\]\]"
        p = re.compile(markdown_pattern)
        g = re.findall(p, content)
        if len(g) > 0:
            for reference, alt_text in g:
                if alt_text == '':
                    att = reference
                else:
                    att = alt_text
                reference = linkify(reference)
                content = re.sub(p, f"[{att}]({reference})", content, 1)


    with open(f, "w") as w:
        w.write(content)


def main():
    # TODO: Copy from my-vault to _posts
    # TODO: Copy images over also
    # Clear out post folder
    rmtree(JEKYLL_POSTS_FOLDER, ignore_errors=True)
    rmtree(JEKYLL_ASSET_FOLDER, ignore_errors=True)
    if not path.exists(JEKYLL_POSTS_FOLDER):
        mkdir(JEKYLL_POSTS_FOLDER)
        mkdir(JEKYLL_ASSET_FOLDER)

    for (dirpath, dirnames, filenames) in walk("my-vault"):
        for f in filenames:
            if ".md" in f:
                ff = copy_over_published_markdown(f, dirpath)
                if ff is None:
                    continue
                improve_metadata(ff)
                copy_over_referenced_images(ff)
                fix_internal_links(ff)
            

if __name__ == "__main__":
    main()
