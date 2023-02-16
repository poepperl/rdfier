# Relative Path:
from src.unco import UNCO_PATH
from pathlib import Path

# UNCO Classes
from src.unco.data import Reader, Dataset
from src.unco.features import RDFGenerator

def test_data_reader_read_csv_data():
    path = Path(UNCO_PATH, "tests/test_data/csv_testdata/unittest_reader.csv")
    data = Reader(str(path)).read()
    assert data.iat[1,3] == "Zaubereiministerium"

def test_generate_triple_plan():
    dataset = Dataset(str(Path(UNCO_PATH, "tests/test_data/csv_testdata/eingabeformat.csv")))
    generator = RDFGenerator(dataset)
    generator._generate_triple_plan()
    assert generator.triple_plan["**"] == {'subject': {1, 2, 4}, 'object': {0}} and '1' in generator.triple_plan