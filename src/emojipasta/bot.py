import time
import json
import os

cfg_filename = "config.json"

import praw
from generator import EmojipastaGenerator

def main():
	cwd = os.getcwd()
	cfg_file = open(cwd + "/" + cfg_filename)
	cfg_settings = json.loads(cfg_file.read())
	cfg_file.close()
	
	reddit = praw.Reddit(user_agent=cfg_settings["user_agent"],
	client_id=cfg_settings["client_id"],
	client_secret=cfg_settings["client_secret"],
	username=cfg_settings["username"],
	password=cfg_settings["password"])
	
	gen = EmojipastaGenerator.of_default_mappings()

	user = reddit.redditor("EmojifierBot")
	for comment in user.comments.hot(limit = None):
		skip = False 
		comment.refresh()
		if comment.parent().author == reddit.config.username:
			continue

		for reply in comment.replies:
			skip = True
			break
		
		if not skip:
			reply_body = gen.generate_emojipasta(comment.body)
			comment.reply(reply_body)
			
			print('-' * 80)
			print(time.strftime("%Y-%m-%d %H:%M:%S GMT", time.gmtime()))
			print("Reply Body:")
			print(reply_body)
			print('-' * 80)
			time.sleep(900) # 15 minutes

main()
