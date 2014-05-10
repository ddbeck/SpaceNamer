"""Word collections and collectors."""

import codecs
import json
import os

DATA_FILES_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'data'
)
PLANETS_FILE = os.path.join(DATA_FILES_PATH, 'planets.json')
NOUNS_FILE = os.path.join(DATA_FILES_PATH, 'nouns.json')
ADJECTIVES_FILE = os.path.join(DATA_FILES_PATH, 'adjs.json')

SPACE_ADJECTIVES_FILE = os.path.join(DATA_FILES_PATH, 'space_adjs.json')
SPACE_NOUNS_FILE = os.path.join(DATA_FILES_PATH, 'space_nouns.json')

WORDS_FILE = os.path.join(DATA_FILES_PATH, 'words.json')


def capitalize(words):
    """Capitalize every string in ``words``.
    """
    return list(w[0].capitalize() + w[1:] for w in words)


def adjectives():
    """Get a list of adjectives."""
    with open(ADJECTIVES_FILE) as fp:
        adjs = json.load(fp)['adjs']

    with codecs.open(SPACE_ADJECTIVES_FILE, "r", "utf-8") as fp:
        adjs.extend(json.load(fp)['adjs'])

    # cover whole alphabet
    adjs.append('Yellow')
    adjs.append('Zoological')

    adjs = capitalize(adjs)
    return list(adjs)


def nouners():
    """Get a list of nouns ending in -er or -or."""
    with open(NOUNS_FILE) as fp:
        nouns = json.load(fp)['nouns']

    with codecs.open(SPACE_NOUNS_FILE, "r", "utf-8") as fp:
        nouns.extend(json.load(fp)['nouns'])

    # cover whole alphabet
    nouns.append('Kicker')
    nouns.append('Quoter')
    nouns.append('Upper')
    nouns.append('Voter')
    nouns.append('Weigher')
    nouns.append('X-rayer')
    nouns.append('Zapper')

    nouns = capitalize(nouns)
    # nouns = (n for n in nouns if n.endswith('er') or n.endswith('or'))
    return list(nouns)


def planetary_body_names():
    """Get a list of planetary bodies.
    """
    with open(PLANETS_FILE) as fp:
        planets = json.load(fp)['planets']

    all_bodies = []
    for planet in planets:
        all_bodies.append(planet['name'])
        all_bodies.extend(planet['moons'])

    # I wanted to be able to cover the entire alphabet, and the IAU doesn't
    # list any planets or moons starting with Q, W, X and Z, yet. So I had to
    # add a few more planetary objects.
    all_bodies.extend(['Quaoar', 'Weywot'])  # a likely planet and its moon
    all_bodies.append('X planet')  # Keep things weird
    all_bodies.append('Zelinda')  # 654 Zelinda is an asteroid.

    return list(sorted(all_bodies))


def major_planets():
    """Get a list of major planets."""
    with open(PLANETS_FILE) as fp:
        planets = json.load(fp)['planets']

    return list(planet['name'] for planet in planets)


def minor_planets():
    """Get a list of minor planets."""
    return list(body for body in planetary_body_names()
                if body not in major_planets())


def words():
    """Just a bunch of words."""
    with open(WORDS_FILE) as fp:
        words = json.load(fp)['words']

    return list(word for word in words)


ADJECTIVES = adjectives()
NOUNERS = nouners()
MAJOR_BODIES = major_planets()
MINOR_BODIES = minor_planets()
PLANETARY_BODIES = list(sorted(MAJOR_BODIES + MINOR_BODIES))
# and probably the dumbest thing in this module
# it's 14 times because that's about what it takes such that the major bodies
# show up ~50% of the time.
WEIGHTED_PLANETARY_BODIES = list(sorted(MAJOR_BODIES * 14 + MINOR_BODIES))
WORDS = words()

__all__ = ['ADJECTIVES', 'NOUNERS', 'MAJOR_BODIES', 'MINOR_BODIES',
           'PLANETARY_BODIES', 'WEIGHTED_PLANETARY_BODIES', 'WORDS']
