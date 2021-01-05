import string

from .config import PERMITTED_PUNCTUATION
from .arpa_ipa_mappings import arpa_to_ipa_dict
from .build_phone_dict import cmu_dict, warn_missing_word

__all__ = ["convert_label_to_phones", "convert_word_to_phones", "arpa_to_ipa"]


def convert_label_to_phones(label, ipa=True, keep_spaces=True, as_list=True, raise_oov_error=True):
    """Convert an entire label from graphemes to phonemes(IPA)"""
    phones = []
    label = _clean_label(label, permitted_punctuation=PERMITTED_PUNCTUATION)
    for word in label.split(" "):
        phones.extend(convert_word_to_phones(word, ipa, raise_oov_error))
        if keep_spaces:
            phones.extend(" ")
    phones = phones[:-1] if keep_spaces else phones
    return phones if as_list else "".join(phones)


def convert_word_to_phones(word, ipa=True, raise_oov_error=True):
    """Convert a word from graphemes to phonemes(IPA)"""
    results = cmu_dict.get(word.lower(), "")
    if not results:
        if raise_oov_error:
            raise ValueError(f"{word} not found in vocabulary")
        else:
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


def _strip_punctuation(s, permitted_punctuation=None, trim_permitted=True):
    """Remove punctuation from a string while leaving permitted_punctuation

    Removes all chars from string.punctuation from the string.
    Args:
    s: str - string to be cleaned
    permitted_punctuation: list - a list of puncutation to not be removed
    trim_permitted: bool - True if you want to strip the chars in permitted_
    punctuation from the margins. For instance '-' may be permitted between words
    but may need to be stripped from the start or end of the label
    """

    all_punc = set(string.punctuation)
    allowed = set(permitted_punctuation) if permitted_punctuation is not None else set()
    exclude = all_punc - allowed

    out = "".join(c for c in s if c not in exclude)
    if trim_permitted:
        out = out.strip("".join(allowed))
    return out


def _clean_label(label, permitted_punctuation, trim_permitted=True):
    label = _strip_nums(label)
    label = _strip_punctuation(label, permitted_punctuation, trim_permitted)
    label = _remove_multiple_spaces(label)
    return label.strip()


def _strip_nums(s):
    return "".join([t for t in s if not t.isdigit()])


def _remove_multiple_spaces(s):
    return " ".join(s.strip().split())
