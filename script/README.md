**Table Of Content**
- [Goal](#goal)
- [Get Started](#get-started)
  * [Requirements](#requirements)
  * [Environment](#environment)
- [Script](#script)
  * [Checking differences](#checking-differences)
  * [Options](#options)
    + [Share all](#share-all)
    + [Share only a file](#share-only-a-file)
  * [How it works](#how-it-works)
    + [Custom CSS](#custom-CSS)
    + [Frontmatter settings](#frontmatter-settings)
    + [Admonition](#admonition)
    + [IOS Shortcuts](#ios-shortcuts)
    + [IOS](#ios)
    + [Obsidian](#obsidian)
  * [Windows bonus](#windows-bonus)
---
  
⚠️ The script and site are not a replacement for [Obsidian Publish](https://obsidian.md/publish), which is a much more efficient way to share Obsidian files.


# Get Started

The best way is to use the template with the **master branch** and delete files in `_notes` (which are the original files).
Otherwise, just copy `sharing.py` script and use it for your own template.

## Requirements

The script uses : 
- [PyGithub](https://github.com/PyGithub/PyGithub)
- [Python-dotenv](https://github.com/theskumar/python-dotenv)
- [python-frontmatter](https://github.com/eyeseast/python-frontmatter)
- [Pyperclip](https://github.com/asweigart/pyperclip) on Windows/MacOS/Linux | IOS : Pasteboard (Pyto) or clipboard (Pythonista) | Clipboard function doesn't work (yet) on a-shell.

You can install all with `pip install -r requirements.txt`

## Environment
You need a `.env` file in root containing the path to your obsidian vault and the link to your blog. The file looks like this :
```
vault="G:\path\vault\"
blog="https://your-website.netlify.app/notes/"
```

# Script
Usage: `sharing.py  [-h] [--Preserve | --update] [--filepath FILEPATH] [--Git]`

Create file in `_notes`, move image in assets, convert to relative path, add share support, and push to git

Optional arguments:
-  `-h`, `--help` : Show this help message and exit  
- `--Preserve`, `--P` : Don't delete file if already exist  
- `--update`, `--U` : Force update : delete all file and reform.  
- `--filepath FILEPATH`, `--F FILEPATH` : Filepath of the file you want to 
  convert  
- `--Git`, `--G` : No commit and no push to git (work for github, gitlab...) 

## Checking differences
The script will convert all file with `share:true` and check if the contents 
are differents with the version in `_notes`. The only things that are 
ignored is the contents of the metadata. If you want absolutely change the 
metadata you can:
- Use `share --file <filepath>` directly
- Use `--u` to force update all file 
- Continue to work on the file before pushing it.
- Add a newline with `$~$` or `<br>` (it will be not converted and displayed on page / obsidian so...)
- Manually delete the file 
- Add or edit the metadata keys (unless `date`/`title`/`created`/`update`/`link`). 

:warning: In case you have two files with the same name but :
- In different folder
- With different sharing statut
The script will bug because **I don't check folder** (It's volontary). In this unique case, you need to rename one of the files. 

## Options
### Share all
By adding, in the yaml of your file, the key `share: true`, you allow the script to publish the file. In fact, the script will read all the files in your vault before selecting the ones meeting the condition.

By default, the script will check the difference between line [(*cf checking difference*)](README.md#checking-differences), and convert only the file with difference. You can use `--u` to force update. 

### Share only a file

The file to be shared does not need to contain `share: true` in its YAML.

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

Note : The clipboard maybe not work in your configuration. I have (and can) only test the script on IOS and Windows, so I use `pyperclip` and `pasteboard` to do that. If you are on MacOS, Linux, Android, please, check your configuration on your python and open an issue if it doesn't work. 
Note : I **can't** testing on these 3 OS, so I can't create a clipboard option on my own. 

### Custom CSS 
You can add CSS using the file (custom.css)[/assets/css/custom.css]. The plugin [Markdown Attribute](https://github.com/valentine195/obsidian-markdown-attributes) allow to use the creation of inline css. 
Some information about this :
- You need to add `:` after the first `{`
- The inline IAL work only if there is stylized markdown. In absence, the text will be bolded. 
- It won't work with highlight (removed automatically by the script)

:warning: As I use CodeMirror Options and Contextual Typography, I warn you : the use of `#tags` to stylize the text before it doesn't work with my build. So, as an option to don't have a random tag in a text, you can use `custom.css` to remove it with `display: none` (you can have an example with `#left`). 

### Frontmatter settings
- `share: true` : Share the file
- `embed: false` : remove the transluction (convert to normal wikilinks)
- `update: false` : Don't update the file at all. 
- `current: false` : Don't update the date
- `private: true` : Use the `_private` folder collection instead of the `_notes` collection.


### Admonition 
As admonition is very tricky, I choose to convert all admonition to a "callout Notion".
The script will : 
- Remove codeblock for admonition codeblocks
- Convert ` ```ad-``` ` to ```!!!ad-```
- Bold title and add a IAL `{: .title}`

JavaScript will niced all things.

⚠ As always with markdown, you will see some problem with new paragraph inside admonition. You can use `$~$` to fake line. The script will automatically add this.
Also, you can add emoji on title to add some nice formatting.

### IOS Shortcuts

### IOS
To use the shortcuts, you need : 
- [Pyto](https://apps.apple.com/fr/app/pyto-python-3/id1436650069)
- [Toolbox Pro](https://apps.apple.com/fr/app/toolbox-pro-for-shortcuts/id1476205977)
- [Working Copy](https://workingcopyapp.com/)

The main shortcut is on RoutineHub (more pratical for version update) : [share one file](https://routinehub.co/shortcut/10044/)
(it's equivalent to `share <filepath>`)

There is another shortcuts to "share all" files : [Share all true file in vault](https://routinehub.co/shortcut/10045/)
(it's equivalent to `share` without arguments)

Note : You first need to clone the repo with Working Copy and install all requirements. 


To use the [shortcuts](https://routinehub.co/shortcut/10151/), you need :
- [a-shell](https://holzschu.github.io/a-Shell_iOS/) (Free)
- [Working Copy](https://workingcopyapp.com/)

Before running the shortcuts, you need to install all requirements, aka :
```
jump <vault>
cd script
pip install -r requirements.txt
```


For the moment I can't create a shortcuts to share only one file BUT ! You can using `a-shell` as you do in a normal terminal, aka : 
```
jump <vault>
python3 <vault-path>/script/sharing.py <file>
```

You could also create an alias for sharing using `~/.profile`: 
`alias share='python3 <git-folder>/script/sharing.py'`

### Obsidian 
→ Please use Wikilinks with "short links" (I BEG YOU)
You can integrate the script within obsidian using the nice plugin [Obsidian ShellCommands](https://github.com/Taitava/obsidian-shellcommands).

You could create two commands :
1. `share all` : `python3 path/to/your/script/sharing.py`
2. `share one` : `python3 path/to/your/script/sharing.py --f {{file_path:absolute}}`

You can use :
- [Customizable Sidebar](https://github.com/phibr0/obsidian-customizable-sidebar)
- [Obsidian Customizable Menu](https://github.com/kzhovn/obsidian-customizable-menu)
To have a button to share your file directly in Obsidian !

## Windows bonus

You can add the script as an alias in Powershell via :
`notepad $PROFILE`
Then, by adding at the end of the file :
```sh
function sharepython ([string]$file) { python3 "path\to\site\folder\sharing.py "$file""}
New-Alias share sharepython
```
So, finally you can just use `share` in powershall to convert, push, commit, your file.
Also, options are supported with that.
