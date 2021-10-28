import pytest

import en_to_ipa.arpa_ipa_mappings as mappings
from en_to_ipa.build_phone_dict import load_cmu_dict


@pytest.fixture(scope="session")
def local_cmu_dict():
    cmu_dict, _ = load_cmu_dict()
    return cmu_dict


@pytest.fixture(scope="session")
def local_cmu_dict_plus():
    _, cmu_dict_plus = load_cmu_dict()
    return cmu_dict_plus


def test_dict_loads(local_cmu_dict):
    assert len(local_cmu_dict.items()) > 5000


def test_oov_dict_loads(local_cmu_dict_plus):
    assert local_cmu_dict_plus.get("fashionitis", "")
    assert local_cmu_dict_plus.get("invitingly", "")


def test_oov_dict_has_orig_keys(local_cmu_dict, local_cmu_dict_plus):
    for word in local_cmu_dict.keys():
        assert word in local_cmu_dict_plus


def test_common_word_found(local_cmu_dict):
    assert local_cmu_dict.get("difference", "")


def test_oov_word_not_found(local_cmu_dict):
    assert not local_cmu_dict.get("jkdfskjfsjkf", "")


def test_ts_bug(local_cmu_dict):
    all_results = local_cmu_dict.values()
    for result_list in all_results:
        for result in result_list:
            assert "TS" not in result and "ts" not in result


def test_valid_arpabet(local_cmu_dict):
    """Regression test to prevent typos after manually editing CMUDict"""
    arpa_symbols = set()
    valid_arpa = _get_valid_arpa_chars()
    for arpa_transcriptions in local_cmu_dict.values():
        for arpa_transcription in arpa_transcriptions:
            arpa_symbols = arpa_symbols.union({a.lower() for a in arpa_transcription})
    assert arpa_symbols.issubset(valid_arpa)


def _get_valid_arpa_chars():
    valid_arpa = set(mappings.arpa_to_ipa_dict.keys())
    poss_intonations = []
    for i in range(3):
        poss_intonations.append({c + str(i) for c in valid_arpa})
    valid_arpa = valid_arpa.union(*poss_intonations)
    return valid_arpa
