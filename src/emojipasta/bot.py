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
	
	while True:
		try:
			for comment in user.comments.hot(limit = None):
				try:
					skip = False
					
					if comment.submission.locked:
						skip = True
					
					if not skip:
						comment.refresh()
						if comment.parent().author == reddit.config.username:
							skip = True
					
					if not skip:
						for reply in comment.replies:
							if reply.author == reddit.config.username:
								skip = True
								break
					
					if not skip:
						reply_body = gen.generate_emojipasta(comment.body)
						
						if len(reply_body) > 10000:
							continue
						
						comment.reply(reply_body)
						
						print_header('-', time.strftime("%Y-%m-%d %H:%M:%S GMT", time.gmtime()) + '\nReply Body:\n' + reply_body)
						#time.sleep(1)
				except BaseException as e:
					handle_error(e)
			
			print_header('*', "Reached end of iterable, retrying shortly.")
		
		except BaseException as e:
			handle_error(e)

		
		#time.sleep(3)

def handle_error(e):
	print_error(e)
	if type(e) == praw.exceptions.RedditAPIException:
		for subexception in e.items:
			if "RATELIMIT" in subexception.error_message:
				print_header('*', "Sleeping for 15 minutes to comply with rate limit")
				time.sleep(900)
				break

def print_error(error):
	print('#' * 80)
	print('#' * 80)
	print(f"An error of type {type(error)} was raised:")
	print(vars(error))
	print('-' * 80)

def print_header(char, text):
	print(char * 80)
	print(text)
	print(char * 80)

main()
