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

NUMB_LOOPS = 1

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
        
    
    def start_boxplot_benchmark(self, querylist : list[int] = [1,2,3,4,5,6], modellist : list[int] = [1,2,3,4,5,6,7,8,9], fuseki : bool = True):
        results = [[] for _ in querylist]
        if fuseki: self.fserver.start_server()

        for model_numb in modellist:
            self.graph_generator = GraphGenerator(self.rdfdata)
            self._generate_graph_with_model(model_numb, fuseki)
            for index, query_numb in enumerate(querylist):
                print(f"Run query {query_numb} of model {model_numb}.")

                looplist = []
                for _ in range(NUMB_LOOPS):
                    start_time = time()
                    res = self.run_query_of_model(query_numb,model_numb,fuseki)
                    time_difference = time() - start_time
                    looplist.append(len(res))
                results[index].append(looplist[0])
        
        if fuski: bench.fserver.stop_server()

        return results
    
    def plot_box_plot(self, list_of_lists : list):
        plt.style.use('_mpl-gallery')

        _, ax = plt.subplots()
        ax.boxplot(list_of_lists)

        ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
            ylim=(0, 8), yticks=np.arange(1, 8))

        plt.show()


    def start_benchmark_increasing_uncertainties(self, querylist : list[int] = [1,2,3,4,5,6], modellist : list[int] = [1,2,3,4,5,6,7,8,9], stepsize : int = 100, fuseki : bool = True):
        query_results = []
        if fuseki: self.fserver.start_server()
        for query_numb in querylist:
            X = range(0, len(self.rdfdata.data), stepsize)[:]
            results = []
            for model_numb in modellist:
                model_results = []
                time_difference = 0
                for i in tqdm(X):
                    if time_difference < 20:
                        ugen = UncertaintyGenerator(deepcopy(self.rdfdata))
                        rdf_data = ugen.add_pseudorand_uncertainty_flags([2,3,4,5,6,9,10,11,12,18,19,20,21],min_uncertainties_per_column=i,max_uncertainties_per_column=i) if i != 0 else rdfdata
                        self._generate_graph_with_model(model_numb, fuseki)
                        loop = []
                        print(f"\nRun query {query_numb} of model {model_numb} with {len(rdf_data.uncertainties)} uncertainties. Graph size: {len(self.graph_generator.graph)}")
                    for _ in range(NUMB_LOOPS):
                        if time_difference > 20:
                            loop.append(time_difference)
                            continue
                        start_time = time()
                        output = self.run_query_of_model(query_numb, model_numb, fuseki)
                        time_difference = time() - start_time
                        loop.append(time_difference)
                    print(f"Result length: {len(output)}. Current runtime: {'%.2f' % median(loop)}s.")
                    model_results.append(median(loop))
                results.append(model_results)
            query_results.append(results)

        for index, query in enumerate(querylist):
            for modelindex, model in enumerate(modellist):
                color = "r"
                linestyle = "-"
                match model:
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

                plt.plot(X, query_results[index][modelindex], color=color, linestyle=linestyle, label=str(model))

            plt.xlabel("#Uncertainties per column")
            plt.ylabel("Time in seconds")
            plt.title(f"Query {query} with increasing numb uncertainties")

            plt.legend()

            plt.show()
        if fuski: bench.fserver.stop_server()
        
        return query_results
    

    def start_benchmark_increasing_alternatives(self, querylist : list[int] = [1,2,3,4,5,6], modellist : list[int] = [1,2,3,4,5,6,7,8,9], stepsize : int = 100, fuseki : bool = True):
        query_results = []
        if fuseki: self.fserver.start_server()
        for query_numb in querylist:
            X = range(0, len(self.rdfdata.data), stepsize)[:20]
            results = []
            for model_numb in modellist:
                model_results = []
                time_difference = 0
                for i in tqdm(X):
                    if time_difference < 20:
                        ugen = UncertaintyGenerator(deepcopy(self.rdfdata))
                        rdf_data = ugen.add_pseudorand_alternatives(list_of_columns=[2,3,4,5,6,9,10,11,12,18,19,20,21], min_number_of_alternatives=i, max_number_of_alternatives=i) if i != 0 else rdfdata
                        self._generate_graph_with_model(model_numb, fuseki)
                        loop = []
                        print(f"\nRun query {query_numb} of model {model_numb} with {i} alternatives per uncertainty and {len(ugen.rdfdata.uncertainties)} uncertainties.")
                    for _ in range(NUMB_LOOPS):
                        if time_difference > 20:
                            loop.append(time_difference)
                            continue
                        start_time = time()
                        output = self.run_query_of_model(query_numb, model_numb, fuseki)
                        time_difference = time() - start_time
                        loop.append(time_difference)
                    print(f"Result length: {len(output)}. Current runtime: {'%.2f' % median(loop)}s.")
                    model_results.append(median(loop))
                results.append(model_results)
            query_results.append(results)

        for index, query in enumerate(querylist):
            for modelindex, model in enumerate(modellist):
                color = "r"
                linestyle = "-"
                match model:
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

                plt.plot(X, query_results[index][modelindex], color=color, linestyle=linestyle, label=str(model))

            plt.xlabel("#Alternatives per uncertain statement")
            plt.ylabel("Time in seconds")
            plt.title(f"Query {query} with increasing numb alternatives")

            plt.legend()

            plt.show()
        if fuski: bench.fserver.stop_server()

        return query_results
    

if __name__ == "__main__":
    # Load data--------------------------------------------------------------------------------------------------------------------------
    input = open(Path(UNCO_PATH,"tests/testdata/afe/afe_ready.csv"), encoding='utf-8')
    rdfdata = RDFData(pd.read_csv(input))
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
    results : list[list[pd.DataFrame]] = bench.start_boxplot_benchmark(fuseki=fuski)
    print(results)
    # print(len(results[0][0]),len(results[0][1]))
    # difference = pd.concat([results[0][0], results[0][1]]).drop_duplicates(keep=False)
    # difference = difference.applymap(lambda x: "" if str(x)[:3] == "_:b" else x).drop_duplicates(keep=False)
    # difference.to_csv(Path(UNCO_PATH,"data/output/query_results_fuseki.csv"))
    # print(difference)
    # bench.plot_box_plot(results)
    

    # Run benchmark numb of uncertainties------------------------------------------------------------------------------------------------
    # print(bench.start_benchmark_increasing_uncertainties(fuseki=fuski, querylist=[1,6], modellist=[3,9], stepsize=int(len(bench.rdfdata.data)/2)))

    # Run benchmark numb of alternatives-------------------------------------------------------------------------------------------------
    # print(bench.start_benchmark_increasing_alternatives(fuseki=fuski, stepsize=3))