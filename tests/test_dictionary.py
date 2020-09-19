import pytest

from audioscraper import dictionary as dt


def test_is_word_white_listed():

    assert dt.is_word_white_listed('de', 'fr', 1)
    assert not dt.is_word_white_listed('reallyrandomworld', 'fr', 1)
