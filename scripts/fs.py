import os
import shutil

import util

# Copy posts and assets to blog
def copy_post_to_blog(post_name, publish_time):
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

# Delete all old blog posts and assets
def clean_folders():
	print("Deleting old blog posts and folders...")

	# Keep track of deleted posts
	deleted = []

	print("Delete files in _posts folder...")
	files = os.walk(os.path.join(util.POSTS))

	for dirpath, dirnames, filenames in files:
		for filename in filenames:
			to_delete = os.path.join(dirpath, filename)
			print(f"Deleted file={to_delete}...")

			os.remove(to_delete)
			deleted += [to_delete]

	print("Delete folders in assets folder...")
	files = os.walk(os.path.join(util.ASSETS))

	for dirpath, dirnames, filenames in files:
		for dirname in dirnames:
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