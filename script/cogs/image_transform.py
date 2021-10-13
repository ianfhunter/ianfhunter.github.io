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

def flags_transform(line,flag):
    img_flags = re.search("[\|\+\-](.*)[]{1,2})]", flag)
    if img_flags:
        img_flags = img_flags.group(0)
        img_flags = img_flags.replace("|", "")
        img_flags = img_flags.replace("]", "")
        img_flags = img_flags.replace(")", "")
        img_flags.replace("(", "")
    else:
        img_flags = ""
    link = re.search("(\[{2}|\().*\.(png|jpg|jpeg|gif)", flag)
    final_text = link.group(0)
    final_text = final_text.replace("(", "")
    final_text = final_text.replace("%20", " ")
    final_text = final_text.replace("[", "")
    final_text = final_text.replace("]", "")
    final_text = final_text.replace(")", "")
    final_text = os.path.basename(final_text)
    image_path = get_image(final_text)
    if image_path:
        shutil.copyfile(image_path, f"{img}/{final_text}")
        final_text = f"../assets/img/{final_text}"
        IAL= f"[{img_flags}]({final_text})"
        line = line.replace(flag, IAL)
    return line

def move_img(line):
    flags = re.search("(\[{2}|\().*\.(png|jpg|jpeg|gif)(\|[-+].*)?\]{2}", line)
    flags = flags.group().split('!')
    if len(flags) > 1:
        for flag in flags:
            line = flags_transform(line, flag)
    else:
        flags = flags[0]
        line = flags_transform(line, flags)
    return line


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
    if re.search("\[(.*)]\((.*)\)", final_text) :
        links=re.search("\[(.*)]\((.*)\)", final_text).group().split()
        if len(links) > 1:
            for link in links:
                if not re.search('https?:\/\/', link) or link == '':
                    line = transform_link(line, link)
        else:
            links = links[0]
            if not re.search('https?:\/\/', links):
                line = transform_link(line, links)
    return line

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