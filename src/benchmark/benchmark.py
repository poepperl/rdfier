import pandas as pd
from unco import UNCO_PATH
from unco.data.rdf_data import RDFData
from unco.features.graph_generator import GraphGenerator
from pathlib import Path


if __name__ == "__main__":
    file = open(str(Path(UNCO_PATH,"tests/test_data/csv_testdata/eingabeformat.csv")), encoding='utf-8')
    prefixes = str(Path(UNCO_PATH,"tests/test_data/csv_testdata/namespaces.csv"))

    rdfdata = RDFData(pd.read_csv(file))
    generator = GraphGenerator(rdfdata)
    generator.load_prefixes(prefixes)
    generator.generate_solution(xml_format=False)

    test_query = Path(UNCO_PATH,"src/benchmark/queries/model1/query5.rq").read_text()
    
    print(generator.run_query(test_query))