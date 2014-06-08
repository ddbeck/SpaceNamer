
import contextlib
import random

import tweepy


class Followers(object):
    """Follower management."""
    def __init__(self, twitter, file_path):
        self.twitter = twitter
        self.file_path = file_path
        self._data = None

    def __str__(self):
        return '{}'.format(self.all())

    def refresh(self):
        """Fetch the follower data from Twitter.

        Note: This incurs a Twitter API call.
        """
        self._data = list(tweepy.Cursor(self.twitter.followers).items())

    @property
    def data(self):
        """The list of followers with details such as user ID, screen name,
        etc.
        """
        if self._data is None:
            self.refresh()
        return self._data

    def all(self):
        """Get the set of follower handles."""
        return set(u.screen_name for u in self.data)

    def named(self):
        """Get the set of named follower handles."""
        with open(self.file_path, 'r') as fp:
            lines = fp.read().splitlines()
        return set(lines)

    def unnamed(self):
        """Get the set of unnamed followers."""
        return self.all() - self.named()

    def add_name_recipient(self, username):
        """Add a username to the list of named followers."""
        assert username in self.all()

        with open(self.file_path, 'a') as fp:
            fp.write("{}\n".format(username))

    @contextlib.contextmanager
    def consume_unnamed(self):
        try:
            picked = random.choice(list(self.unnamed()))
            yield picked
        except Exception:
            raise
        else:
            self.add_name_recipient(picked)
