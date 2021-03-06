from py.test import raises

from spacenamer import generator


class TestSpacename(object):
    def test_empty_name(self):
        with raises(ValueError):
            generator.spacename('')

    def test_one_letter_name(self):
        word_lists = {
            'nouners': ['Tester'],
            'bodies': [],
            'adjectives': [],
        }
        assert generator.spacename('T', word_lists) == ['Tester']

    def test_two_letter_name(self):
        word_lists = {
            'nouners': ['Leader'],
            'bodies': ['Adrastea'],
            'adjectives': []
        }
        assert generator.spacename('Al', word_lists) == ['Adrastea', 'Leader']

    def test_three_letter_name(self):
        word_lists = {
            'nouners': ['Nodder'],
            'bodies': ['Jupiter', 'Oberon'],
            'adjectives': ['Janky', 'Oblong'],
        }
        result = generator.spacename('Jon', word_lists)
        assert result[0] in (word_lists['bodies'] + word_lists['adjectives'])
        assert result[1] in (word_lists['bodies'] + word_lists['adjectives'])
        assert result[2] == word_lists['nouners'][0]

    def test_four_letter_name(self):
        word_lists = {
            'nouners': ['Nodder'],
            'bodies': ['Jupiter', 'Oberon', 'Himalia'],
            'adjectives': ['Janky', 'Oblong', 'Hiding'],
        }
        result = generator.spacename('John', word_lists)
        assert result.count('Nodder') == 1
        assert len([w for w in result if w in word_lists['bodies']]) == 1
        assert len([w for w in result if w in word_lists['adjectives']]) == 2

    def test_budgets_letters(self):
        word = 'Vvv'
        word_lists = {
            'nouners': ['Vinter'],
            'bodies': ['Venus'],
            'adjectives': ['V123456789', 'V123'],
        }
        result = generator.spacename(word, word_lists, budget=16)
        assert 'V123456789' not in result

    def test_raises_on_unsatisfiable_budget(self):
        word = 'Vvv'
        word_lists = {
            'nouners': ['Vinter'],
            'bodies': ['Venus'],
            'adjectives': ['V123456789'],
        }
        with raises(generator.UnsatisfiableBudgetError):
            generator.spacename(word, word_lists, budget=16)

    def test_word_has_underscore(self):
        word = 'a_b'
        result = generator.spacename(word)
        assert '_' not in result


class TestCombineNumbers(object):
    def test_basic(self):
        result = generator.combine_numbers(
            ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])

        assert result == ['0123456789']

    def test_alpha_first(self):
        result = generator.combine_numbers(['Alpha', '1', '2', '3'])
        assert result == ['Alpha', '123']

    def test_alpha_middle(self):
        result = generator.combine_numbers(['1', '2', '3', 'Alpha', '4', '5'])
        assert result == ['123', 'Alpha', '45']

    def test_alpha_last(self):
        result = generator.combine_numbers(['1', '2', '3', 'Alpha', 'Beta'])
        assert result == ['123', 'Alpha', 'Beta']
