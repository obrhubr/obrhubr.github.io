from notion2md.convertor.richtext import richtext_convertor
from notion2md.exporter.block import MarkdownExporter
import zipfile
from datetime import datetime
import shutil
import re
import os
import urllib.request
from urllib.request import urlretrieve

import fs
import util

# Download page as markdown file
def download_markdown(post_id):
	print("Exporting page from Notion...")
	MarkdownExporter(
		block_id=post_id,
		output_path=os.path.join(util.NOTION_FOLDER), 
		download=True
	).export()

	return

# Extract zip file export to short-name folder
def extract_zip(post_id, short_name):
	print("Unzipping file...")
	with zipfile.ZipFile(os.path.join(util.NOTION_FOLDER, post_id + ".zip"), 'r') as zip_ref:
		zip_ref.extractall(os.path.join(util.NOTION_FOLDER, short_name))

	return

# Remove the zip file
def clean_zip(post_id):
	print("Remove zip file...")
	os.remove(os.path.join(util.NOTION_FOLDER, post_id + ".zip"))

	return

def rename_post_folder(post_id, short_name, filename):
	print(f"Rename markdown file and folder to filename={filename}")
	os.rename(
		os.path.join(util.NOTION_FOLDER, short_name, post_id + ".md"),
		os.path.join(util.NOTION_FOLDER, short_name, filename + ".md")
	)

	return

def move_assets(short_name):
	# Create asset directory and move all images there
	print("Create asset directory...")
	os.mkdir(os.path.join(util.NOTION_FOLDER, short_name, util.ASSETS))

	print("Moving assets...")
	files = os.walk(os.path.join(util.NOTION_FOLDER, short_name))
	for dirpath, _, filenames in files:
			for filename in filenames:
				# Only move image assets
				if re.search(r"\.(gif|jpe?g|tiff?|png|webp|bmp)$", filename) != None:
					# Check if in assets
					if dirpath[len(dirpath) - 6:] != "assets":
						src = os.path.join(dirpath, filename)
						dst = os.path.join(util.NOTION_FOLDER, short_name, util.ASSETS)

						print(f"Moved file src={src} to dst={dst}")
						shutil.move(src, dst)

	return

def fetch_previewimage(post, short_name):
	# Add preview image
	preview_images = post["properties"]["preview-image"]["files"]

	# If there is no preview image, return none
	if len(preview_images) == 0:
		return "none"
	
	# add image to meta tags
	image = preview_images[0]
	name = image['name'].split(".")
	previewimage = "preview." + name[-1]

	# download image
	image_url = image['file']['url']
	urllib.request.urlretrieve(
		image_url,
		os.path.join(util.NOTION_FOLDER, short_name, util.ASSETS, previewimage)
	)

	return previewimage

def fetch_favicon(post, short_name):
	# If the post has no emoji icon, return the default
	if post["icon"]["type"] != "emoji":
		return "favicon.png"
	
	# Get emoji name
	emoji = post['icon']["emoji"]
	if len(emoji) > 1:
		emoji = emoji[0]

	# Download emoji as png
	print("Downloading emoji as favicon")
	urlretrieve(
		f"https://emojiapi.dev/api/v1/{hex(ord(emoji))[2:]}/32.png", 
		os.path.join(util.NOTION_FOLDER, short_name, util.ASSETS, "favicon.png")
	)

	return os.path.join(short_name, "favicon.png")

def get_tags(post):
	tags = []
	for tag in post["properties"]["Tags"]["multi_select"]:
		tags += [tag["name"]]

	return tags

def format_tags(post):
	array_to_string = lambda arr: '[{}]'.format(', '.join(f'"{x}"' for x in arr))

	return array_to_string(get_tags(post))

# Check if the post has the tag "Short"
def check_short(post):
	tags = get_tags(post)

	if "Short" in tags:
		return True
	
	return False

# Calculate time to read blog post
def get_words(text):
	minutes = round(len(text.split(" ")) / 200)

	if minutes > 1:
		return f"{minutes} minutes"
	
	return f"{minutes} minute"

def get_sourcecode(post):
	try:
		src = post["properties"]["sourcecode"]["rich_text"][0]["plain_text"]
		return f'"{src}"'
	except KeyError:
		return ""

def add_metadata(markdown_text, metadata):
	print("Inserting jekyll metadata...")

	# Convert metadata dictionary to string
	def metadata_to_string(metadata):
		s = ""
		for key, value in metadata.items():
			s += f"{key}: {value}\n"

		return f"---\nlayout: page\n{s}---\n"

	return f"{metadata_to_string(metadata)}\n{markdown_text}"

def format_page(post, short_name, publish_time, filename):
	# Read file
	markdown_text = ""
	print("Reading .md file and replacing any markdown image tags with the correct filename...")
	with open(os.path.join(util.NOTION_FOLDER, short_name, filename + ".md"), "r") as f:
		markdown_text = f.read()

	# Replace MD image tags with correct filename
	markdown_text = re.sub(
		r"(\!\[.*?\])\((.*)\)",
		r"\1"+ "(/assets/" + short_name + "/" + r"\2" + ")",
		markdown_text
	)

	# Set metadata
	metadata = {
		"title": f'"{post["properties"]["Name"]["title"][0]["text"]["content"]}"',
		"time": get_words(markdown_text),
		"published": publish_time,
		"tags": format_tags(post),
		"permalink": short_name,
		"image": os.path.join(util.ASSETS, short_name, fetch_previewimage(post, short_name)),
		"favicon": fetch_favicon(post, short_name),
		"excerpt": f'"{richtext_convertor(post["properties"]["Summary"]["rich_text"])}"',
		"short": check_short(post),
		"sourcecode": get_sourcecode(post)
	}

	# insert jekyll metadata
	markdown_text = add_metadata(markdown_text, metadata)

	print("Writing file to .md...")
	with open(os.path.join(util.NOTION_FOLDER, short_name, filename + ".md"), "w") as f:
		f.write(markdown_text)
	
	return

def export_page(post_id, post):
	download_markdown(post_id)

	# Get url name of the page
	short_name = post["properties"]["short-name"]["rich_text"][0]["text"]["content"]
	publish_time = post["properties"]["Date"]["date"]["start"].split("T")[0]
	filename = publish_time + "-" + short_name

	extract_zip(post_id, short_name)
	clean_zip(post_id)

	rename_post_folder(post_id, short_name, filename)
	move_assets(short_name)

	format_page(post, short_name, publish_time, filename)

	fs.copy_post_to_blog(short_name, publish_time)

	return