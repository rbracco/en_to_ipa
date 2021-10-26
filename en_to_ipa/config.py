import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_CMU_DICT = os.path.join(ROOT_DIR, "data/cmu_dict.json")
PATH_OOV_DICT = os.path.join(ROOT_DIR, "data/oov_dict.json")
PATH_OOV_NEW = os.path.join(ROOT_DIR, "data/oov_new.txt")

PERMITTED_PUNCTUATION = set(["'", "-"])
REPLACE_DIPHTHONGS = True
