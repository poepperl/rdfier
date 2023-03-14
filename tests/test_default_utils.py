# Relative Path:
from src.unco import UNCO_PATH
from pathlib import Path

# UNCO Classes
from src.unco.data import Reader, RDFData
from src.unco.features import RDFGenerator

def test_data_reader_read_csv_data():
    path = Path(UNCO_PATH, "tests/test_data/csv_testdata/unittest_reader.csv")
    data = Reader(str(path)).read()
    assert data.iat[1,3] == "Zaubereiministerium"

def test_generate_triple_plan():
    dataset = RDFData(str(Path(UNCO_PATH, "tests/test_data/csv_testdata/eingabeformat.csv")))
    generator = RDFGenerator(dataset)
    generator._generate_triple_plan()
    assert generator.triple_plan["**"] == {'object': {1, 2, 4}, 'subject': {0}} and '1' in generator.triple_plan

def test_get_language_or_datatype_from_header():
    dataset = RDFData(str(Path(UNCO_PATH, "tests/test_data/csv_testdata/eingabeformat.csv")))
    generator = RDFGenerator(dataset)
    generator._generate_triple_plan()
    generator._get_datatype_and_language()
    assert generator.column_languages[3] == "en" and generator.column_datatypes[4] == "xsd:decimal"