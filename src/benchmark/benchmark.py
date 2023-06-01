import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy
from tqdm import tqdm
from statistics import median
from unco import UNCO_PATH
from unco.data.rdf_data import RDFData
from unco.data.uncertainty_generator import UncertaintyGenerator
from unco.features.graph_generator import GraphGenerator
from pathlib import Path
from time import time

NUMB_LOOPS = 5

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

    def _generate_graph_with_model(self, rdfdata : RDFData, model_id : int) -> None:
        self.graph_generator = GraphGenerator(rdfdata)
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


    def start_benchmark_increasing_uncertainties(self):
        query_results = []
        for query_numb in range(1,2):
            X = range(0, len(self.rdfdata.data), 100)[:]
            results = []
            for model_numb in [1,2,3,4,5,6,7,8]:
                model_results = []
                for i in X:
                    ugen = UncertaintyGenerator(deepcopy(self.rdfdata))
                    rdf_data = ugen.add_pseudorand_uncertainty_flags([2,3,4,5,6,9,10,11,12,18,19,20,21],min_uncertainties_per_column=i,max_uncertainties_per_column=i) if i != 0 else rdfdata
                    self._generate_graph_with_model(rdf_data, model_numb)
                    loop = []
                    print(f"Run query {query_numb} of model {model_numb} with {len(rdf_data.uncertainties)} uncertainties. Graph size: {len(self.graph_generator.graph)}")
                    for _ in tqdm(range(NUMB_LOOPS)):
                        start_time = time()
                        _ = self.run_query_of_model(query_numb,model_numb)
                        time_difference = time() - start_time
                        loop.append(time_difference)
                    model_results.append(median(loop))
                results.append(model_results)
            query_results.append(results)

        for i, res in enumerate(query_results):
            plt.plot(X, res[0], color='r', label='1')
            plt.plot(X, res[1], color='b', label='2')
            plt.plot(X, res[2], color='g', label='3')
            plt.plot(X, res[3], color='y', label='4')
            plt.plot(X, res[4], color='m', label='5')
            plt.plot(X, res[5], color='c', label='6')
            plt.plot(X, res[6], color='k', label='7')
            plt.plot(X, res[7], color='y', label='8')

            plt.xlabel("#Uncertainties")
            plt.ylabel("Time")
            plt.title(f"Query {i+1} with increasing numb uncertainties")

            plt.legend()

            plt.show()
        
        return query_results

if __name__ == "__main__":
    # Load data-------------------------------------------------------------------------------------------------------------------------
    input = open(Path(UNCO_PATH,"tests/testdata/afe/afemapping_changed_1000rows.csv"), encoding='utf-8')
    rdfdata = RDFData(pd.read_csv(input))
    bench = Benchmark(rdfdata,str(Path(UNCO_PATH,"tests/testdata/afe/namespaces.csv")))

    # Test query of model---------------------------------------------------------------------------------------------------------------
    # model = 3
    # bench._generate_graph_with_model(model)
    # print(bench.run_query_of_model(6,model))

    # Run benchmark models/queries------------------------------------------------------------------------------------------------------
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
    
    # Run benchmark numb of uncertainties------------------------------------------------------------------------------------------------
    print(bench.start_benchmark_increasing_uncertainties())
