---
title: Obsidian integration
tags: CMS
category: Obsidian
resume: Obsidian Integration
---

The main purpose of this fork, other than cosmetic changes, is to create a web representation of an [[Obsidian::https://obsidian.md]] vault, using the [[Simply-Jekyll::https://github.com/raghuveerdotnet/simply-jekyll]] template.

## Usage

Things to know :

- Markdown is fully-compatible (including Latex delimiters !)

- There are now only notes (no blog posts). If you really want blog posts along notes, a hack is to set the YAML season of blog posts to `summer` and notes to `automn` - they won't appear in feed but will be searchable and appear in tags page.

- Code is now correctly indented

- You can change the code template by replacing the css in `/assets/css/highlight.css` by any template from [[pygment.css::https://github.com/richleland/pygments-css]]

- Wikilinks are usable : **[​[**​...**]]**,

- Also alt-text wikilinks (with transclusion !) : **[​[**​original link\\|alternative text**]]**

Please note : You need to escape the pipe character in Obsidian (\\| instead of \|). This won't break Obsidian's functionality.

- **Fresh new feature** : you can also link headers ! Use # when typing the wikilink : **[​[**Obsidian integration#Obsidian setup\|Alt-text**]]** will create the following link : [[Obsidian integration#Obsidian setup\|Alt-text]] (click on it to see the effect)

Please note : This feature will work only if you write alternative text in the link : [[Obsidian integration#Obsidian setup]] won't work[^1]. 

[^1]: I don't use it, so I didn't change it but if it's important for you open an issue and I may fix it.

- You can use [[Simply-Jekyll custom features::https://simply-jekyll.netlify.app/posts/exploring-the-features-of-simply-jekyll]], such as flashcards : [[flashcards !::srs]] - but don't click on it in Obsidian, else it will create a new page.

### Frontmatter

Front matter is needed at the beginning of your note. Here is the template :

```yaml
---
category: 
share: 
title: 
date: 
flux:
resume:
embed:
---
```

- `share: true` : Share the file
- `embed: false` : remove the transluction (convert to normal wikilinks)
- `update: false` : Don't update the file at all. 
- `current: false` : Don't update the date
- `flux: false` : remove the file from the feed
- `category` : Add a category for the category page ; `category: false` remove it from this page too.
- `resume` : Add a resume of the file in the feed. 

### Images

Images are the tricky part : 

- You can use vanilla markdown links: `![](/asset/img/img.png)`
- You can drag/drop/paste images in Obsidian, which will create a link such as : `[​[​../assets/img/Pasted image.png]]`

A quick hack in the last case is just to change the brackets : `![](../assets/img/Pasted image.png)`


