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

## Environment
You need a `.env` file in root containing the path to your obsidian vault. The file looks like this :
```
vault="G:\path\vault\"
```

# Script
There are several way to use the script :
- `python3 sharing.py` directly to convert, commit and push all file containing `share: true` in the frontmatter
- `python3 sharing.py <file>` to convert specific file (without using the frontmatter)

You can use some option :
- `--F` : Don't delete file if already exist.
- `--G` : Prevent git to commit and push

## Options

### Share all
By adding, in the yaml of your file, the key `share: true`, you allow the script to publish the file. In fact, the script will read all the files in your vault before selecting the ones meeting the condition.

By default, the script will delete and rewrite all file with `share: true`.

### Share only a file

The file to be shared does not need to contain `share: true` in its YAML. 

## Functionnement

The script : 
- Moves file (with `share: true` frontmatter or specific file) in the `_notes` folder
- Moves image in `assets/img` and convert (with alt support)
- Converts highlight (`==mark==` to `[[mark::highlight]]`)
- Converts "normal" writing to GFM markdown (adding `  \n` each `\n`)
- Supports non existant file (adding a css for that 😉)
- Supports image flags css (Lithou snippet 🙏)
- Support normal and external files

Finally, the plugin will add, commit and push if supported.
For mobile, I work on ios on some shortcuts.

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
