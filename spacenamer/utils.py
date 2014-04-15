"""Various spaceanming utilities."""

import random


def filter_by_budget(seq, budget):
    """Filter ``seq`` such that each element is no longer than ``budget``."""
    return (elem for elem in seq if len(elem) <= budget)


def filter_by_startswith(seq, chars):
    """A generator that filters ``seq`` such that every element in ``seq``
    begins with ``chars``.
    """
    return (elem for elem in seq if elem.startswith(chars))


def random_by_startswith(seq, chars):
    """Randomly select an element from ``seq`` that starts with ``chars``."""
    filtered_seq = list(filter_by_startswith(seq, chars))

    if not filtered_seq:
        msg = "{0!r} does not contain an element starting with {1!r}"
        raise ValueError(msg.format(seq, chars))

    return random.choice(filtered_seq)
