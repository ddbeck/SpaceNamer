import tweepy


def followers(twitter):
    """Get the set of current followers."""
    users = tweepy.Cursor(twitter.followers).items()
    return set(u.screen_name for u in users)

