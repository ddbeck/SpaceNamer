from __future__ import division

import string

from spacenamer import words


def contains_elem_starting_with(iterable, letter):
    for element in iterable:
        if element.startswith(letter):
            return True


def contains_words_starting_with_alphabet(iterable):
    for letter in string.ascii_uppercase:
        assert contains_elem_starting_with(iterable, letter)


class TestWordLists(object):
    def test_adjectives_covers_alphabet(self):
        contains_words_starting_with_alphabet(words.ADJECTIVES)

    def test_nouners_covers_alphabet(self):
        contains_words_starting_with_alphabet(words.NOUNERS)

    def test_planetary_bodies_covers_alphabet(self):
        contains_words_starting_with_alphabet(words.PLANETARY_BODIES)

    def test_weighted_planetary_bodies_is_weighted_correctly(self):
        """Get close to picking a major planet 50% of the time."""
        major_count = 0
        for planet in words.MAJOR_BODIES:
            major_count += words.WEIGHTED_PLANETARY_BODIES.count(planet)

        minor_count = 0
        for body in words.MINOR_BODIES:
            minor_count += words.WEIGHTED_PLANETARY_BODIES.count(body)

        weighted_planets = len(words.WEIGHTED_PLANETARY_BODIES)
        major_ratio = major_count / weighted_planets
        minor_ratio = minor_count / weighted_planets

        assert len(words.MAJOR_BODIES) < len(words.MINOR_BODIES)
        assert major_count + minor_count == weighted_planets
        assert 0 < minor_ratio < 0.50
        assert 0.49 < major_ratio < 0.51
