import pytest

import en_to_ipa.en_to_ipa as en_to_ipa


def test_clean_result_removes_num():
    assert en_to_ipa._clean_result("AY0 B") == "ay b"


def test_clean_result_strips_whitespace():
    assert en_to_ipa._clean_result("   AY B   \n") == "ay b"


def test_clean_result_removes_comment():
    assert en_to_ipa._clean_result("AY0 B#This is a comment") == "ay b"


def test_clean_result_cleans_all():
    assert en_to_ipa._clean_result("  AY0 B #This is a comment\n") == "ay b"


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


# def test_convert_word_to_arpa():
#     zebra = en_to_ipa.convert_word_to_phones("Zebra", ipa=False)
#     # assert zebra == ["z", "iy", "b", "r", "ah"]


@pytest.mark.xfail(raises=ValueError)
def test_oov_word_raises():
    en_to_ipa.convert_word_to_phones("ksdfklsdfklksdfksdf", warn_oov=False)


@pytest.mark.xfail(raises=ValueError)
def test_oov_label_raises():
    en_to_ipa.convert_label_to_phones("There is a ksdfklsdfklksdfksdf today", warn_oov=False)
