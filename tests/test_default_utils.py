# Relative Paths:
import os
import unco

#CSV Reader:
from unco.data.reader import csvreader


UNCO_PATH = unco.getUscoPath()

def test_data_reader_read_csv_data():
    path = os.path.join(UNCO_PATH, "tests/test_data/csv_testdata/unittest_reader.csv")
    data = csvreader.CSVReader(path).read()
    assert list(data)[2][2] == "Zaubereiministerium"