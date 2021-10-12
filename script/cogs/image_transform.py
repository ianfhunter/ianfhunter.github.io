import os
import re
import shutil

from . import global_value as settings

vault = settings.vault
img = settings.img

def get_image(image):
    image = os.path.basename(image)
    for sub, dirs, files in os.walk(vault):
        for file in files:
            filepath = sub + os.sep + file
            if image in file:
                return filepath


def move_img(line):
    img_flags = re.search("[\|\+\-](.*)[]{1,2})]", line)
    if img_flags and not re.search("\-\d+", line):
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
    if ".excalidraw" in line:
        # take the png img from excalidraw
        line = line.replace(".excalidraw", ".excalidraw.png")
        line = line.replace(".md", "")
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
    if (
        re.search("\!\[", line)
        and not re.search("(png|jpg|jpeg|gif)", line)
        and not re.search("https", line)
    ):
        final_text = line.replace("!", "")  # remove "!"
        final_text = re.sub("#(.*)", "]]", final_text)
        final_text = re.sub("\\|(.*)", "]]", final_text)  # remove Alternative title
        final_text = re.sub("]]", "::rmn-transclude]]", final_text)
    return final_text