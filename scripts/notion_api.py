from notion_client import Client
import os

def fetch_all_posts():
	# Connect to notion
	print("Connecting to Notion...")
	notion = Client(auth=os.environ["NOTION_TOKEN"])

	# Fetch blog posts from DB
	print("Fetching blog posts from Notion...")
	posts = notion.databases.query(
		**{
			"database_id": os.environ["DB_ID"]
		}
	)

	return posts

def filter_posts(posts):
	pages = []

	for entry in posts["results"]:
		if entry["properties"]["Blog"]["select"]["name"] == "Publish":
			post_id = entry["id"]
			
			print(f"Found a blog post to publish, id={post_id}...")
			pages += [(post_id, entry)]

	return pages