import requests
from datetime import datetime

import fs

NOTION_FOLDER = "notion2md"
ASSETS = "assets"
POSTS = "_posts"

def get_time_since_edit(page):
	# get time when page was last edited
	edited_time = datetime.strptime(page['last_edited_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
	
	time_delta = datetime.now() - edited_time

	return time_delta.total_seconds()

def check_posts(posts):
	to_download = []
	current_posts = fs.get_assets_folders()

	updated = []
	new = []

	for (post_id, p) in posts:
		name = p["properties"]["short-name"]["rich_text"][0]["text"]["content"]

		if not name in current_posts:
			new += [name]
			to_download += [(post_id, p)]
		# if the post has been edited in the last 25 hours, download it
		elif get_time_since_edit(p) < 25 * 60 * 60:
			updated += [name]
			to_download += [(post_id, p)]

	print(f"Downloading the following posts: {new}, {updated}")

	# Deduplicate to_download list
	return to_download, updated, new

# Send logsnag notification if a new post has been added
def log_new(new, updated, deleted):
	def send_notification(event, description, icon):
		# Define the endpoint URL
		url = 'https://api.logsnag.com/v1/log'
		token = 'a4a1235927cef91812a645e040b3ed15'

		data = {
			'project': 'obrhubr',
			'channel': 'blog',
			'event': event,
			'description': description,
			'icon': icon,
			'notify': 'true'
		}

		headers = {
			'Authorization': 'Bearer ' + token,
			'Content-Type': 'application/json'  # Assuming you are sending JSON data
		}
		requests.post(url, json=data, headers=headers)
		print(f"Sent notification to logsnag with data: {event}, {description}, {icon}.")

	for post in new:
		send_notification(
			"publish-post",
			f"A new post has been published: {post}.",
			"📫"
		)

	for post in updated:
		send_notification(
			"update-post",
			f"A post has been updated: {post}.",
			"✅"
		)

	for post in deleted:
		send_notification(
			"delete-post",
			f"A post has been deleted: {post}.",
			"❌"
		)

	return