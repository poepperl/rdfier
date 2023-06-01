import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from unco import UNCO_PATH
from unco.data.rdf_data import RDFData
from unco.features.graph_generator import GraphGenerator
from pathlib import Path
from time import time

NUMB_LOOPS = 10

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
            # return self.graph_generator.graph.query(query).serialize(destination=str(Path(UNCO_PATH,r"data\output\query_results.csv")),format="xml")
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
                print(f"Run query {query_numb} of model {model_numb}.")
                for _ in range(NUMB_LOOPS):
                    start_time = time()
                    _ = self.run_query_of_model(query_numb,model_numb)
                    time_difference = time() - start_time
                    loop.append(time_difference*10)
                query_times[query_numb] = loop
            time_results[model_numb] = query_times
        
        return time_results
    
    def plot_box_plot(self, list_of_lists : list):
        plt.style.use('_mpl-gallery')

        _, ax = plt.subplots()
        ax.boxplot(list_of_lists)

        ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
            ylim=(0, 8), yticks=np.arange(1, 8))

        plt.show()


if __name__ == "__main__":
    # file = open(str(Path(UNCO_PATH,"tests/test_data/csv_testdata/eingabeformat.csv")), encoding='utf-8')
    # prefixes = str(Path(UNCO_PATH,"tests/test_data/csv_testdata/namespaces.csv"))

    # rdfdata = RDFData(pd.read_csv(file))
    # generator = GraphGenerator(rdfdata)
    # generator.load_prefixes(prefixes)
    # generator.generate_solution(xml_format=False)

    # test_query = Path(UNCO_PATH,"src/benchmark/queries/model1/query5.rq").read_text()
    
    # print(generator.run_query(test_query))

    # input = open(Path(UNCO_PATH,"data/input/afemapping_1_public_changed.csv"), encoding='utf-8')
    input = open(Path(UNCO_PATH,"data/input/test_eingabeformat/eingabeformat.csv"), encoding='utf-8')
    rdfdata = RDFData(pd.read_csv(input))
    # bench = Benchmark(rdfdata,str(Path(UNCO_PATH,"data/input/namespaces.csv")))
    bench = Benchmark(rdfdata,str(Path(UNCO_PATH,"data/input/test_eingabeformat/namespaces.csv")))

    model = 3
    bench._generate_graph_with_model(model)
    print(bench.run_query_of_model(6,model))

    # dictionary = bench.start_benchmark()

    # for query_numb in range(1,6):
    #     query_results = []
    #     for model_numb in range(1,9):
    #         model_list = []
    #         for loop in range(NUMB_LOOPS):
    #             model_list.append(dictionary[model_numb][query_numb][loop])
    #         query_results.append(model_list)
    #     print(query_results)
    #     bench.plot_box_plot(query_results)