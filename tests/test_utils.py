import string

from hypothesis import given
from hypothesis.strategies import text

import en_to_ipa.utils as utils


def test_strip_punctuation():
    pass


@given(text())
def test_remove_multiple_spaces_hypothesis(s):
    # Add a bunch of multispaces in addition to what might already be in s
    s = s + "  " + s + "      " + s
    assert "  " not in utils._remove_multiple_spaces(s)


def test_remove_multiple_spaces_fixed():
    multispace = "Hello, this 1  is a sentence    with  multiple spaces."
    single_space = "Hello, this 1 is a sentence with multiple spaces."
    assert utils._remove_multiple_spaces(multispace) == single_space


@given(text().filter(lambda x: any([c.isdigit() for c in x])))
def test_remove_nums(s):
    """Starting with text containing digits, ensure all digits are stripped out"""
    stripped = set(utils._remove_nums(s))
    assert set(string.digits).intersection(stripped) == set()


def test_clean_arpa_list_removes_nums():
    assert utils._clean_arpa_list(["AY0", "B1"]) == ["ay", "b"]


def test_clean_arpa_list_strips_whitespace():
    assert utils._clean_arpa_list([" AY0   ", "B1\n"]) == ["ay", "b"]
