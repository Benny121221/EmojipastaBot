## Description
This Python bot turns the parent of your comment into emojipasta. It can be
summoned by a username tag, 'u/AnEmojipastaBot'.

Example:

```
redditor 1: hello world
redditor 2: u/AnEmojipastaBot
AnEmojipastaBot: hello world 🌍
```

It was built by scraping thousands of comments from r/emojipasta
and using them to form mappings from word->emoji. The bot itself,
and the scraping tool, are based on the PRAW framework, and the
'emoji' Python package was used identify emojis in the r/emojipasta
comments.

There are no hard-coded credentials or user details in the code, so
everyone is free to run their own version of the bot.

## How to use
#### The bot

```
python ./src/bot/emojipastabot.py <client_id> <client_secret> <user_agent> <username> <password>
```

If you don't have credentials or a reddit user, then follow the setup
instructions in the [PRAW docs](http://praw.readthedocs.io/en/latest/getting_started/quick_start.html).

#### The scraper
The scraper saves comments to a hard-coded location, you may want
to modify it.
```
python ./src/scraping/reddit_scraping.py <client_id> <client_secret> <user_agent> <username> <password>
```

#### The emojipasta generator
```python
from emojipasta.emojipastagenerator import EmojipastaGenerator
generator = EmojipastaGenerator.of_default_mappings()
generator.generate_emojipasta("it's getting hot in here")
```
Output:
```
it's getting hot 🔥😍 in 🔽👏 here 💪👏
```

If you want to create an EmojipastaGenerator with custom emoji
mappings (a dict that maps from a lowercase word to a list
of emojis):
```python
from emojipasta.emojipastagenerator import EmojipastaGenerator
EmojipastaGenerator.of_custom_mappings({"hello": ["👋", "👈"]})
``` 