---
title: Test page to see how the raw markdown is rendered
tags: python, script, Obsidian
category: Obsidian
flux: true
date: 31-10-2020
toc: true
---

⚠️ The script and site are not a replacement for [Obsidian Publish](https://obsidian.md/publish), which is a much more efficient way to share Obsidian files.

---

# Get Started

- You first need to create a template using [YAFPA-blog](https://github.com/Mara-Li/yet-another-free-publish-alternative)
- After, do `pip install YAFPA`

## Requirements

The script uses : 
- [PyGithub](https://github.com/PyGithub/PyGithub)
- [Python-dotenv](https://github.com/theskumar/python-dotenv)
- [python-frontmatter](https://github.com/eyeseast/python-frontmatter)
- [Pyperclip](https://github.com/asweigart/pyperclip) on Windows/MacOS/Linux | IOS : Pasteboard (Pyto) or clipboard (Pythonista) | Clipboard function doesn't work (yet) on a-shell.

You can install all with `pip install -r requirements.txt`

## Environment

The first time you use the script, it will ask you three things :
- Your vault path (absolute path !)
- The path of the blog (absolute too !)
- The link of your blog, as `https://my-awesome-blog.netlify.app/`

You can reconfig the path with `yafpa --config`

The file will be created in `$HOME/.YAFPA-env` (`~/.YAFPA-env`)  so you can edit it directly. 

# Script
usage: yafpa [-h] [--preserve | --update] [--filepath FILEPATH] [--git] [--keep] [--config]

Create file in folder, move image in assets, convert to relative path, add share support, and push to git

optional arguments:
  - `-h, --help`: show this help message and exit
  - `--preserve, --p, --P` : Don't delete file if already exist
  - `--update, --u, --U` : force update : delete all file and reform.
  - `--filepath FILEPATH, --f FILEPATH, --F FILEPATH `: Filepath of the file you want to convert
  - `--git, --g, --G` : No commit and no push to git
  - `--keep, --k` : Keep deleted file from vault and removed shared file
  - `--config, --c` : Edit the config file


## Checking differences
The script will convert all file with `share:true` and check if the contents 
are differents with the version in `_notes`. The only things that are 
ignored is the contents of the metadata. If you want absolutely change the 
metadata you can:
- Use `yafpa --file <filepath>` directly
- Use `--u` to force update all file 
- Continue to work on the file before pushing it.
- Add a newline
- Manually delete the file 
- Add or edit the metadata keys (unless `date`/`title`/`created`/`update`/`link`). 

:warning: In case you have two files with the same name but :
- In different folder
- With different sharing statut
The script will bug because **I don't check folder** (It's volontary). In this unique case, you need to rename one of the files. 

## Options
### Share all
`yafpa` and all `yafpa` option without `--F FILEPATH` will automatically read all file in your vault to check the `share: true` key in metadata (frontmatter YAML).

By default, the script will check the difference between line [(*cf checking difference*)](README.md#checking-differences), and convert only the file with difference. You can use `--u` to force update. 

### Share only a file
The command will be : `yafpa --F filepath`

The file to be shared does not need to contain `share: true` in its YAML, and will be updated no matter what.

## How it works

The script : 
- Moves file (with `share: true` frontmatter or specific file) in the `_notes` folder
- Moves image in `assets/img` and convert (with alt support)
- Converts highlight (`==mark==` to `[[mark::highlight]]`)
- Converts "normal" writing to GFM markdown (adding `  \n` each `\n`)
- Supports non existant file (adding a css for that 😉)
- Supports image flags css (Lithou snippet 🙏)
- Support normal and external files (convert "normal markdown link" to 
  "wikilinks")
- Edit link to support transluction (if not `embed: False`)
- Remove block id (no support)
- Add CSS settings for inline tags (no link support) ; Tags are : class = .hash ; id = #tag_name (so you can style each tags you use)
- Frontmatter :  Update the date. If there is already a `date` key, save it to `created` and update `date`.
- Frontmatter : In absence of title, add the file's title.
- Copy the link to your clipboard if one file is edited.
- ⭐ Admonition convertion to "callout inspired notion"
- Update the frontmatter in the original file, adding the link and change `share` to true if one file is shared.

Finally, the plugin will add, commit and push if supported.

Note : The clipboard may not work in your configuration. I have (and can) only test the script on IOS and Windows, so I use `pyperclip` and `pasteboard` to do that. If you are on MacOS, Linux, Android, please, check your configuration on your python and open an issue if it doesn't work. 
Note : I **can't** testing on these 3 OS, so I can't create a clipboard option on my own. 

### Custom CSS 
You can add CSS using the file (custom.css)[https://github.com/Mara-Li/yet-another-free-publish-alternative/blob/master/assets/css/custom.css]. The plugin [Markdown Attribute](https://github.com/valentine195/obsidian-markdown-attributes) allow to use the creation of inline css. 
Some information about this :
- You need to add `:` after the first `{`
- The inline IAL work only if there is stylized markdown. In absence, the text will be bolded. 
- It won't work with highlight (removed automatically by the script)
 
⚠️ As I use CodeMirror Options and Contextual Typography, I warn you : the use of `#tags` to stylize the text before it doesn't work with my build. So, as an option to don't have a random tag in a text, you can use `custom.css` to remove it with `display: none` (you can have an example with `#left`). 

### Frontmatter settings
- `share: true` : Share the file
- `embed: false` : remove the transluction (convert to normal wikilinks)
- `update: false` : Don't update the file at all after the first push
- `current: false` : Don't update the date
- `private: true` : Use the `_private` folder collection instead of the `_notes` collection.


### Admonition 
As admonition is very tricky, I choose to convert all admonition to a "callout Notion".
The script will : 
- Remove codeblock for admonition codeblocks
- Convert ` ```ad-``` ` to ```!!!ad-```
- Bold title and add a IAL `{: .title}`

JavaScript will niced all things.

⚠️ As always with markdown, you will see some problem with new paragraph inside admonition. You can use `$~$` to fake line. The script will automatically add this.
Also, you can add emoji on title to add some nice formatting.


### Obsidian 
→ Please use Wikilinks with "short links" (I BEG YOU)
You can integrate the script within obsidian using the nice plugin [Obsidian ShellCommands](https://github.com/Taitava/obsidian-shellcommands).

You could create two commands :
1. `share all` : `yafpa`
2. `share one` : `yafpa --f {{file_path:absolute}}`

You can use :
- [Customizable Sidebar](https://github.com/phibr0/obsidian-customizable-sidebar)
- [Obsidian Customizable Menu](https://github.com/kzhovn/obsidian-customizable-menu)

To have a button to share your file directly in Obsidian !
