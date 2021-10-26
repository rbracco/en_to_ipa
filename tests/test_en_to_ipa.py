import pytest

import en_to_ipa.en_to_ipa as en_to_ipa


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
    assert airpower == ["ɛɪ", "ɹ", "p", "ɑʊ", "ʌɹ"]


def test_convert_label_to_ipa_list2():
    russians = en_to_ipa.convert_label_to_phones("russians", ipa=True, as_list=True)
    assert russians == ["ɹ", "ʌ", "ʃ", "ʌ", "n", "z"]


def test_convert_label_to_ipa_str1():
    tinderbox = en_to_ipa.convert_label_to_phones("tinderbox", ipa=True, as_list=False)
    assert tinderbox == "tɪndʌɹbɑks"


def test_convert_label_to_ipa_str2():
    sneaky = en_to_ipa.convert_label_to_phones("sneaky", ipa=True, as_list=False)
    assert sneaky == "sniki"


def test_no_regression_nauseating():
    nauseating = en_to_ipa.convert_label_to_phones("nauseating", ipa=False, as_list=True)
    assert nauseating == ["n", "ao", "z", "iy", "ey", "t", "ih", "ng"]


def test_no_regression_beer():
    beer = en_to_ipa.convert_label_to_phones("beer", ipa=False, as_list=True)
    assert beer == ["b", "iy", "r"]


def test_no_regression_and():
    and_arpa = en_to_ipa.convert_label_to_phones("and", ipa=False, as_list=True)
    assert and_arpa == ["ae", "n", "d"]


@pytest.mark.xfail(raises=ValueError)
def test_oov_word_raises():
    en_to_ipa._convert_word_to_phones("ksdfklsdfklksdfksdf", warn_oov=False)


@pytest.mark.xfail(raises=ValueError)
def test_oov_label_raises():
    en_to_ipa.convert_label_to_phones("There is a ksdfklsdfklksdfksdf today", warn_oov=False)
