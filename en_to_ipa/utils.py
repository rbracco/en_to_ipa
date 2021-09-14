import string
from typing import Collection


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
