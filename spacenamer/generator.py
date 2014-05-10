from __future__ import print_function

import random

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

    # pick a noun for the last letter
    result[-1] = utils.random_by_startswith(word_lists['nouners'], letters[-1])
    budget -= len(result[-1])

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

    return result


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
