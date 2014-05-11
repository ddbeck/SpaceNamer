from __future__ import print_function

import json
import random

import click
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


def post(twitter, status):
    """Post status to Twitter."""
    twitter.update_status(status)


@click.command()
@click.option('--keysfile', '-k', type=click.File('r'))
@click.option('--dryrun', is_flag=True)
@click.argument('word', default=None)
def publish(keysfile, word=None, dryrun=False):
    status = generate_status(word)

    if dryrun:
        print(status)
    else:
        keys = json.load(keysfile)['twitter']
        twitter = authenticate(keys['api_key'], keys['api_secret'],
                               keys['access_key'], keys['access_secret'])
        post(twitter, status)


if __name__ == '__main__':
    publish()
