import pytest
from en_to_ipa.build_phone_dict import load_cmu_dict


@pytest.fixture(scope="session")
def local_cmu_dict():
    return load_cmu_dict()


def test_dict_loads(local_cmu_dict):
    assert len(local_cmu_dict.items()) > 5000


def test_oov_dict_loads(local_cmu_dict):
    print(local_cmu_dict.get("fashionitis", ""))
    assert local_cmu_dict.get("fashionitis", "")
    assert local_cmu_dict.get("invitingly", "")


def test_common_word_found(local_cmu_dict):
    print(local_cmu_dict.get("the", ""))
    assert local_cmu_dict.get("difference", "")


def test_oov_word_not_found(local_cmu_dict):
    assert not local_cmu_dict.get("jkdfskjfsjkf", "")


def test_ts_bug(local_cmu_dict):
    all_results = local_cmu_dict.values()
    for result_list in all_results:
        for result in result_list:
            assert "TS" not in result and "ts" not in result
