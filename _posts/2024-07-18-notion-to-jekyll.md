---
layout: page
title: "Writing the Tool notion-to-jekyll for my Blog"
time: 1 minute
published: 2024-07-18
colortags: [{'id': '2ed41265-7c0a-4aa6-9c43-6ca82f1a0459', 'name': 'Short', 'color': 'default'}, {'id': 'd4527084-e89a-472f-a8aa-454b5d0a3eeb', 'name': 'Blogging', 'color': 'gray'}, {'id': '26e3acab-0124-4773-a185-49dd8760c91c', 'name': 'API', 'color': 'orange'}]
tags: ['Short', 'Blogging', 'API']
permalink: notion-to-jekyll
image: none
favicon: notion-to-jekyll/favicon.png
excerpt: ""
short: True
sourcecode: "https://github.com/obrhubr/notion-to-jekyll"
math: False
---

I [previously](https://obrhubr.org/created-blog) wrote about my process to publish posts on my blog but in the meantime I have been quite busy. My workflow has now changed quite a bit.

I had a [single script](https://github.com/obrhubr/obrhubr.github.io/blob/5521915354da232c5bc40c8d8a035f6c7d2fd953/notion_export.py) called `notion_export.py` living in my [blog’s repository](https://github.com/obrhubr/obrhubr.github.io) that downloaded all posts and their assets and copied them into my `_posts` directory. This script ran daily on GitHub Actions and mirrored my entire writings from Notion to my blog.

As I added more features, the script grew in size drastically, which is why I refactored it into a [standalone tool](https://github.com/obrhubr/notion-to-jekyll): `notion-to-jekyll`. The basic structure remained identical, but it’s a ✨python package✨ now. However, there have been a few upgrades.

- Instead of downloading all posts, it only exports those that have changed since it last downloaded them.

- It logs any changes to [Logsnag](https://logsnag.com/) and notifies me.

- It supports inline equations that work with [Katex](https://katex.org/), which means I don’t need JavaScript to render them with [MathJax](https://www.mathjax.org/) on the frontend.

- It converts all images to `.jpg` and renames them to an MD5 hash of their content, which fixes the ugly filenames on my blog.

- Use the captions on Notion to add correct alt-text to the images.

- Automatically generate smaller versions of images in order to optimise load times.

- and a lot more small details…

If you want to use this tool too, you can! Head to the repository at [obrhubr/notion-to-jekyll](https://github.com/obrhubr/notion-to-jekyll) and follow the instructions. You can customise it to fit your use case with the command line options.

