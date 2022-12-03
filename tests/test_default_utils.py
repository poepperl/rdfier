import re
from unco import get_datetime_postfix
from unco.data import read_utils as data_utils

def test_get_datetime_postfix():
    postfix = get_datetime_postfix()
    assert re.match(r"\d{8}_\d{6}$", postfix) != None

def test_data_utils_get_all_files_in_path_all():
    file_list = data_utils.get_all_files_in_path('tests/test_data')
    assert len(file_list) == 5

def test_data_utils_get_all_files_in_path_json_only():
    file_list = data_utils.get_all_files_in_path('tests/test_data', 'json')
    assert len(file_list) == 1

def test_data_utils_get_all_files_in_path_not_recursive():
    file_list = data_utils.get_all_files_in_path('tests/test_data', recursive=False)
    assert len(file_list) == 0
