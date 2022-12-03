# Relative Paths:
import os
from unco import UNCO_PATH

#CSV Reader:
from unco.data import Reader

def test_data_reader_read_csv_data():
    path = os.path.join(UNCO_PATH, "tests/test_data/csv_testdata/unittest_readersv")
    data = Reader(path).read()
    assert list(data)[2][2] == "Zaubereiministerium"