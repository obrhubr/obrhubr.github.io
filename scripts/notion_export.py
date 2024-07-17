from dotenv import load_dotenv

import notion_api
import util
import fs
import post

def export_posts():
	try:
		fs.setup_folders()

		posts = notion_api.fetch_all_posts()
		posts = notion_api.filter_posts(posts)

		to_download, updated, new = util.check_posts(posts)

		for (post_id, p) in to_download:
			post.export_page(post_id, p)

		# Delete any posts that have been removed
		deleted = fs.clean_folders(posts)

		# Log updates to logsnag
		util.log_new(new, updated, deleted)
	except Exception as e:
		print(f"Error occured while exporting posts: {e}...")
		raise e
	finally:
		# If an error occurs, clean up the folders
		fs.clean_up()

	return

if __name__ == "__main__":
	load_dotenv()

	export_posts()