from __future__ import print_function

import itertools
import random
import re

import click

import words
import utils

DEFAULT_WORD_LISTS = {
    'bodies': words.WEIGHTED_PLANETARY_BODIES,
    'nouners': words.NOUNERS,
    'adjectives': words.ADJECTIVES,
}


class UnsatisfiableBudgetError(Exception):
    pass


def spacename(word, word_lists=DEFAULT_WORD_LISTS, budget=float('inf')):
    """Generate an instrument name based on the letters of ``word``.

    ``word`` must be a string-like object with one or more letters.
    """
    if not word:
        raise ValueError("can't make a spacename without letters")

    letters = list(c for c in word.upper())
    result = [None for c in letters]

    # don't convert numbers into words
    for index, c in enumerate(letters):
        if c in '0123456789':
            result[index] = c

    # pick a noun for the last unused letter
    last_unused_word_index = len(result) - 1
    for index, c in enumerate(result):
        if c is None:
            last_unused_word_index = index

    result[last_unused_word_index] = utils.random_by_startswith(
        word_lists['nouners'], letters[last_unused_word_index])
    budget -= len(result[last_unused_word_index])

    # if it's only one word, it's time to skip
    if all(result):
        return result

    # pick a planet for a random remaining letter
    remaining_indicies = [index for index, value in enumerate(result)
                          if value is None]
    planet_index = random.choice(remaining_indicies)
    planet_letter = letters[planet_index]
    result[planet_index] = utils.random_by_startswith(word_lists['bodies'],
                                                      planet_letter)
    budget -= len(result[planet_index])

    for index, value in enumerate(result):
        if value is None:
            try:
                budgeted_words = utils.filter_by_budget(
                    word_lists['adjectives'],
                    budget
                )
                result[index] = utils.random_by_startswith(budgeted_words,
                                                           letters[index])
            except ValueError:
                msg = ('could not find an adjective <={0} characters long '
                       'starting with {1}')
                raise UnsatisfiableBudgetError(msg.format(budget,
                                                          letters[index]))
            budget -= len(result[index])

    result = combine_numbers(result)

    return result


RE_NUMBER = re.compile('\d+')


def is_numeric(s):
    if RE_NUMBER.match(s):
        return True
    else:
        return False


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return itertools.izip_longest(*args, fillvalue=fillvalue)


def combine(a, b):
    if is_numeric(a) and is_numeric(b):
        yield "{}{}".format(a, b)
    else:
        yield a
        yield b


def _combine(seq):
    while seq:
        if len(seq) <= 1:
            yield seq.pop(0)
        else:
            current = seq.pop(0)
            next_ = seq.pop(0)

            if is_numeric(current) and is_numeric(next_):
                current = "{}{}".format(current, next_)
                seq.insert(0, current)
            elif not is_numeric(current) and is_numeric(next_):
                yield current
                seq.insert(0, next_)
            else:
                yield current
                yield next_


def combine_numbers(seq):
    return list(_combine(seq))


@click.command()
@click.option('--budget', '-b', default=107,
              help='number of characters allowed')
@click.argument('word')
def main(budget, word):
    n = ' '.join(spacename(word=word, budget=budget))
    t = '{0}: {1}'.format(word, n)
    print(t)
    print('{0} characters.'.format(len(t)))


if __name__ == '__main__':
    main()
