import string

from .config import PERMITTED_PUNCTUATION
from .arpa_ipa_mappings import arpa_to_ipa_dict
from .build_phone_dict import cmu_dict, warn_missing_word

__all__ = ["convert_label_to_phones", "convert_word_to_phones", "arpa_to_ipa"]


def convert_label_to_phones(label, ipa=True, keep_spaces=True, as_list=True):
    """Convert an entire label from graphemes to phonemes(IPA)"""
    phones = []
    label = _clean_label(label, permitted_punctuation=PERMITTED_PUNCTUATION)
    for word in label.split(" "):
        phones.extend(convert_word_to_phones(word, ipa))
        if keep_spaces:
            phones.extend(" ")
    phones = phones[:-1] if keep_spaces else phones
    return phones if as_list else "".join(phones)


def convert_word_to_phones(word, ipa=True):
    """Convert a word from graphemes to phonemes(IPA)"""
    results = cmu_dict.get(word.lower(), "")
    if not results:
        warn_missing_word(word)
        return ""
    arpa_list = _clean_results(results[0])
    # if ipa, convert arpa to ipa, otherwise remove spaces from the word
    return arpa_to_ipa(arpa_list) if ipa else arpa_list


def arpa_to_ipa(arpa_list):
    """Convert a single word from ARPA to Intenational Phonetic Alphabet"""
    return [arpa_to_ipa_dict[arpa] for arpa in arpa_list]


def _clean_results(results):
    return [_clean_result(result) for result in results]


def _clean_result(result):
    """Strip comments, lowercase, extra whitespace, and numbers"""
    result = result.split("#")[0].strip().lower()
    return _strip_nums(result)


def _clean_label(label, permitted_punctuation):
    label = _strip_nums(label)
    label = _strip_punctuation(label, permitted_punctuation)
    label = _remove_multiple_spaces(label)
    return label.strip()


def _strip_nums(s):
    return "".join([t for t in s if not t.isdigit()])



def _strip_punctuation(s, permitted_punctuation=None):


    all_punc = set(string.punctuation)
    allowed = set(permitted_punctuation) if permitted_punctuation is not None else set()
    exclude = all_punc - allowed
    return "".join(c for c in s if c not in exclude)


def _remove_multiple_spaces(s):
    return " ".join(s.split())
