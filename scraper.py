import enum
import praw
import prawcore
from prawcore.exceptions import PrawcoreException
import tweepy
import configparser

from tweepy.error import TweepError


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
            comm = self.get_user_comment_texts(
                social_source, name)
            friends = self.get_twitter_friends(name)
            texts = []
            for f in friends:
                try:
                    texts.append(self.get_user_comment_texts(
                        social_source, f, item_count=3))
                except Exception:
                    continue
            return [(5, comm), (1, " ".join(texts))]
        elif(social_source == Social.REDDIT):
            return [(1, self.get_user_comment_texts(social_source, name, item_count))]
        else:
            raise Exception(
                f"Incorrect social_source. It needs to be one of Social.{', Social.'.join(Social._member_names_)}.")

    def get_user_comment_texts(self, social_source: Social, name: str, item_count=10):
        return " ".join([t[0] for t in self.get_user_comments(social_source, name, item_count)])

    def get_user_comment_urls(self, social_source: Social, name: str, item_count=10):
        return [t[1] for t in self.get_user_comments(social_source, name, item_count)]

    def get_user_comments(self, social_source: Social, name: str, item_count=10):
        if(social_source == Social.TWITTER):
            try:
                timeline = self.twitter.user_timeline
                comments = [(t.text, f"https://twitter.com/twitter/statuses/{str(t.id)}") for t in tweepy.Cursor(timeline,
                                                                                                                 screen_name=name, count=item_count).items(item_count)]
                return comments
            except TweepError as e:
                code = e.response.status_code
                if(code == 404):
                    raise Exception("User not found.")
                elif(code == 401):
                    raise Exception(
                        "Your account might be private. We are not authorized to access your timeline/friends.")
                elif(code == 429):
                    raise Exception(
                        "Too many users! Wait 15 minutes before retrying as Twitter needs to reset our quota.")
                else:
                    raise e
        elif(social_source == Social.REDDIT):
            try:
                redditor = self.reddit.redditor(name=name)
                comments = [(t.body, f"https://www.reddit.com{t.permalink}") for t in redditor.comments.top(
                    "all", limit=item_count)]
                return comments
            except PrawcoreException as e:
                code = e.response.status_code
                if(code == 404):
                    raise Exception("User not found.")
                elif(code == 401):
                    raise Exception(
                        "Your account might be private. We cannot access your Reddit history.")
                elif(code == 429):
                    raise Exception(
                        "Too many requests! Wait 5 minutes before retrying as Reddit needs to reset our quota.")
                else:
                    raise e
        else:
            raise Exception(
                f"Incorrect social_source. It needs to be one of Social.{', Social.'.join(Social._member_names_)}.")

    def get_twitter_friends(self, name: str, limit=5):
        friends = self.twitter.friends_ids(screen_name=name)[:limit]
        friend_names = [self.twitter.get_user(
            id).screen_name for id in friends]
        return friend_names

    def get_twitter_followers(self, name: str, limit=10):
        followers = self.twitter.followers_ids(screen_name=name)[:limit]
        followers_names = [self.twitter.get_user(
            id).screen_name for id in followers]
        return followers_names

    def sample_names(self, social_source: Social, limit=10, topic="news"):
        if(social_source == Social.TWITTER):
            search = self.twitter.search
            comments = [t.author.screen_name for t in tweepy.Cursor(search,
                                                                    q=topic, lang="en", tweet_mode="extended", count=limit).items(limit)]
            return comments
        elif(social_source == Social.REDDIT):
            names = [post.author.name for post in self.reddit.subreddit(
                topic).comments(limit=limit)]
        return names