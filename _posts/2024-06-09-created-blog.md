---
layout: page
title: "How I created my Blog - Notion to GitHub Pages"
time: 2 minutes
published: 2024-06-09
tags: ["Short", "Blogging", "API"]
permalink: created-blog
image: assets/created-blog/none
favicon: created-blog/favicon.png
excerpt: ""
short: True
sourcecode: "https://github.com/obrhubr/obrhubr.github.io"
---

The biggest hurdle to creating content for a blog is writing the entries themselves. Hosting a blog on GitHub Pages means that you have to submit your entries in markdown (or html) format. But while Markdown is great for writing documents, adding tables and images is not as ergonomic as I would like.

This is why I use Notion to edit my blog posts. I get a great interface for free - which allows me to edit from anywhere and any device - and I can easily upload images and create tables with a GUI. Then, once finished, I download (automatically of course, I’m a developer after all) raw Markdown and publish to GitHub.

## But…

The battle-hardened Linux user will take offense at two things here:

- I don’t own my data. Notion stores it in the cloud and can do anything and everything they want with it.

- Editing locally allows me to customise everything about the interface.

The first point doesn’t concern me as anything I write will be freely available online anyways, no secrets here… As for the second point, of course editing locally might allow me to change specific things, and I sometimes miss this (especially for code blocks). But the fact that I can edit from anywhere makes the trade-off worth it.

## How does my Writing get from Notion to [obrhubr.org](http://obrhubr.org/)?

I set up an action in the repository which stores the source code for the blog. It runs once a week and - thanks to [notion2md](https://github.com/echo724/notion2md) - fetches all posts tagged with `publish` from Notion. The assets are then automatically moved to the right directory in the Jekyll blog and the Markdown file is tagged with the information needed to publish it (date, excerpt, reading time, tags).

I don’t have to worry about anything, except changing the tag from `preview` to `publish` in my Notion Database containing all the posts. This also means I can edit the posts anytime from Notion and the changes will be reflected at most 7 days later. 

I don’t have to waste time worrying if I have actually pushed changes to GitHub, especially if I’m not on my PC or a platform that allows me to interface with git.

