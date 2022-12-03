import os


def get_unco_path():
    unco_path = os.path.dirname(__file__)
    return unco_path[:30]


UNCO_PATH = get_unco_path()
