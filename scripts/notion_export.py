from dotenv import load_dotenv

import notion_api
import util
import fs
import post

def export_posts():
	deleted = fs.clean_folders()
	fs.setup_folders()

	posts = notion_api.fetch_all_posts()
	posts = notion_api.filter_posts(posts)

	for (post_id, p) in posts:
		post.export_page(post_id, p)

	util.log_new(deleted, posts)

	fs.clean_up()

	return

if __name__ == "__main__":
	load_dotenv()

	export_posts()