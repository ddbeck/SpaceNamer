import json
import random

import click

from spacenamer.followers import Followers
from spacenamer.publisher import authenticate, generate_status, post


@click.command()
@click.option('--keysfile', '-k', type=click.File('r'))
@click.option('--followersfile', '-f', type=click.Path())
@click.option('--dryrun', is_flag=True)
@click.argument('word', default=None, required=False)
def publish(keysfile, followersfile, word=None, dryrun=False):
    keys = json.load(keysfile)['twitter']
    twitter = authenticate(keys['api_key'], keys['api_secret'],
                           keys['access_key'], keys['access_secret'])
    followers = Followers(twitter, followersfile)

    use_followers = random.choice([followers.unnamed(), False])

    if word is None and use_followers:
        with followers.consume_unnamed(dryrun=dryrun) as follower:
            if not dryrun:
                twitter.create_friendship(follower)
            post(twitter, generate_status('@{}'.format(follower)),
                 dryrun=dryrun)
    else:
        post(twitter, generate_status(word), dryrun=dryrun)

if __name__ == '__main__':
    publish()
