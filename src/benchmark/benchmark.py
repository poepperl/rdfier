import pandas as pd
from unco import UNCO_PATH
from unco.data.rdf_data import RDFData
from unco.features.graph_generator import GraphGenerator
from pathlib import Path
from time import time


class Benchmark:
    """
        Class that represents the dataset of an unco input.

    Attributes
    ----------
    data : pd.DataFrame
        DataFrame wich includes the data from Reader.
    triple_plan: dict
        Dictionary to save which columns are interpreted as subjects and their corresponding object columns. 
    types_and_languages: dict
        Dictionary to save the datatype or language of a value.
    uncertainty_flags: dict
        Dictionary to save some uncertainty flags. A flag is saved as: uncertainty_flags[column_indices] = list(row_indices)
    alternatives: dict
        Dictionary to save some alternatives for all uncertain values. The slternatives are saved as: alternatives[(row,column)] = list(alternatives)
    """

    def __init__(self, rdfdata : RDFData, prefixes_path : str) -> None:
        """
        Parameters
        ----------
        rdfdata : RDFData
            Object which contains the data of the rdf graph.
        """
        self.rdfdata = rdfdata
        self.prefixes_path = prefixes_path
        self.graph_generator : GraphGenerator
        self.NUMB_LOOPS = 8

    def _generate_graph_with_model(self, model_id : int) -> None:
        self.graph_generator = GraphGenerator(self.rdfdata)
        self.graph_generator.load_prefixes(self.prefixes_path)
        self.graph_generator.generate_solution(model_id)


    def run_query_of_model(self, query_id : int, model_id : int) -> pd.DataFrame:
        """ 
            Method which takes the SPARQL query "src/benchmark/queries/model{model_id}/query{query_id}.rq" and runs the query on self.graph.
            Outputs the DataFrame of the SPARQL result.

        Attributes
        ----------
        query_id : int
            Query id of the saved query.
        model_id : int
            Model id of the implemented model.
        """
        if (query_path := Path(UNCO_PATH,f"src/benchmark/queries/model{model_id}/query{query_id}.rq")).is_file():
            query = query_path.read_text()
            return self.graph_generator.run_query(query)
        else:
            print(f"Warning: Doesn't found query{query_id} for model {model_id}.")
            return pd.DataFrame()
        
    
    def start_benchmark(self):
        time_results = dict()
        for model_numb in range(1,9):
            self._generate_graph_with_model(model_numb)
            query_times = dict()
            for query_numb in range(1,6):
                loop = []
                for _ in range(self.NUMB_LOOPS):
                    start_time = time()
                    _ = self.run_query_of_model(query_numb,model_numb)
                    time_difference = time() - start_time
                    loop.append(time_difference)
                query_times[query_numb] = loop
            time_results[model_numb] = query_times
        
        return time_results


if __name__ == "__main__":
    # file = open(str(Path(UNCO_PATH,"tests/test_data/csv_testdata/eingabeformat.csv")), encoding='utf-8')
    # prefixes = str(Path(UNCO_PATH,"tests/test_data/csv_testdata/namespaces.csv"))

    # rdfdata = RDFData(pd.read_csv(file))
    # generator = GraphGenerator(rdfdata)
    # generator.load_prefixes(prefixes)
    # generator.generate_solution(xml_format=False)

    # test_query = Path(UNCO_PATH,"src/benchmark/queries/model1/query5.rq").read_text()
    
    # print(generator.run_query(test_query))

    input = open(Path(UNCO_PATH,r"tests\testdata\afe\afemapping_1_public_changed.csv"), encoding='utf-8')
    rdfdata = RDFData(pd.read_csv(input))
    bench = Benchmark(rdfdata,str(Path(UNCO_PATH,r"tests\testdata\afe\namespaces.csv")))
    print(bench.start_benchmark())