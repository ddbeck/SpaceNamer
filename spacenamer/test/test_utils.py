import pytest

from spacenamer import utils


def test_filter_by_startswith():
    word_list = ['Alpha', 'Aardvark', 'Beta', 'Gamma']
    a_words = list(utils.filter_by_startswith(word_list, 'A'))

    assert 'Beta' not in a_words
    assert 'Gamma' not in a_words


class TestRandomByStartswith(object):
    def test_raises_without_options(self):
        with pytest.raises(ValueError):
            utils.random_by_startswith(['A', 'B', 'C'], 'D')

    def test_output_exists_in_input_sequence(self):
        seq = ['A', 'B', 'C']
        result = utils.random_by_startswith(seq, 'A')

        assert result in seq
        assert result == 'A'


class TestFilterByBudget(object):
    def test_nothing_in_budget(self):
        result = list(utils.filter_by_budget(['Areallylongword'], 5))
        assert len(result) == 0

    def test_some_things_in_budget(self):
        result = list(utils.filter_by_budget(['12345', '123456789'], 6))
        assert result == ['12345']

    def test_all_things_in_budget(self):
        word_list = ['Abcd', '1234']
        result = list(utils.filter_by_budget(word_list, 1000))
        assert result == word_list
