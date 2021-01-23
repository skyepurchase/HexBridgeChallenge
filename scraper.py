import enum
import praw
import tweepy
import configparser


CONFIG_FILE = "config.ini"


class Social(enum.Enum):
    REDDIT = 1
    TWITTER = 2


class Scraper:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        dt = config['DEFAULT']
        self.reddit = praw.Reddit(client_id=dt.get('REDDIT_CLIENT'),
                                  client_secret=dt.get('REDDIT_CLIENT_SECRET'),
                                  user_agent=dt.get('REDDIT_USER_AGENT'))
        tweepy_auth = tweepy.AppAuthHandler(
            dt.get('TWITTER_CLIENT'), dt.get('TWITTER_CLIENT_SECRET'))
        self.twitter = tweepy.API(tweepy_auth)

    def get_user_text(self, social_source: Social, name: str, item_count=10):
        if(social_source == Social.TWITTER):
            friends = self.get_twitter_friends(name)
            texts = [self.get_user_comments(
                social_source, f, item_count=3) for f in friends]
            comm = self.get_user_comments(
                social_source, name)
            return (comm, " ".join(texts))
        elif(social_source == Social.REDDIT):
            return (self.get_user_comments(social_source, name, item_count), " ")

    def get_user_comments(self, social_source: Social, name: str, item_count=10):
        if(social_source == Social.TWITTER):
            timeline = self.twitter.user_timeline
            comments = [t.text for t in tweepy.Cursor(timeline,
                                                      screen_name=name, count=item_count).items(item_count)]
        elif(social_source == Social.REDDIT):
            redditor = self.reddit.redditor(name=name)
            comments = [t.body for t in redditor.comments.top(
                "all", limit=item_count)]
        return " ".join(comments)

    def get_twitter_friends(self, name: str, limit=10):
        friends = self.twitter.friends_ids(screen_name=name)[:limit]
        friend_names = [self.twitter.get_user(
            id).screen_name for id in friends]
        return friend_names

    def get_redditors(self, limit=10):
        names = [post.author.name for post in self.reddit.subreddit(
            "news").comments(limit=limit)]
        return names
