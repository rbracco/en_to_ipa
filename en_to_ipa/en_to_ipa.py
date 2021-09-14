import string
from typing import Collection, List

from .arpa_ipa_mappings import arpa_to_ipa_dict
from .build_phone_dict import (
    add_word_to_oov_file,
    cmu_dict,
    cmu_dict_keys,
    warn_missing_word,
)
from .config import PERMITTED_PUNCTUATION

__all__ = ["convert_label_to_phones", "arpa_to_ipa", "is_label_convertible"]


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


def is_label_convertible(label: str):
    """Check if a label is convertible to phones

    Args:
    label: str - A string containing English graphemes
    """
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
    arpa_results = cmu_dict.get(word.lower(), "")
    if not arpa_results:
        add_word_to_oov_file(word)
        if warn_oov:
            warn_missing_word(word)
        if raise_oov:
            raise ValueError(f"{word} not found in vocabulary")
        return ""
    # TODO: Find a way to handle returning multiple values, keep in mind this
    #       is a helper to convert_label_to_phones and a label may have multiple
    #       words with multiple pronunciations
    #       OR... find a way to return the one preferred result (pos tagging?)
    top_result = arpa_results[0]
    arpa_list = _clean_arpa_list(top_result)
    return arpa_to_ipa(arpa_list) if ipa else arpa_list


def arpa_to_ipa(arpa_list: List[str]):
    """Convert a single word from ARPA to Intenational Phonetic Alphabet"""
    return [arpa_to_ipa_dict[arpa] for arpa in arpa_list if arpa != ""]


def _clean_arpa_list(arpa_list):
    """Strip lowercase, extra whitespace, and numbers from a list of ARAP characters

    Args:
    arpa_list: List[str] - A list of strings representing ARPA characters e.g. ["AY0", "S", "K"]
    """
    return [_clean_arpa_char(arpa_char) for arpa_char in arpa_list]


def _clean_arpa_char(arpa_char: str):
    """Strip lowercase, extra whitespace, and numbers from an arpa character

    Args:
    arpa_char: str - A string representing an arpa character and intonation e.g. AH0 or K
    """
    arpa_char = arpa_char.strip().lower()
    return _remove_nums(arpa_char)


def _clean_label(label: str, permitted_punctuation: Collection = None, trim_permitted: bool = True):
    """Clean an English label by stripping whitespace removing unwanted punctuation and multiple spaces

    Args:
    label: str - A label containing English graphemes e.g. "This is a sentence!"
    permitted_punctiation: Collection - Punctuation that won't be stripped out of the label, currently "'" and "-"
    trim_permitted: bool - True if you want to strip the chars in permitted_ punctuation from the margins.
    For instance '-' may be permitted between words but may need to be stripped from the start or end of the label
    """
    # label = _remove_nums(label)
    label = _strip_punctuation(label, permitted_punctuation, trim_permitted)
    label = _remove_multiple_spaces(label)
    return label.strip()


def _strip_punctuation(
    s: str, permitted_punctuation: Collection = None, trim_permitted: bool = True
):
    """Remove punctuation from a string while leaving permitted_punctuation

    Removes all chars from string.punctuation from the string.
    Args:
    s: str - string to be cleaned
    permitted_punctiation: Collection - Punctuation that won't be stripped out of the label, currently "'" and "-"
    trim_permitted: bool - True if you want to strip the chars in permitted_ punctuation from the margins.
    For instance '-' may be permitted between words but may need to be stripped from the start or end of the label
    """
    all_punc = set(string.punctuation)
    allowed = set(permitted_punctuation) if permitted_punctuation is not None else set()
    exclude = all_punc - allowed
    out = "".join(c for c in s if c not in exclude)
    if trim_permitted:
        out = out.strip("".join(allowed))
    return out


def _remove_nums(s: str):
    """Remove any numbers from a string. Mainly used to remove intonation numbers from CMUDict results

    Args:
    s: str - A string to remove numbers from.
    """
    return "".join([t for t in s if not t.isdigit()])


def _remove_multiple_spaces(s: str):
    """Replace any instance of multiple spaces with a single space

    s: str - A string to remove multiple spaces from
    """
    return " ".join(s.strip().split())
