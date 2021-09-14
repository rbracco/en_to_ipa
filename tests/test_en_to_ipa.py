import string

import pytest
from hypothesis import given
from hypothesis.strategies import text

import en_to_ipa.en_to_ipa as en_to_ipa


def test_strip_punctuation():
    pass


@given(text())
def test_remove_multiple_spaces_hypothesis(s):
    # Add a bunch of multispaces in addition to what might already be in s
    s = s + "  " + s + "      " + s
    assert "  " not in en_to_ipa._remove_multiple_spaces(s)


def test_remove_multiple_spaces_fixed():
    multispace = "Hello, this 1  is a sentence    with  multiple spaces."
    single_space = "Hello, this 1 is a sentence with multiple spaces."
    assert en_to_ipa._remove_multiple_spaces(multispace) == single_space


@given(text().filter(lambda x: any([c.isdigit() for c in x])))
def test_remove_nums(s):
    """Starting with text containing digits, ensure all digits are stripped out"""
    stripped = set(en_to_ipa._remove_nums(s))
    assert set(string.digits).intersection(stripped) == set()


def test_clean_arpa_list_removes_nums():
    assert en_to_ipa._clean_arpa_list(["AY0", "B1"]) == ["ay", "b"]


def test_clean_arpa_list_strips_whitespace():
    assert en_to_ipa._clean_arpa_list([" AY0   ", "B1\n"]) == ["ay", "b"]


def test_label_convertible_with_caps():
    assert en_to_ipa.is_label_convertible("Hello This is a SENTENCE")


def test_label_convertible_with_punctuation():
    assert en_to_ipa.is_label_convertible("Hello, This is a sentence!")


def test_label_convertible_with_whitespace():
    assert en_to_ipa.is_label_convertible("    Hello This is a sentence\n")


def test_label_convertible_with_doublespace():
    assert en_to_ipa.is_label_convertible("Hello This is a  sentence")


def test_label_convertible_fails_number():
    assert not en_to_ipa.is_label_convertible("Hello This is 1 sentence")


def test_is_label_convertible_fails_oov():
    assert not en_to_ipa.is_label_convertible("Hello This is awordthatdoesntexist")


def test_is_label_convertible_fails_misspelling():
    assert not en_to_ipa.is_label_convertible("Heello")


def test_all_cmudict_keys_are_convertible():
    assert all([en_to_ipa.is_label_convertible(k)] for k in en_to_ipa.cmu_dict_keys)


def test_convert_label_to_arpa_list1():
    zebra = en_to_ipa.convert_label_to_phones("Zebra", ipa=False, as_list=True)
    assert zebra == ["z", "iy", "b", "r", "ah"]


def test_convert_label_to_arpa_list2():
    muffins = en_to_ipa.convert_label_to_phones("MuFFins", ipa=False, as_list=True)
    assert muffins == ["m", "ah", "f", "ah", "n", "z"]


def test_convert_label_to_arpa_str1():
    ghosts = en_to_ipa.convert_label_to_phones("ghosts", ipa=False, as_list=False)
    assert ghosts == "gowsts"
    # assert zebra == ["z", "iy", "b", "r", "ah"]


def test_convert_label_to_arpa_str2():
    defendant = en_to_ipa.convert_label_to_phones("defendant", ipa=False, as_list=False)
    assert defendant == "dihfehndahnt"


def test_convert_label_to_ipa_list1():
    airpower = en_to_ipa.convert_label_to_phones("airpower", ipa=True, as_list=True)
    assert airpower == ["ɛ", "ɹ", "p", "ɑʊ", "ʌɹ"]


def test_convert_label_to_ipa_list2():
    russians = en_to_ipa.convert_label_to_phones("russians", ipa=True, as_list=True)
    assert russians == ["ɹ", "ʌ", "ʃ", "ʌ", "n", "z"]


def test_convert_label_to_ipa_str1():
    tinderbox = en_to_ipa.convert_label_to_phones("tinderbox", ipa=True, as_list=False)
    assert tinderbox == "tɪndʌɹbɑks"


def test_convert_label_to_ipa_str2():
    sneaky = en_to_ipa.convert_label_to_phones("sneaky", ipa=True, as_list=False)
    assert sneaky == "sniki"


@pytest.mark.xfail(raises=ValueError)
def test_oov_word_raises():
    en_to_ipa._convert_word_to_phones("ksdfklsdfklksdfksdf", warn_oov=False)


@pytest.mark.xfail(raises=ValueError)
def test_oov_label_raises():
    en_to_ipa.convert_label_to_phones("There is a ksdfklsdfklksdfksdf today", warn_oov=False)
