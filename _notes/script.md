---
title: Python Scripting
category: Setup
flux: true
---

⚠️ The script and site are not a replacement for [Obsidian Publish](https://obsidian.md/publish), which is a much more efficient way to share Obsidian files.

# Goal 
Having files written in Markdown on Obsidian, I created a python script in order to semi-automatically share some of my files, on a static site in JEKYLL.

The site uses [notenote.link](https://github.com/Maxence-L/notenote.link) (thanks to Maxence-L) template which is the easiest to set up with Netlify, but there's nothing stopping you to modify the css.

# Get Started

The best way is to fork the original template and delete files in `_notes` (which are the original files).
Otherwise, just copy `sharing.py` script and use it for your own template.

## Requirements

The script uses : 
- [PyGithub](https://github.com/PyGithub/PyGithub)
- [Python-dotenv](https://github.com/theskumar/python-dotenv)
- [python-frontmatter](https://github.com/eyeseast/python-frontmatter)
- [Pyperclip](https://github.com/asweigart/pyperclip) on Windows/MacOS/Linux | IOS : Pasteboard (Pyto) or clipboard (Pythonista)

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
- 
- Use `share --file <filepath>` directly
- Use `--u` to force update all file 
- Continue to work on the file before pushing it.
- Add a newline with `$~$` or `<br>` (it will be not converted and displayed on page / obsidian so...)
- Manually delete the file 
- Add or edit the metadata keys (unless `date`/`title`/`created`/`update`). 

:warning: In case you have two files with the same name but :
- In different folder
- With different sharing statut
The script will bug because **I don't check folder** (It's volontary). In this unique case, you need to rename one of the files. 

## Options
### Share all
By adding, in the yaml of your file, the key `share: true`, you allow the script to publish the file. In fact, the script will read all the files in your vault before selecting the ones meeting the condition.

By default, the script will check the difference between line [(*cf checking difference*)](https://github.com/Mara-Li/yes-another-free-publish/tree/owlly-house#checking-differences), and convert only the file with difference. You can use `--u` to force update. 

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
- Frontmatter :  Update the date. If there is already a `date` key, save it to `created` and update `date`.
- Frontmatter : In absence of title, add the file's title.
- Copy the link to your clipboard if one file is edited.
- ⭐ Admonition convertion to "callout inspired notion"

Finally, the plugin will add, commit and push if supported.

Note : The clipboard maybe not work in your configuration. I have (and can) only test the script on IOS and Windows, so I use `pyperclip` and `pasteboard` to do that. If you are on MacOS, Linux, Android, please, check your configuration on your python and open an issue if it doesn't work. 
Note : I **can't** testing on these 3 OS, so I can't create a clipboard option on my own. 

### Frontmatter settings
- `share: true` : Share the file
- `embed: false` : remove the transluction (convert to normal wikilinks)
- `update: false` : Don't update the file at all. 
- `current: false` : Don't update the date

You can totally use the `owlly-house` branch, who add more option in the yaml ; as :
- `flux: false` : remove the file from the feed
- `category` : Add a category for the category page ; `category: false` remove it from this page too.
- `resume` : Add a resume of the file in the feed. 

### Admonition 
As admonition is very tricky, I choose to convert all admonition to a "callout Notion".
The script will : 
- Remove codeblock for admonition codeblocks
- Convert ` ```ad-``` ` to ```!!!ad-```
- Bold title and add a IAL `{: .title}`

JavaScript will niced all things.

⚠ As always with markdown, you will see some problem with new paragraph inside admonition. You can use `$~$` to fake line. The script will automatically add this.
Also, you can add emoji on title to add some nice formatting.

!!!ad-note
**🍎 Title**{:.title}  
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi faucibus at ex in ultricies. Etiam ac sodales mi, non aliquam lorem. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Integer ac lectus quam. Proin sed velit eget dui aliquet sodales. Duis sed urna eleifend, dictum neque eu, elementum neque. Quisque efficitur, justo ut malesuada faucibus, magna libero tempor elit, at fermentum libero mauris aliquam magna. Quisque ultrices tortor nec enim bibendum sodales.  
$~$  
It supports latex : $1+1$ and *markdown* 


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
