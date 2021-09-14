from typing import List

import en_to_ipa.utils as utils
from en_to_ipa.arpa_ipa_mappings import arpa_to_ipa_dict
from en_to_ipa.build_phone_dict import (
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
    label = utils._clean_label(label, permitted_punctuation=PERMITTED_PUNCTUATION)
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
    clean_label = utils._clean_label(label, permitted_punctuation=PERMITTED_PUNCTUATION)
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
    arpa_list = utils._clean_arpa_list(top_result)
    return arpa_to_ipa(arpa_list) if ipa else arpa_list


def arpa_to_ipa(arpa_list: List[str]):
    """Convert a single word from ARPA to Intenational Phonetic Alphabet"""
    return [arpa_to_ipa_dict[arpa] for arpa in arpa_list if arpa != ""]
