import string

from .arpa_ipa_mappings import arpa_to_ipa_dict
from .build_phone_dict import (
    add_word_to_oov_file,
    cmu_dict,
    cmu_dict_keys,
    warn_missing_word,
)
from .config import PERMITTED_PUNCTUATION

__all__ = ["convert_label_to_phones", "arpa_to_ipa"]


def convert_label_to_phones(
    label: str,
    ipa: bool = True,
    as_list: bool = True,
    raise_oov: bool = True,
    warn_oov: bool = True,
):
    """Convert an entire label from graphemes to phonemes(IPA)

    label: str - English grapheme label to be converted to IPA
    ipa: bool - If True convert to IPA, else convert to ARPA
    as_list: bool - If True return a list of characters else join them as a string
    raise_oov: bool - If true raise an error if the word isn't found in CMUDict, if False ignore
    warn_oov: bool - If true issue a warnings.Warning if the word isn't found in CMUDict
    """
    phones = []
    label = _clean_label(label, permitted_punctuation=PERMITTED_PUNCTUATION)
    for word in label.split(" "):
        phones.extend(_convert_word_to_phones(word, ipa, raise_oov, warn_oov))
        phones.extend(" ")
    phones = phones[:-1]
    return phones if as_list else "".join(phones)


def is_label_convertible(label):
    clean_label = _clean_label(label, permitted_punctuation=PERMITTED_PUNCTUATION)
    words = [word.lower() for word in clean_label.split(" ")]
    return all([word in cmu_dict_keys for word in words])


def _convert_word_to_phones(
    word: str,
    ipa: bool = True,
    raise_oov: bool = True,
    warn_oov: bool = True,
):
    """Internal method for converting a word from graphemes to IPA or ARPA\

    Args:
    word: str - The English word to be converted
    ipa: bool - If true convert to IPA, else convert to ARPA
    raise_oov: bool - If true raise an error if the word isn't found in CMUDict, if False ignore
    warn_oov: bool - If true issue a warnings.Warning if the word isn't found in CMUDict
    """
    results = cmu_dict.get(word.lower(), "")
    if not results:
        add_word_to_oov_file(word)
        if warn_oov:
            warn_missing_word(word)
        if raise_oov:
            raise ValueError(f"{word} not found in vocabulary")
        return ""
    # TODO: Find a way to handle returning multiple values, keep in mind this
    #       is a helper to convert_label_to_phones and a label may have multiple
    #       words with multiple pronunciations
    arpa_list = _clean_results(results[0])
    return arpa_to_ipa(arpa_list) if ipa else arpa_list


def arpa_to_ipa(arpa_list):
    """Convert a single word from ARPA to Intenational Phonetic Alphabet"""
    return [arpa_to_ipa_dict[arpa] for arpa in arpa_list if arpa != ""]


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
    # label = _strip_nums(label)
    label = _strip_punctuation(label, permitted_punctuation, trim_permitted)
    label = _remove_multiple_spaces(label)
    return label.strip()


def _strip_nums(s):
    return "".join([t for t in s if not t.isdigit()])


def _remove_multiple_spaces(s):
    return " ".join(s.strip().split())
