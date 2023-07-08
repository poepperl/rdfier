import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from statistics import median, mean
from unco import UNCO_PATH
from unco.data.data_util import data_optimize
from unco.data.rdf_data import RDFData
from unco.data.uncertainty_generator import UncertaintyGenerator
from unco.features.fuseki import FusekiServer
from unco.features.graph_generator import GraphGenerator
from pathlib import Path
from time import time


class Benchmark:
    """
        Class that runs the benchmark methods of unco.

    Attributes
    ----------
    prefixes_path : str
        Path to the prefix-namespace table.
    graph_generator : GraphGenerator
        Instance of the GraphGenerator which contains the inputed RDFData.
    fserver : FusekiServer
        Object which can interact with the fuseki server.
    MEDIAN_LOOPS: int
        Number of runs which should be used to calculate the medians.
    MEAN_LOOPS: int
        Number of medians which should be used to calculate the means.
    run_on_fuseki: bool
        If True, the benchmark uses fuseki to run the queries.
    """

    def __init__(self, rdfdata: RDFData, prefixes_path: str = None) -> None:
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
        self.fserver = FusekiServer(Path(UNCO_PATH, "src/apache-jena-fuseki-4.8.0"))
        self.MEDIAN_LOOPS = 5
        self.MEAN_LOOPS = 5
        self.run_on_fuseki = True

    def _generate_graph_with_model(self, model_id: int) -> None:
        """
        Generates the rdf graph of the current dataset with the given model_id.

        Parameters
        ----------
        model_id : int
            ID of the model which should be used to insert uncertain statements
        """
        if self.prefixes_path:
            self.graph_generator.load_prefixes(self.prefixes_path)
        self.graph_generator.generate_solution(model_id, xml_format=False)

    def run_query_of_model(self, query_id: int, model_id: int) -> float:
        """ 
        Method which takes the SPARQL query "src/benchmark/queries/model{model_id}/query{query_id}.rq" and
        runs the query on self.graph. Outputs the DataFrame of the SPARQL result.

        Attributes
        ----------
        query_id : int
            Query id of the saved query.
        model_id : int
            Model id of the implemented model.
        """
        if (query_path := Path(UNCO_PATH, f"src/benchmark/queries/model{model_id}/query{query_id}.rq")).is_file():
            query = query_path.read_text()
            start_time = time()
            self.graph_generator.run_query(query, save_result=False) if not self.run_on_fuseki else self.fserver.run_query(query,save_result=False)
            return time()-start_time
        return 0.0

    def _get_color_linestyle_of_model(self, model_numb: int) -> tuple[str, str]:
        """
        Returns the plots color and linestyle for each model.

        Parameter
        ---------
        model_numb: int
            ID of the model.
        """
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

    def _get_median(self, query_id: int, model_id: int) -> float:
        """
        Runs the query on the current rdf graph. Returns the median of MEDIAN_LOOPS runs.

        Parameters
        ----------
        query_id: int
            ID of the query.
        model_id: int
            ID of the model which was used to generate the current graph.
        """
        medianlist = []
        for _ in range(self.MEDIAN_LOOPS+3):
            time_difference = self.run_query_of_model(query_id, model_id)
            medianlist.append(time_difference)
        return median(medianlist[3:])

    def _run_benchmark_unit(self, querylist: list[int] = [1, 2, 3, 4, 5, 6], modellist: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]):
        """
        Runs a single benchmark unit on the current RDFData.

        Parameters
        ----------
        querylist: list[int]
            List of the queries that will be tested by the benchmark.
        modellist: list[int]
            List of models that will be tested by the benchmark.
        """
        results = [[[] for _ in modellist] for _ in querylist]

        for _ in tqdm(range(self.MEAN_LOOPS+1)):
            for model_index, model_numb in enumerate(modellist):
                if self.run_on_fuseki:
                    self.fserver.start_server()
                self._generate_graph_with_model(model_numb)
                if self.run_on_fuseki:
                    self.fserver.delete_graph()
                    self.fserver.upload_data(str(Path(UNCO_PATH, "data/output/graph.ttl")))
                for index, query_numb in enumerate(querylist):
                    altlist = [len(str(self.graph_generator.rdfdata.data.iat[key[0], key[1]]).split(';')) for key in self.graph_generator.rdfdata.uncertainties]
                    tqdm.write(f"Run query {query_numb} of model {model_numb}. #uncertain cells = {len(self.graph_generator.rdfdata.uncertainties)}. #uncertain statements = {sum(altlist) if len(altlist) > 0 else 0}")
                    results[index][model_index].append(self._get_median(query_numb, model_numb))

                if self.run_on_fuseki:
                    self.fserver.stop_server()

        return [[mean(models[1:]) for models in sublist] for sublist in results]

    def run_benchmarktest(self, increasing_alternatives: bool = False, querylist: list[int] = [1, 2, 3, 4, 5, 6], modellist: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], x_range: range = range(0, 301, 30)):
        """
        Method which runs a benchmarktest of unco.

        Parameters
        ----------
        increasing_alternatives: bool
            Sets the mode to increasing alternatives or increasing uncertainties.
            If no parameter should increase, you have to set the range to a single value range.
        querylist: list[int]
            List of the queries that will be tested by the benchmark.
        modellist: list[int]
            List of models that will be tested by the benchmark.
        x_range: range
            The range of the parameters should be increased.
        """
        results = []

        for count in tqdm(x_range):
            if increasing_alternatives:
                un_generator = UncertaintyGenerator(self.graph_generator.rdfdata).add_pseudorand_alternatives(list_of_columns=[7, 8, 9, 16, 17, 18, 19], min_number_of_alternatives=count, max_number_of_alternatives=count) if count > 0 else self.graph_generator.rdfdata
            else:
                un_generator = UncertaintyGenerator(self.graph_generator.rdfdata).add_pseudorand_uncertainty_flags([2, 3, 4, 7], min_uncertainties_per_column=count, max_uncertainties_per_column=count) if count > 0 else self.graph_generator.rdfdata

            del un_generator
            results.append(self._run_benchmark_unit(querylist, modellist))
            print("Current results: \nresults = ", results)

        if len(x_range) > 2:
            self._plot_results_increasing_params(increasing_alternatives, x_range, results, querylist, modellist)
        else:
            self.pretty_print_results(results[0], querylist, modellist)

        return results

    def _plot_results_increasing_params(self, increasing_alternatives: bool, x_range: range, results: list[list[list[float]]], querylist: list[int], modellist: list[int]):
        """
        Creates matplotlib plots for increasing parameter benchmarktests and saves them in src/benchmark/results folder.

        Parameters
        ----------
        increasing_alternatives: bool
            Sets the mode to increasing alternatives or increasing uncertainties.
            If no parameter should increase, you have to set the range to a single value range.
        x_range: range
            The range of the parameters should be increased.
        results: list[list[list[float]]]
            Results of the run_benchmarktest method.
        querylist: list[int]
            List of the queries that will be tested by the benchmark.
        modellist: list[int]
            List of models that will be tested by the benchmark.
        """
        output = [[[] for _ in modellist] for _ in querylist]
        for res in results:
            for query_numb, query_res in enumerate(res):
                for model_numb, model_res in enumerate(query_res):
                    output[query_numb][model_numb].append(model_res)

        for index, query_numb in enumerate(querylist):
            fig = plt.figure()
            for modelindex, model_numb in enumerate(modellist):
                color, linestyle = self._get_color_linestyle_of_model(model_numb)
                if model_numb == 9:
                    model_numb = "9a"
                model_numb = "9b" if model_numb == 10 else str(model_numb)
                plt.plot(x_range, output[index][modelindex], color=color, linestyle=linestyle, label=str(model_numb))

            if increasing_alternatives:
                plt.xlabel("#Alternatives per uncertain statement")
            else:
                plt.xlabel("#Uncertainties per column")

            plt.ylabel("Time in seconds")
            if increasing_alternatives:
                plt.title(f"Query {query_numb} with increasing numb alternatives")
            else:
                plt.title(f"Query {query_numb} with increasing numb uncertainties")

            plt.legend()

            if increasing_alternatives:
                plt.savefig(Path(UNCO_PATH, f"src/benchmark/results/alternatives{query_numb}.pdf"), format="pdf", bbox_inches="tight")
            else:
                plt.savefig(Path(UNCO_PATH, f"src/benchmark/results/uncertainties{query_numb}.pdf"), format="pdf", bbox_inches="tight")

            plt.close(fig)

    def pretty_print_results(self, results: list, querylist: list[int] = [1, 2, 3, 4, 5, 6], modellist: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]):
        """
        Creates a prettier print of non-increasing parameter results.

        Parameters
        ----------
        results: list[list[list[float]]]
            Results of the run_benchmarktest method.
        querylist: list[int]
            List of the queries which where tested by the benchmark.
        modellist: list[int]
            List of models which where tested by the benchmark.
        """
        print(f"         |", end="")
        for model in modellist:
            if model == 9:
                model = "9a"
            elif model == 10:
                model = "9b"
            print(f"model {model}|", end="") if len(str(model)) < 2 else print(f"model{model}|", end="")

        print("\n", end="")

        for index, query in enumerate(querylist):
            print(f"query {query}: | ", end="")
            for res in results[index]:
                print("%.3f" % res + " | ", end="")
            print("\n", end="")

