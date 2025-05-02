# obrhubr.github.com

I wanted to have an easy solution to publish my notes and writing from notion to my github pages, so I wrote a little python script.

It fetches all notion pages in a database and determines which are ready to publish by checking for the `Publish` tag.

It then adds the necessary jekyll metadata and writes the markdown file and assets to the corresponding jekyll folders.

# Thanks

I could not have done this without the great [notion2md](https://github.com/echo724/notion2md) project.