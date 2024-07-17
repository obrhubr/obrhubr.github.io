import os
import shutil

import util

# Copy posts and assets to blog
def copy_post_to_blog(post_name, publish_time):
	# Delete the files of the post in the _posts and assets folders
	print("Delete previous files from assets/ and _posts/ folders for the blogpost")

	try:
		os.remove(os.path.join(util.POSTS, publish_time + "-" + post_name + ".md"))
		# Remove directory in assets
		shutil.rmtree(os.path.join(util.ASSETS, post_name))
	except:
		pass

	# Copy markdown and assets to production folders
	print("Copy files to assets/ and _posts/ folders...")

	shutil.copytree(
		os.path.join(util.NOTION_FOLDER, post_name, util.ASSETS),
		os.path.join(util.ASSETS, post_name)
	)
	shutil.copy(
		os.path.join(util.NOTION_FOLDER, post_name, publish_time + "-" + post_name + ".md"),
		os.path.join(util.POSTS)
	)

	return

# Delete all old blog posts and assets that don't exist on notion
def clean_folders(posts):
	print("Deleting blog posts and folders that don't exist on Notion...")

	# Get all post_names for posts on Notion
	posts_names = []
	for (_, p) in posts:
		name = p["properties"]["short-name"]["rich_text"][0]["text"]["content"]
		time = p["properties"]["Date"]["date"]["start"].split("T")[0]
		posts_names += [f"{time}-{name}.md"]

	# Keep track of deleted files
	deleted = []

	# Delete the files
	files = os.walk(os.path.join(util.POSTS))

	for dirpath, dirnames, filenames in files:
		for filename in filenames:
			if not filename in posts_names:
				to_delete = os.path.join(dirpath, filename)
				print(f"Deleted file={to_delete}...")
				os.remove(to_delete)

				# Log deleted name
				deleted += [to_delete]

	# Get folder names to delete
	deleted_names = []
	for d in deleted:
		split_name = d.split("-")
		# Remove date at the beginning
		deleted_names += ["-".join(split_name[3:-1])]

	# Delete all folders in assets/ that match the previously deleted posts in _posts
	files = os.walk(os.path.join(util.ASSETS))

	for dirpath, dirnames, filenames in files:
		for dirname in dirnames:
			if dirname in deleted_names:
				to_delete = os.path.join(dirpath, dirname)
				print(f"Deleted folder={to_delete}...")
				shutil.rmtree(to_delete)

	return deleted

# Setup folder structure necessary for exporting
def setup_folders():
	# Create Notion2md folder
	print("Creating notion2md temporary folder...")
	os.mkdir(os.path.join(util.NOTION_FOLDER))

	return

# Remove the temporary folders
def clean_up():
	# Remove Notion2md folder
	print("Removing the notion2md folder...")
	shutil.rmtree(os.path.join(util.NOTION_FOLDER))

	return

# Get published posts by looping through assets
def get_current_posts():
	pass

# This list also includes styles/ and fonts/ for now
def get_assets_folders():
	posts = []

	# Get all files in assets
	files = os.walk(os.path.join(util.ASSETS))

	for dirpath, dirnames, filenames in files:
		for dirname in dirnames:
			posts += [dirname]

	return posts