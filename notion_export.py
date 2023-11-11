from notion_client import Client
import os
from notion2md.exporter.block import MarkdownExporter
import zipfile
from datetime import datetime
import shutil
import re
from dotenv import load_dotenv

load_dotenv()

# Connect to notion
notion = Client(auth=os.environ["NOTION_TOKEN"])

# Fetch blog posts from DB
blog_posts = notion.databases.query(
	**{
		"database_id": os.environ["DB_ID"]
	}
)

# Get all blog posts marked ready for publishing
pages = []

for entry in blog_posts["results"]:
	if entry["properties"]["Blog"]["select"]["name"] == "Publish":
		pages += [(entry["id"], entry)]

# Create Notion2md folder
os.mkdir("./notion2md/")

# Loop through blog posts to export them
for page in pages:
	# Download page as markdown file
	MarkdownExporter(block_id=page[0], output_path='./notion2md/', download=True).export()

	# Get url name of the page
	short_name = page[1]["properties"]["short-name"]["rich_text"][0]["text"]["content"]

	# Extract zip file export to short-name folder
	with zipfile.ZipFile("./notion2md/" + page[0] + ".zip", 'r') as zip_ref:
		zip_ref.extractall("./notion2md/" + short_name)
		
	# Remove the original directory and create new ones
	os.remove("./notion2md/" + page[0] + ".zip")
	os.rename(
		"./notion2md/" + short_name + "/" + page[0] + ".md", 
		"./notion2md/" + short_name + "/" + datetime.today().strftime('%Y-%m-%d') + "-" + short_name + ".md"	
	)

	# Create asset directory and move all images there
	os.mkdir("./notion2md/" + short_name + "/assets")
	files = os.walk("./notion2md/" + short_name)

	for dirpath, dirnames, filenames in files:
			for filename in filenames:
				if re.search(r"\.(gif|jpe?g|tiff?|png|webp|bmp)$", filename) != None:
					if dirpath[len(dirpath) - 6:] != "assets":
						shutil.move(dirpath + "/" + filename, "./notion2md/" + short_name + "/assets/")

	# Read file and replace all markdown image tags with new filenames
	new_file = ""

	with open("./notion2md/" + short_name + "/" + datetime.today().strftime('%Y-%m-%d') + "-" + short_name + ".md", "r") as f:
		new_file = re.sub(
			r"(\!\[.*?\])\((.*)\)",
			r"\1"+ "(/assets/" + short_name + "/" + r"\2" + ")",
			f.read()
		)

	with open("./notion2md/" + short_name + "/" + datetime.today().strftime('%Y-%m-%d') + "-" + short_name + ".md", "w") as f:
		f.write(new_file)

	# insert jekyll metadata
	tags = []
	for tag in pages[0][1]["properties"]["Tags"]["multi_select"]:
		tags += [tag["name"]]

	new_file = ""
	metadata = ""

	with open("./notion2md/" + short_name + "/" + datetime.today().strftime('%Y-%m-%d') + "-" + short_name + ".md", "r") as f:
		new_file = f.read()
		metadata = """---
layout: page
title: {title}

time: {time}
published: {date}

tags: {tags}
excerpt: {excerpt}
---

""".format(
		title=pages[0][1]["properties"]["Name"]["title"][0]["text"]["content"],
		time=str(round(len(new_file.split(" ")) / 200)) + " minute", 
		date=pages[0][1]["last_edited_time"].split("T")[0], 
		tags=" ".join(tags),
		excerpt=pages[0][1]["properties"]["Summary"]["rich_text"][0]["text"]["content"]
	)

	with open("./notion2md/" + short_name + "/" + datetime.today().strftime('%Y-%m-%d') + "-" + short_name + ".md", "w") as f:
		f.write(metadata + new_file)

	# Copy markdown and assets to production folders
	shutil.copytree("./notion2md/" + short_name + "/assets", "./assets/" + short_name)
	shutil.copy("./notion2md/" + short_name + "/" + datetime.today().strftime('%Y-%m-%d') + "-" + short_name + ".md", "_posts")

# Remove Notion2md folder
shutil.rmtree("./notion2md")