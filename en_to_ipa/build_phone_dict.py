import json
import warnings
import cmudict
from .config import PATH_OOV_DICT, PATH_OOV_NEW


def read_json(fname, encoding="utf-8"):
    with open(fname, "r", encoding=encoding) as f:
        return json.load(f)


def write_json(fname, obj, encoding="utf-8"):
    with open(fname, "w", encoding=encoding) as f:
        return json.dump(f, obj)


def warn_missing_word(word):
    warnings.warn(f"'{word}' not found in cmudict")


def add_word_to_oov_file(word):
    with open(PATH_OOV_NEW, "r+") as f:
        words = [line.strip() for line in f]
        if word not in words:
            f.write(word + "\n")


def get_oov_pronunciations():
    oov_dict = read_json(PATH_OOV_DICT)
    # There's a bug where T'S is translated as TS but should be T S
    oov_dict = {k: [v.replace("TS", "T S").split(" ")] for k, v in oov_dict.items()}
    return oov_dict


def load_cmu_dict():
    cmu_dict = cmudict.dict()
    oov_dict = get_oov_pronunciations()
    cmu_dict_plus = {**cmu_dict, **oov_dict}
    cmu_dict_plus = {k.lower(): v for k, v in cmu_dict_plus.items()}
    return cmu_dict, cmu_dict_plus


cmu_dict, cmu_dict_plus = load_cmu_dict()
cmu_dict_keys = cmu_dict.keys()
