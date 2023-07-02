import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy
from tqdm import tqdm
from statistics import median, mean
from unco import UNCO_PATH, data
from unco.data.rdf_data import RDFData
from unco.data.uncertainty_generator import UncertaintyGenerator
from unco.features import fuseki
from unco.features.fuseki import FusekiServer
from unco.features.graph_generator import GraphGenerator
from pathlib import Path
from time import sleep, time

MEDIAN_LOOPS = 11
MEAN_LOOPS = 5

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
        self.prefixes_path = prefixes_path
        self.graph_generator = GraphGenerator(rdfdata)
        self.fserver = FusekiServer(Path(UNCO_PATH,"src/apache-jena-fuseki-4.8.0"))

    def _generate_graph_with_model(self, model_id : int, fuseki : bool) -> None:
        self.graph_generator.load_prefixes(self.prefixes_path)
        self.graph_generator.generate_solution(model_id, xml_format=False)
        if fuseki:
            self.fserver.delete_graph()
            self.fserver.upload_data(str(Path(UNCO_PATH,"data/output/graph.ttl")))

    def run_query_of_model(self, query_id : int, model_id : int, run_on_fuseki : bool = False) -> pd.DataFrame:
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
            return self.graph_generator.run_query(query,save_result=False) if not run_on_fuseki else self.fserver.run_query(query,save_result=False)
            # return self.graph_generator.graph.query(query).serialize(destination=str(Path(UNCO_PATH,r"data\output\query_results.csv")),format="xml")
        else:
            print(f"Warning: Doesn't found query{query_id} for model {model_id}.")
            return pd.DataFrame()
        
    def _get_color_linestyle_of_model(self, model_numb):
        color = "r"
        linestyle = "-"
        match model_numb:
            case 1:
                color = "r"
                linestyle = "-"
            case 2:
                color = "g"
                linestyle = "-"
            case 3:
                color = "b"
                linestyle = "-"
            case 4:
                color = "y"
                linestyle = "-"
            case 5:
                color = "m"
                linestyle = "-"
            case 6:
                color = "c"
                linestyle = "-"
            case 7:
                color = "k"
                linestyle = "-"
            case 8:
                color = "r"
                linestyle = ":"
            case 9:
                color = "g"
                linestyle = ":"
        return color, linestyle
    

    def _get_mean_of_medians(self, query_numb, model_numb, fuseki):
        meanlist = []
        for _ in range(MEAN_LOOPS):
            medianlist = []
            for _ in range(MEDIAN_LOOPS):
                start_time = time()
                _ = self.run_query_of_model(query_numb,model_numb,fuseki)
                time_difference = time() - start_time
                medianlist.append(time_difference)
            meanlist.append(median(medianlist))

        return mean(meanlist)
    
    def benchmark_current_rdfdata(self, querylist : list[int] = [1,2,3,4,5,6], modellist : list[int] = [1,2,3,4,5,6,7,8,9], fuseki : bool = True):
        results = [[] for _ in querylist]
        if fuseki: self.fserver.start_server()

        for model_numb in modellist:
            self._generate_graph_with_model(model_numb, fuseki)
            for index, query_numb in enumerate(querylist):
                print(f"Run query {query_numb} of model {model_numb}.")
                results[index].append(self._get_mean_of_medians(query_numb, model_numb, fuseki))

        if fuski: bench.fserver.stop_server()

        return results
    

    def benchmark_increasing_params(self, increasing_alternatives : bool = False, querylist : list[int] = [1,2,3,4,5,6], modellist : list[int] = [1,2,3,4,5,6,7,8,9], start : int = 0, stop : int = 100, step : int = 5, fuseki : bool = True):
        results = []
        X = range(start, stop, step)

        for count in X:
            if increasing_alternatives: un_generator = UncertaintyGenerator(self.graph_generator.rdfdata).add_pseudorand_alternatives([2,3,4,5,6,9,10,11,12,18,19,20,21],min_uncertainties_per_column=count,max_uncertainties_per_column=count)
            else: un_generator = UncertaintyGenerator(self.graph_generator.rdfdata).add_pseudorand_uncertainty_flags([2,3,4,5,6,9,10,11,12,18,19,20,21],min_uncertainties_per_column=count,max_uncertainties_per_column=count)

            del un_generator
            results.append(self.benchmark_current_rdfdata(querylist,modellist,fuseki))
        
        output = [[[] for _ in modellist] for _ in querylist]
        for res in results:
            for query_numb, query_res in enumerate(res):
                for model_numb, model_res in enumerate(query_res):
                    output[query_numb][model_numb].append(model_res)

        print(list(X))
        print(output, results)

        self._plot_results_increasing_alternatives(X, output, querylist, modellist, increasing_alternatives)

        return output

    def start_benchmark_increasing_alternatives_uncertainties(self, uncertainties : bool, querylist : list[int] = [1,2,3,4,5,6], modellist : list[int] = [1,2,3,4,5,6,7,8,9], start : int = 0, stop : int = 100, step : int = 5, fuseki : bool = True):
        results = [[[] for _ in modellist] for _ in querylist]
        X = range(start, stop, step)
        # if 0 < numb_steps <= len(X): X = X[:numb_steps]

        if fuseki: self.fserver.start_server()

        for i in tqdm(X):
            for model_index, model_numb in enumerate(modellist):
                self.graph_generator = GraphGenerator(self.rdfdata)
                un_generator = UncertaintyGenerator(self.graph_generator.rdfdata)
                if uncertainties == False: self.graph_generator.rdfdata = un_generator.add_pseudorand_alternatives(list_of_columns=[2,3,4,5,6,9,10,11,12,18,19,20,21], min_number_of_alternatives=i, max_number_of_alternatives=i) if i > 0 else self.rdfdata
                else: self.graph_generator.rdfdata = un_generator.add_pseudorand_uncertainty_flags([2,3,4,5,6,9,10,11,12,18,19,20,21],min_uncertainties_per_column=i,max_uncertainties_per_column=i) if i != 0 else self.rdfdata
                self._generate_graph_with_model(model_numb, fuseki)

                for query_index, query_numb in enumerate(querylist):
                    if uncertainties == False: print(f"Run query {query_numb} of model {model_numb} with {i} alternatives per uncertainty and {len(un_generator.rdfdata.uncertainties)} uncertainties.")
                    else: print(f"\nRun query {query_numb} of model {model_numb} with {len(self.graph_generator.rdfdata.uncertainties)} uncertainties. Graph size: {len(self.graph_generator.graph)}")
                    results[query_index][model_index].append(self._get_mean_of_medians(query_numb, model_numb, fuseki))

        if fuski: bench.fserver.stop_server()

        self._plot_results_increasing_alternatives(X, results, querylist, modellist, uncertainties)

        return results
    

    def _plot_results_increasing_alternatives(self, X : range, results : list[list[list[float]]], querylist : list[int], modellist : list[int], uncertainties : bool):
        for index, query_numb in enumerate(querylist):
            for modelindex, model_numb in enumerate(modellist):
                color, linestyle = self._get_color_linestyle_of_model(model_numb)
                plt.plot(X, results[index][modelindex], color=color, linestyle=linestyle, label=str(model_numb))

            if uncertainties == False: plt.xlabel("#Alternatives per uncertain statement")
            else: plt.xlabel("#Uncertainties per column")

            plt.ylabel("Time in seconds")
            if uncertainties == False: plt.title(f"Query {query_numb} with increasing numb alternatives")
            else: plt.title(f"Query {query_numb} with increasing numb uncertainties")

            plt.legend()

            if uncertainties == False: plt.savefig(Path(UNCO_PATH,f"src/benchmark/results/alternatives{query_numb}.pdf"), format="pdf", bbox_inches="tight")
            else: plt.savefig(Path(UNCO_PATH,f"src/benchmark/results/uncertainties{query_numb}.pdf"), format="pdf", bbox_inches="tight")

            plt.show()

    
    def pretty_print_results(self, resultlist : list[list[float]], querylist : list[int] = [1,2,3,4,5,6], modellist : list[int] = [1,2,3,4,5,6,7,8,9]):
        print(f"         |", end="")
        for model in modellist:
            print(f"model {model}|", end="")
        
        print("\n",end="")

        for index, query in enumerate(querylist):
            print(f"query {query}: | ", end="")
            for res in resultlist[index]:
                print("%.3f" % res + " | ", end="")
            print("\n",end="")
    

if __name__ == "__main__":
    # Load data--------------------------------------------------------------------------------------------------------------------------
    rdfdata = RDFData(pd.read_csv(Path(UNCO_PATH,"tests/testdata/afe/afe_noUn_ready.csv")))
    bench = Benchmark(rdfdata,str(Path(UNCO_PATH,"tests/testdata/afe/namespaces.csv")))
    fuski = True

    # Test query of model----------------------------------------------------------------------------------------------------------------
    # model = 8
    # query = 5
    # ugen = UncertaintyGenerator(deepcopy(rdfdata))
    # rdf_data = ugen.add_pseudorand_uncertainty_flags([2,3,4,5,6,9,10,11,12,18,19,20,21],min_uncertainties_per_column=10,max_uncertainties_per_column=10)
    # # rdf_data = ugen.add_pseudorand_uncertainty_flags([19],min_uncertainties_per_column=10,max_uncertainties_per_column=10)
    # bench._generate_graph_with_model(rdf_data,model,query)
    # if fuski:
    #     bench.fserver.start_server()
    #     bench.fserver.upload_data(str(Path(UNCO_PATH,"data/output/graph.ttl")))
    # start = time()
    # print(bench.run_query_of_model(query,model,fuski))

    # time_diff = time() - start
    # if fuski: bench.fserver.stop_server()
    # print(f"Zeit: {time_diff}")



    # Run afe benchmark -------------------------------------------------------------------------------------------------------
    # results : list[list[pd.DataFrame]] = bench.start_boxplot_benchmark(fuseki=fuski)
    # print(results)
    # bench.pretty_print_results(results)
    

    # Run benchmark numb of uncertainties------------------------------------------------------------------------------------------------
    # print(bench.start_benchmark_increasing_uncertainties(fuseki=fuski, querylist=[1,6], modellist=[3,9], stepsize=int(len(bench.rdfdata.data)/2)))

    # Run benchmark numb of alternatives-------------------------------------------------------------------------------------------------
    print(bench.benchmark_increasing_params(fuseki=fuski, modellist=[2], querylist=[2], start=1, step=5, stop=10))