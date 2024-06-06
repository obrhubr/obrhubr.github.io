from notion_client import Client
import os
from notion2md.exporter.block import MarkdownExporter
from notion2md.convertor.richtext import *
import zipfile
from datetime import datetime
import shutil
import re
from dotenv import load_dotenv
import urllib.request

load_dotenv()

# Connect to notion
print("Connecting to Notion...")
notion = Client(auth=os.environ["NOTION_TOKEN"])

# Fetch blog posts from DB
print("Fetching blog posts from Notion...")
blog_posts = notion.databases.query(
	**{
		"database_id": os.environ["DB_ID"]
	}
)

# Get all blog posts marked ready for publishing
old_pages = []
pages = []

for entry in blog_posts["results"]:
	if entry["properties"]["Blog"]["select"]["name"] == "Publish":
		print("Found a blog post to publish, id={id}...".format(id=entry["id"]))
		pages += [(entry["id"], entry)]

# Delete all old blog posts and assets
print("Deleting old blog posts and folders...")

print("Delete files in _posts folder...")
files = os.walk("./_posts/")

for dirpath, dirnames, filenames in files:
	for filename in filenames:
		if filename != "0000-01-01-default.md":
			print("Deleted file={file}...".format(file=dirpath + "/" + filename))
			os.remove(dirpath + "/" + filename)

print("Delete folders in assets folder...")
files = os.walk("./assets/")

for dirpath, dirnames, filenames in files:
	for dirname in dirnames:
		# Only delete folders from blog posts not notes
		if dirname[0:2] != "20":
			old_pages += [dirname]
			print("Deleted folder={folder}...".format(folder=dirpath + "/" + dirname))
			shutil.rmtree(dirpath + "/" + dirname)

# Create Notion2md folder
print("Creating notion2md temporary folder...")
os.mkdir("./notion2md/")

# Loop through blog posts to export them
for page in pages:
	# Download page as markdown file
	print("Exporting page from Notion...")
	MarkdownExporter(block_id=page[0], output_path='./notion2md/', download=True).export()

	# Get url name of the page
	short_name = page[1]["properties"]["short-name"]["rich_text"][0]["text"]["content"]

	# Extract zip file export to short-name folder
	with zipfile.ZipFile("./notion2md/" + page[0] + ".zip", 'r') as zip_ref:
		print("Unzipping file...")
		zip_ref.extractall("./notion2md/" + short_name)
		
	# Remove the original directory and create new ones
	print("Remove zip file...")
	os.remove("./notion2md/" + page[0] + ".zip")
	
	print("Rename markdown file and folder to short_name={short_name} and date={date}...".format(short_name=short_name, date=datetime.today().strftime('%Y-%m-%d')))
	os.rename(
		"./notion2md/" + short_name + "/" + page[0] + ".md", 
		"./notion2md/" + short_name + "/" + page[1]["created_time"].split("T")[0] + "-" + short_name + ".md"	
	)

	# Create asset directory and move all images there
	print("Create asset directory...")
	os.mkdir("./notion2md/" + short_name + "/assets")
	files = os.walk("./notion2md/" + short_name)

	print("Moving assets...")
	for dirpath, dirnames, filenames in files:
			for filename in filenames:
				if re.search(r"\.(gif|jpe?g|tiff?|png|webp|bmp)$", filename) != None:
					if dirpath[len(dirpath) - 6:] != "assets":			
						print("Moved file src={src} to dst={dst}...".format(src=dirpath + "/" + filename, dst="./notion2md/" + short_name + "/assets/"))
						shutil.move(dirpath + "/" + filename, "./notion2md/" + short_name + "/assets/")

	# Read file and replace all markdown image tags with new filenames
	new_file = ""

	print("Reading .md file and replacing any markdown image tags with the correct filename...")
	with open("./notion2md/" + short_name + "/" + page[1]["created_time"].split("T")[0] + "-" + short_name + ".md", "r") as f:
		new_file = re.sub(
			r"(\!\[.*?\])\((.*)\)",
			r"\1"+ "(/assets/" + short_name + "/" + r"\2" + ")",
			f.read()
		)

	print("Writing original file to .md...")
	with open("./notion2md/" + short_name + "/" + page[1]["created_time"].split("T")[0] + "-" + short_name + ".md", "w") as f:
		f.write(new_file)

	# Add preview image
	previewimage = "none"
	preview_images = page[1]["properties"]["preview-image"]["files"]
	if len(preview_images) != 0:
		# add image to meta tags
		name = preview_images[0]['name'].split(".")
		previewimage = "preview." + name[-1]

		# download image
		image_url = preview_images[0]['file']['url']

		urllib.request.urlretrieve(image_url, "./notion2md/" + short_name + "/assets/" + previewimage)

	# Add favicon
	favicon = "favicon.png"
	if page[1]["icon"]["type"] == "emoji":
		favicon = short_name + "/favicon.png"

		# Fetch icon as png from the web
		from urllib.request import urlretrieve
		emoji = page[1]['icon']["emoji"]
		if len(emoji) > 1:
			emoji = emoji[0]
		print("Downloading emoji as favicon")
		urlretrieve('https://emojiapi.dev/api/v1/{:X}'.format(ord(emoji)) + "/32.png", "./notion2md/" + short_name + "/assets" + "/favicon.png")

	# insert jekyll metadata
	print("Inserting jekyll metadata...")
	tags = []
	for tag in page[1]["properties"]["Tags"]["multi_select"]:
		tags += [tag["name"]]

	new_file = ""
	metadata = ""

	with open("./notion2md/" + short_name + "/" + page[1]["created_time"].split("T")[0] + "-" + short_name + ".md", "r") as f:
		new_file = f.read()
		metadata = """---
layout: page
title: {title}

time: {time}
published: {date}

tags: {tags}
permalink: {permalink}
image: {previewimage}
favicon: {favicon}
excerpt: {excerpt}
---

""".format(
		title=page[1]["properties"]["Name"]["title"][0]["text"]["content"],
		time=str(round(len(new_file.split(" ")) / 200)) + " minute", 
		date=page[1]["created_time"].split("T")[0], 
		tags=" ".join(tags),
		permalink=short_name,
		previewimage="assets/" + short_name + "/" + previewimage,
		favicon=favicon,
		excerpt=richtext_convertor(page[1]["properties"]["Summary"]["rich_text"])
	)

	print("Writing new file with metadata to .md...")
	with open("./notion2md/" + short_name + "/" + page[1]["created_time"].split("T")[0] + "-" + short_name + ".md", "w") as f:
		f.write(metadata + new_file)

	# Copy markdown and assets to production folders
	print("Copy files to assets/ and _posts/ folders...")
	shutil.copytree("./notion2md/" + short_name + "/assets", "./assets/" + short_name)
	shutil.copy("./notion2md/" + short_name + "/" + page[1]["created_time"].split("T")[0] + "-" + short_name + ".md", "_posts")

# Remove Notion2md folder
print("Removing the notion2md folder...")
shutil.rmtree("./notion2md")

# Send logsnag notification
if len(old_pages) != len(pages):
	import requests
	# Define the endpoint URL
	url = 'https://api.logsnag.com/v1/log'
	token = 'a4a1235927cef91812a645e040b3ed15'

	data = {
		'project': 'obrhubr',
		'channel': 'blog',
		'event': 'publish-post',
		'description': 'A new blogpost was just published.',
		'icon': '📫',
		'notify': 'true'
	}

	headers = {
		'Authorization': 'Bearer ' + token,
		'Content-Type': 'application/json'  # Assuming you are sending JSON data
	}
	response = requests.post(url, json=data, headers=headers)

print("Done.")