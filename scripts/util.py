import requests

NOTION_FOLDER = "notion2md"
ASSETS = "assets"
POSTS = "_posts"

# Send logsnag notification if a new post has been added
def log_new(deleted, exported):
	if len(deleted) == len(exported):
		return
	
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
	requests.post(url, json=data, headers=headers)

	return