import pytest
import en_to_ipa
from en_to_ipa import convert_label_to_phones


def test_clean_result():
    assert en_to_ipa.en_to_ipa._clean_result("AY0 B") == "ay b"
    assert en_to_ipa.en_to_ipa._clean_result("   AY B   \n") == "ay b"
    assert en_to_ipa.en_to_ipa._clean_result("AY0 B#This is a comment") == "ay b"
    assert en_to_ipa.en_to_ipa._clean_result("  AY0 B #This is a comment") == "ay b"
