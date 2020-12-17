from config import REPLACE_DIPHTHONGS

vowel_maps = {
    "aa": "ɑ",
    "ae": "æ",
    "ah": "ʌ",
    "ao": "ɔ",
    "aw": "ɑʊ" if REPLACE_DIPHTHONGS else "aʊ",
    "ax": "ə",
    "axr": "ɚ",
    "ay": "ɑɪ" if REPLACE_DIPHTHONGS else "aɪ",
    "eh": "ɛ",
    "er": "ʌɹ" if REPLACE_DIPHTHONGS else "ɝ",
    "ey": "ɛɪ" if REPLACE_DIPHTHONGS else "eɪ",
    "ih": "ɪ",
    "ix": "ɪ",
    "iy": "i",
    "ow": "oʊ",
    "oy": "ɔɪ",
    "uh": "ʊ",
    "uw": "u",
    "ux": "u",
}
# dx is the flap like tt in butter, arpabet says it translates to ɾ in ipa
# but im not so sure
# nx is another one to be careful with, it translates to either ng or n as in winner
# wh is meant to be wh like why/when/where but most ipa consider it a w
cons_maps = {
    "ch": "ʧ",
    "dh": "ð",
    "dx": "ɾ",
    "el": "l",
    "em": "m",
    "en": "n",
    "hh": "h",
    "jh": "ʤ",
    "ng": "ŋ",
    "nx": "n",
    "q": "ʔ",
    "r": "ɹ",
    "sh": "ʃ",
    "th": "θ",
    " ": " ",
    "wh": "w",
    "y": "j",
    "zh": "ʒ",
    "b": "b",
    "d": "d",
    "f": "f",
    "g": "g",
    "k": "k",
    "l": "l",
    "m": "m",
    "n": "n",
    "p": "p",
    "s": "s",
    "t": "t",
    "v": "v",
    "w": "w",
    "z": "z",
}

# these are maps that only timit uses, not arpanet
timit_specific_maps = {
    "ax-h": "ə",
    "bcl": "b",
    "dcl": "d",
    "eng": "ŋ",
    "gcl": "g",
    "hv": "h",
    "kcl": "k",
    "pcl": "p",
    "tcl": "t",
    "pau": "silence",
    "epi": "silence",
    "h#": "silence",
}

arpa_to_ipa_dict = {**vowel_maps, **cons_maps, **timit_specific_maps}
