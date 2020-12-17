import json
import warnings
import cmudict
from config import PATH_OOV_DICT


def read_json(fname, encoding="utf-8"):
    with open(fname, "r", encoding=encoding) as f:
        return json.load(f)


def write_json(fname, obj, encoding="utf-8"):
    with open(fname, "w", encoding=encoding) as f:
        return json.dump(f, obj)


def warn_missing_word(word):
    warnings.warn(f"'{word}' not found in cmudict", KeyError)
    with open(PATH_OOV_DICT, "r+") as f:
        words = [line.strip() for line in f]
        if word not in words:
            f.write(word + "\n")


def get_oov_pronunciations(cmu_dict):
    oov_dict = read_json("data/oov_dict.json")
    # There's a bug where T'S is translated as TS but should be T S
    oov_dict = {k: v.replace("TS", "T S") for k, v in oov_dict.items()}
    return oov_dict


def load_cmu_dict():
    cmu_dict = cmudict.dict()
    oov_dict = get_oov_pronunciations(cmu_dict)
    cmu_dict.update(oov_dict)
    return cmu_dict


cmu_dict = load_cmu_dict()
