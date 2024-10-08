---
layout: page
title: "How I publish from Notion to GitHub Pages"
time: 2 minutes
published: 2024-06-09
colortags: [{'id': '2ed41265-7c0a-4aa6-9c43-6ca82f1a0459', 'name': 'Short', 'color': 'default'}, {'id': 'd4527084-e89a-472f-a8aa-454b5d0a3eeb', 'name': 'Blogging', 'color': 'gray'}, {'id': '26e3acab-0124-4773-a185-49dd8760c91c', 'name': 'API', 'color': 'orange'}]
tags: ['Short', 'Blogging', 'API']
permalink: created-blog
favicon: created-blog/favicon.png
excerpt: ""
short: True
sourcecode: "https://github.com/obrhubr/obrhubr.github.io"
math: False
---

The biggest hurdle to creating content for a blog is writing the posts themselves. Hosting a blog on GitHub Pages means that you have to push your posts in markdown (or html) format. But while Markdown is great for writing documents, adding tables and images is not as easy as I would like.

This is why I use Notion to edit my blog posts. I get a great interface for free - which allows me to edit from anywhere and any device - and I can easily upload images and create tables with a GUI. Then, once finished, I download (automatically of course, I’m a developer after all) raw Markdown and publish to GitHub.

## But…

The big-corp wary user will point out two things here:

- I don’t own my data. Notion stores it in the cloud and can do anything and everything they want with it.

- Editing locally would allow me to customise everything about the interface.

However the ease of use and that I can edit from anywhere in the world on any device makes these trade-offs worth it for me.

## How does my Writing get from Notion to [obrhubr.org](http://obrhubr.org/)?

I set up an action in the repository which stores the source code for the blog. It runs once a day and - thanks to [notion2md](https://github.com/echo724/notion2md) - fetches all posts tagged with `publish` from Notion. The assets are then automatically moved to the right directory in the Jekyll blog and the Markdown file is tagged with the information needed to publish it (date, excerpt, reading time, tags).

I don’t have to worry about anything, except changing the tag from `preview` to `publish` in my Notion Database containing all the posts. This also means I can edit the posts anytime from Notion and the changes will be reflected at most 7 days later. 

I don’t have to waste time worrying if I have actually pushed changes to GitHub, especially if I’m not on my PC or a platform that allows me to interface with git.

