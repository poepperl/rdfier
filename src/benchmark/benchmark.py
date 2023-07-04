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

MEDIAN_LOOPS = 5
MEAN_LOOPS = 11

class Benchmark:
    """
        Class that starts the benchmark methods of unco.

    Attributes
    ----------
    prefixes_path : str
        Path to the prefix-namespace table.
    graph_generator : GraphGenerator
        Instance of the GraphGenerator which contains the inputed RDFData.
    fserver : FusekiServer
        Object which can interact with the fuseki server.
    """


    def __init__(self, rdfdata : RDFData, prefixes_path : str = None) -> None:
        """
        Parameters
        ----------
        rdfdata : RDFData
            Object which contains the data of the rdf graph.
        prefixes_path : str
            Path to the prefix-namespace table.
        """
        self.prefixes_path = prefixes_path
        self.graph_generator = GraphGenerator(rdfdata)
        self.fserver = FusekiServer(Path(UNCO_PATH,"src/apache-jena-fuseki-4.8.0"))


    def _generate_graph_with_model(self, model_id : int, fuseki : bool) -> None:
        """
        Generates the rdf graph of the current dataset with the given model_id.

        Parameters
        ----------
        model_id : int
            ID of the model which should be used to insert uncertaint statements
        fuseki : bool
            Boolean value if the graph should be uploaded to the fuseki server
        """
        if self.prefixes_path: self.graph_generator.load_prefixes(self.prefixes_path)
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
            case 10:
                color = "b"
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
    
    def benchmark_current_rdfdata(self, querylist : list[int] = [1,2,3,4,5,6], modellist : list[int] = [1,2,3,4,5,6,7,8,9,10], fuseki : bool = True):
        results = [[] for _ in querylist]

        for model_numb in modellist:
            if fuseki: self.fserver.start_server()
            self._generate_graph_with_model(model_numb, fuseki)
            for index, query_numb in enumerate(querylist):
                altlist = [len(str(self.graph_generator.rdfdata.data.iat[key[0],key[1]]).split(';')) for key in self.graph_generator.rdfdata.uncertainties]
                print(f"Run query {query_numb} of model {model_numb}. #uncertainties = {len(self.graph_generator.rdfdata.uncertainties)}. #alternatives = {median(altlist) if len(altlist)>0 else 0}")
                results[index].append(self._get_mean_of_medians(query_numb, model_numb, fuseki))

            if fuski: bench.fserver.stop_server()

        return results
    

    def benchmark_increasing_params(self, increasing_alternatives : bool = False, querylist : list[int] = [1,2,3,4,5,6], modellist : list[int] = [1,2,3,4,5,6,7,8,9,10], start : int = 0, stop : int = 100, step : int = 5, fuseki : bool = True):
        results = []
        X = range(start, stop, step)

        for count in X:
            if increasing_alternatives: un_generator = UncertaintyGenerator(self.graph_generator.rdfdata).add_pseudorand_alternatives(list_of_columns=[3,4,7,15], min_number_of_alternatives=count, max_number_of_alternatives=count) if count > 0 else self.graph_generator.rdfdata
            else: un_generator = UncertaintyGenerator(self.graph_generator.rdfdata).add_pseudorand_uncertainty_flags([2,3,4,7,8,9,10,16,17,18,19],min_uncertainties_per_column=count,max_uncertainties_per_column=count) if count > 0 else self.graph_generator.rdfdata

            del un_generator
            results.append(self.benchmark_current_rdfdata(querylist,modellist,fuseki))


        if len(X) > 2: self._plot_results_increasing_alternatives(X, results, querylist, modellist, increasing_alternatives)

        return results
    

    def _plot_results_increasing_alternatives(self, X : range, results : list[list[list[float]]], querylist : list[int], modellist : list[int], increasing_alternatives : bool):
        output = [[[] for _ in modellist] for _ in querylist]
        for res in results:
            for query_numb, query_res in enumerate(res):
                for model_numb, model_res in enumerate(query_res):
                    output[query_numb][model_numb].append(model_res)
        
        for index, query_numb in enumerate(querylist):
            fig = plt.figure()
            for modelindex, model_numb in enumerate(modellist):
                color, linestyle = self._get_color_linestyle_of_model(model_numb)
                plt.plot(X, output[index][modelindex], color=color, linestyle=linestyle, label=str(model_numb))

            if increasing_alternatives: plt.xlabel("#Alternatives per uncertain statement")
            else: plt.xlabel("#Uncertainties per column")

            plt.ylabel("Time in seconds")
            if increasing_alternatives: plt.title(f"Query {query_numb} with increasing numb alternatives")
            else: plt.title(f"Query {query_numb} with increasing numb uncertainties")

            plt.legend()

            if increasing_alternatives: plt.savefig(Path(UNCO_PATH,f"src/benchmark/results/alternatives{query_numb}.pdf"), format="pdf", bbox_inches="tight")
            else: plt.savefig(Path(UNCO_PATH,f"src/benchmark/results/uncertainties{query_numb}.pdf"), format="pdf", bbox_inches="tight")

            plt.close(fig)
            # plt.show()

    
    def pretty_print_results(self, resultlist : list[list[float]], querylist : list[int] = [1,2,3,4,5,6], modellist : list[int] = [1,2,3,4,5,6,7,8,9,10]):
        print(f"         |", end="")
        for model in modellist:
            print(f"model {model}|", end="") if model < 10 else print(f"model{model}|", end="")
        
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
    # model = 10
    # query = 6
    # bench.graph_generator.rdfdata = UncertaintyGenerator(bench.graph_generator.rdfdata).add_pseudorand_uncertainty_flags([2,3,4],min_uncertainties_per_column=2,max_uncertainties_per_column=2)
    # # rdf_data = ugen.add_pseudorand_uncertainty_flags([19],min_uncertainties_per_column=10,max_uncertainties_per_column=10)
    # if fuski:
    #     bench.fserver.start_server()

    # bench._generate_graph_with_model(model,fuski)
    # start = time()
    # print(bench.run_query_of_model(query,model,fuski))

    # time_diff = time() - start
    # if fuski: bench.fserver.stop_server()
    # print(f"Zeit: {time_diff}")



    # Run afe benchmark -------------------------------------------------------------------------------------------------------
    # results : list[list[pd.DataFrame]] = bench.benchmark_increasing_params(increasing_alternatives=True, fuseki=fuski, start=0, step=1, stop=1)
    # print(results)
    # bench.pretty_print_results(results[0])
    

    # Run benchmark numb of uncertainties------------------------------------------------------------------------------------------------
    print(bench.benchmark_increasing_params(increasing_alternatives=False, fuseki=fuski, start=0, step=20, stop=301))

    # Run benchmark numb of alternatives-------------------------------------------------------------------------------------------------
    # bench.graph_generator.rdfdata = UncertaintyGenerator(rdfdata).add_pseudorand_uncertainty_flags([1,2,3,4,5,7],min_uncertainties_per_column=1000,max_uncertainties_per_column=1000)
    # print(bench.benchmark_increasing_params(increasing_alternatives=True, fuseki=fuski, start=0, step=20, stop=81))

    # print(bench.graph_generator.rdfdata.data.columns[1]) # 2,3,4,7,8,9,10,16,17,18,19