- [Notenote.link](#notenotelink)
  * [What is this?](#what-is-this-)
  * [What is different?](#what-is-different-)
  * [How do I use this?](#how-do-i-use-this-)
  * [How can I participate?](#how-can-i-participate-)
  * [How do I customize this for my needs?](#how-do-i-customize-this-for-my-needs-)
- [Python script](#python-script)
  * [Requirements](#requirements)
  * [Environment](#environment)
- [Script](#script)
- [Frontmatter and metadata](#frontmatter-and-metadata)
  * [Script](#script-1)
  * [Blog frontmatter options](#blog-frontmatter-options)
- [Custom CSS](#custom-css)
---

# Notenote.link

[![Netlify Status](https://api.netlify.com/api/v1/badges/7b37d412-1240-44dd-8539-a7001465b57a/deploy-status)](https://app.netlify.com/sites/owlly-house/deploys)

## What is this?
A digital garden using a custom version of `simply-jekyll`, optimised for integration with [Obsidian](https://obsidian.md). It is more oriented on note-taking and aims to help you build a nice knowledge base that can scale with time. 

[**DEMO**](https://master--owlly-house.netlify.app/)

If you want to see a more refined example, you can check my notes (in french) at [arboretum.link](https://www.arboretum.link/). Build time is approx. 15 seconds, FYI.

Issues are welcome, including feedback ! Don't hesitate to ask if you can't find a solution. 💫

![screenshot](/assets/img/screenshot.png)

## What is different?

- Markdown is fully-compatible with Obsidian (including Latex delimiters!)
- There are now only notes (no blog posts).
- There are cosmetic changes (ADHD-friendly code highlighting, larger font, larger page)
- Code is now correctly indented
- Wikilinks, but also alt-text wikilinks (with transclusion!) are usable.

## How do I use this?

You can click on this link and let the deploy-to-netlify-for-free-script do the rest !

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/Mara-Li/yet-another-free-publish-alternative)

Follow the [How to setup this site](https://notenote.link/notes/how-to-setup-this-site) guide, written by [raghuveerdotnet](https://github.com/raghuveerdotnet) and then adapted for this fork.

If you want to use it with Github Pages, it is possible, [please read this](https://github.com/Maxence-L/notenote.link/issues/5#issuecomment-762508069).

## How can I participate?

Open an issue to share feedback or propose features. Star the repo if you like it! 🌟

## How do I customize this for my needs?

Things to modify to make it yours:

- The favicon and profile are here: [assets/site/](assets/site)
- The main stuff is in [\_config.yml](_config.yml):
    ```yaml
    title: My obsidian notebook
    name: Obsidian Notebook
    user_description: My linked notebook
    tagline: My linked notebook
    notes_url: "https://yourlink.netlify.app"
    profile_pic: /assets/site/profile.gif
    favicon: /assets/site/favicon.png
    logo: /assets/site/LOGO_SEO.png
    copyright_name: MIT
    baseurl: "/" # the subpath of your site, e.g. /blog
    url: "https://owlly-house.netlify.app/" # the base hostname & protocol for your site, e.g. http://example.com
    encoding: utf-8
    ```
- You may want to change the copyright in [\_includes/footer.html](_includes/footer.html):
   ```html
   <p id="copyright-notice">Licence MIT</p>
   ```
On command-line, you can run `bundle exec jekyll serve` then go to `localhost:4000` to check the result.

# Python script
Having files written in Markdown on Obsidian, I created a python script in order to semi-automatically share selected file, not all file, in my blog. 

## Requirements
- [Python](https://www.python.org/)
- [PyGithub](https://github.com/PyGithub/PyGithub)
- [Python-dotenv](https://github.com/theskumar/python-dotenv)
- [python-frontmatter](https://github.com/eyeseast/python-frontmatter)
- [Pyperclip](https://github.com/asweigart/pyperclip) on Windows/MacOS/Linux | IOS : Pasteboard (Pyto) or clipboard (Pythonista)
You can install all with `pip install -r requirements.txt`

## Environment
You need to create a `.env` in your root folder, with : 
```
vault="G:\path\vault\"
blog="https://your-website.netlify.app/"
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

For more information, see [script Readme](script/README.md)

# Frontmatter and metadata
## Script
The script work with the frontmatter :
- `share: true` : Share the file
- `embed: false` : remove the transluction (convert to normal wikilinks)
- `update: false` : Don't update the file at all. 
- `current: false` : Don't update the date
- `folder` : Use another folder than `_notes`

## Blog frontmatter options
- `flux: false` : remove the file from the feed
- `category` : Add a category for the category page ; `category: false` remove it from this page too.
- `resume` : Add a resume of the file in the feed. 

### Folder options
The metadata key `folder` allow to use another folder than `_note`. There is several steps before you can fully use this options :
1. Create a new folder with the name you want, prefixed with `_` (as `_notes` or `_private`)
2. Add to the `_config.yml` : 
   1. collection : 
```yml
  private:
     output: true
     permalink: /folder_name/:title
   ```
   2. defaults
```yml
   - scope: 
       path: ""
       type: folder_name
    values: 
      layout: post
      content-type: notes
  ```
3. Duplicate the `private.md` and rename it with the folder name you want. 
   1. In this new file, change the line `{%- if page.permalink == "/private/" -%}` for `{%- if page.permalink == "/folder_name/" -%}` 
   2. Change the `permalink` key with `permalink: /folder_name/` 
   3. change `{% assign mydocs = site.folder_name | group_by: 'category' %}`

And there is it !

**Notes about Private folder** : the private folder doesn't have a page, and doesn't appear in the feed or in search. The only way to access it is with the link (adding `/private` at the end) 

# Custom CSS

You can add custom css in [custom css](assets/css/custom.css). It will be read when you use hashtag to stylize your text according to [ContextualTypography](https://github.com/mgmeyers/obsidian-contextual-typography) and/or [CodeMirror Options](https://github.com/nothingislost/obsidian-codemirror-options).

To add custom tag to customize your text, you need to edit the `custom.css` file with :
```css
#tag_name {
    css_value : css;
    . . . 
}
```
The script will read the file and change `#tag_name` to `{: .tag_name}`. 