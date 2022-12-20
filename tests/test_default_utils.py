# Relative Paths:
import os
from src.unco import UNCO_PATH

# CSV Reader:
from src.unco.data import Reader


def test_data_reader_read_csv_data():
    path = os.path.join(UNCO_PATH, "tests/test_data/csv_testdata/unittest_reader.csv")
    data = Reader(path).read()
    assert data.iat[1,3] == "Zaubereiministerium"
