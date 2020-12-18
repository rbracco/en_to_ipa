import pytest
import en_to_ipa.arpa_ipa_mappings


@pytest.fixture(scope="session")
def arpa_to_ipa_dict():
    return en_to_ipa.arpa_ipa_mappings.arpa_to_ipa_dict


def test_dict_loads(arpa_to_ipa_dict):
    assert len(arpa_to_ipa_dict.keys()) > 10


def test_immutable_sounds(arpa_to_ipa_dict):
    assert arpa_to_ipa_dict["m"] == "m"
    assert arpa_to_ipa_dict["aa"] == "ɑ"
    assert arpa_to_ipa_dict["epi"] == "silence"
