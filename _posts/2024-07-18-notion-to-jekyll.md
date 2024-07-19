---
layout: page
title: "Writing Notion to Jekyll, a Tool for my Blog"
time: 2 minutes
published: 2024-07-18
colortags: [{'id': '2ed41265-7c0a-4aa6-9c43-6ca82f1a0459', 'name': 'Short', 'color': 'default'}, {'id': 'd4527084-e89a-472f-a8aa-454b5d0a3eeb', 'name': 'Blogging', 'color': 'gray'}, {'id': '26e3acab-0124-4773-a185-49dd8760c91c', 'name': 'API', 'color': 'orange'}]
tags: ['Short', 'Blogging', 'API']
permalink: notion-to-jekyll
image: assets/notion-to-jekyll/none
favicon: notion-to-jekyll/favicon.png
excerpt: ""
short: True
sourcecode: "https://github.com/obrhubr/notion-to-jekyll"
math: False
---

I previously wrote about my process to publish posts to my blog. In the meantime I have been quite busy and the way it works has now changed quite a bit.

Previously, I had a [single script](https://github.com/obrhubr/obrhubr.github.io/blob/5521915354da232c5bc40c8d8a035f6c7d2fd953/notion_export.py) called `notion_export.py` living in my [blog’s repository](https://github.com/obrhubr/obrhubr.github.io) that downloaded all posts and their assets and simply copied them into my `_posts` directory. I ran this script daily using GitHub Actions, that was it.

But as I added more features the script grew in size drastically. This is why I refactored it into a standalone tool: `notion-to-jekyll`.

It still fundamentally works the same, but it’s a ✨python package✨ now. However, there have been a few upgrades.

- Instead of downloading all posts, it only exports those that have changed in the last 24 hours (which makes it a lot faster).

- It logs any changes to [Logsnag](https://logsnag.com/) and notifies me.

- It supports inline equations that work with [Katex](https://katex.org/), which means I don’t need JavaScript to render them with [MathJax](https://www.mathjax.org/) on the frontend.

- It converts all images to `.jpg` and renames them to an MD5 hash of their content, which fixes the ugly filenames on my blog.

- Use the captions on Notion to add correct alt-text to the images.

- and a lot more small details…

<br/>

Here is what that looks like on the terminal (I’m quite proud of my progress bars):


```bash
Starting Notion to Jekyll Exporter...
Loading secrets from the environment variables.
Found 5 blog posts to publish.
Downloading all posts.

1/5 - Exporting created-blog to Jekyll.
Downloading markdown from Notion.
Unzipping file...
Replacing image tags in markdown with correct paths.
Encode images to jpg.
Rename image to it's hash.
Downloading emoji as favicon: 📟
Inserting jekyll metadata.
Output formatted markdown file.

Exporting post created-blog: 100%|███████████████████████| 8/8 [00:06<00:00, 1.45 steps/s]

[...]

5/5 - Exporting chess-engine to Jekyll.
Downloading markdown from Notion.
Unzipping file...
Replacing image tags in markdown with correct paths.
Encode images to jpg.
Rename image to it's hash.
Downloading preview image from Notion.
Downloading emoji as favicon: ♟
Inserting jekyll metadata.
Output formatted markdown file.

Exporting post chess-engine: 100%|███████████████████████| 8/8 [00:06<00:00, 1.45 steps/s]

Finished exporting posts from Notion to Jekyll.
```

If you want to use this tool too, you can! Head to the repository at [obrhubr/notion-to-jekyll](https://github.com/obrhubr/notion-to-jekyll) and follow the instructions. You can customise it to fit your use case with the command line options.

