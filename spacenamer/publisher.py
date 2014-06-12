from __future__ import print_function

import random

import tweepy

from spacenamer.generator import spacename
from words import WORDS


def generate_status(word=None):
    if word is None:
        word = random.choice(WORDS)
    word = word.upper()

    budget = 140 - len(word) - len(': ') - ((len(word) - 1))
    sn = ' '.join(spacename(word, budget=budget))
    return '{0}: {1}'.format(word, sn)


def authenticate(api_key, api_secret, access_key, access_secret):
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_key, access_secret)
    return tweepy.API(auth)


def post(twitter, status, dryrun=False):
    """Post status to Twitter."""
    if dryrun is False:
        twitter.update_status(status)
    else:
        print('{} ({})'.format(status, len(status)))
