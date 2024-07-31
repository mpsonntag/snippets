import feedparser

feed_url = ""

curr_feed = feedparser.parse(feed_url)

num_episodes = len(curr_feed.entries)
curr_loop = len(curr_feed.entries)
for en in curr_feed.entries:
    print(f"#{curr_loop}/{num_episodes}: {en.title}: {en.link}")
    curr_loop = curr_loop - 1
