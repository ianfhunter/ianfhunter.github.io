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
