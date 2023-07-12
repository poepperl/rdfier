import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from statistics import median, mean
from unco import UNCO_PATH
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

    def __init__(self, rdfdata: RDFData, prefixes_path: str = None, fuseki_path: str | Path = Path(UNCO_PATH, "src/apache-jena-fuseki-4.8.0")) -> None:
        """
        Parameters
        ----------
        rdfdata : RDFData
            Object which contains the data of the rdf graph.
        prefixes_path : str
            Path to the prefix-namespace table.
        fuseki_path: str | Path
            Path to the fuseki server folder.
        """
        self.prefixes_path = prefixes_path
        self.graph_generator = GraphGenerator(rdfdata)
        self.fserver = FusekiServer(fuseki_path)
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
        self.graph_generator.generate_graph(model_id, xml_format=False)

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
        for _ in range(self.MEDIAN_LOOPS+5):
            time_difference = self.run_query_of_model(query_id, model_id)
            medianlist.append(time_difference)
        return median(medianlist[5:])

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

    def run_benchmarktest(self, increasing_alternatives: bool, increasing_columns: list[int], querylist: list[int] = [1, 2, 3, 4, 5, 6], modellist: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], x_range: range = range(0, 301, 30)):
        """
        Method which runs a benchmarktest of unco.

        Parameters
        ----------
        increasing_alternatives: bool
            Sets the mode to increasing alternatives or increasing uncertainties.
            If no parameter should increase, you have to set the range to a single value range.
        increasing_columns: list[int]
            Columns which should get increasing number of uncertainties/alternatives.
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
                un_generator = UncertaintyGenerator(self.graph_generator.rdfdata).add_pseudorand_alternatives(list_of_columns=increasing_columns, min_number_of_alternatives=count, max_number_of_alternatives=count) if count > 0 else self.graph_generator.rdfdata
            else:
                un_generator = UncertaintyGenerator(self.graph_generator.rdfdata).add_pseudorand_uncertainty_flags(list_of_columns=increasing_columns, min_uncertainties_per_column=count, max_uncertainties_per_column=count) if count > 0 else self.graph_generator.rdfdata

            del un_generator
            results.append(self._run_benchmark_unit(querylist, modellist))
            print("Current results: \nresults = ", results)

        if len(x_range) > 2:
            self._plot_results_increasing_params(increasing_alternatives, x_range, results, querylist, modellist)

        print("End-Results:")
        self.pretty_print_results(results[-1], querylist, modellist)
        print("End-Ranking:")
        self.pretty_print_results(self.get_ranking(results[-1]), querylist, modellist, True)

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

            if increasing_alternatives: plt.savefig(Path(UNCO_PATH, f"data/results/plots/alternatives{query_numb}.pdf"), format="pdf", bbox_inches="tight")
            else: plt.savefig(Path(UNCO_PATH, f"data/results/plots/uncertainties{query_numb}.pdf"), format="pdf", bbox_inches="tight")

            plt.close(fig)
    
    def get_ranking(self, results: list[list[float]]) -> list[list[int]]:
        """
        Returns the ranking of the current results.

        Parameters
        ----------
        results: list[list[float]]
            Results of the run_benchmarktest method.
        """
        results = [[results[q][m] - min([v for v in results[q] if v != 0]) for m in range(len(results[0]))] for q in range(len(results))]
        maxes = [max([float(results[q][m]) for m in range(len(results[0]))]) for q in range(len(results))]
        results = [[((results[q][m]/maxes[q]) - 0.1) if results[q][m] >= 0 else 100 for m in range(len(results[0]))] for q in range(len(results))]  # list of percentage values

        for q in range(len(results)):
            new_query_result = [m for m in results[q]]
            current_value = min(results[q])
            current_rang = 1
            for counter in range(1,len(results[0])+1):

                if (mini := min(results[q])) == 100:
                    new_query_result[new_query_result.index(mini)] = "X"
                    results[q].remove(mini)
                    continue

                if mini > current_value + 0.05:
                    current_rang = counter
                    current_value = mini

                new_query_result[new_query_result.index(mini)] = current_rang
                results[q].remove(mini)

            results[q] = new_query_result


        return results

    def pretty_print_results(self, results: list, querylist: list[int] = [1, 2, 3, 4, 5, 6], modellist: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], ranking: bool = False):
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
        ranking: bool
            If true, the results are printed as ints.
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
                if ranking: print(str(res) + ("     | " if len(str(res))==1 else "    | "), end="")
                else: print("%.3f" % res + " | ", end="")
            print("\n", end="")

if __name__ == "__main__":
    bench = Benchmark(RDFData(pd.read_csv(r"D:\Dokumente\Repositories\unco\data\input\example_input.csv")))

    results = [[[0.0756082325358073, 0.07659681638081868, 0.07915266354878743, 0.08450512091318767, 0.07642125643310547, 0.0747679074605306, 0.06948153177897136, 0.06559403737386067, 0.06549493471781413, 0.06521085898081462], [0.02034131685892741, 0.020469864209493, 0.022633592287699383, 0.02609694004058838, 0.04219937324523926, 0.019278208414713543, 0.019598642985026043, 0.01919511953989665, 0.01576848824818929, 0.01620316505432129], [0.06653865178426106, 0.06448276837666829, 0.06781208515167236, 0.06753977139790852, 0.06718218326568604, 0.06081740061442057, 0.06891135374704997, 0.05992607275644938, 0.05660974979400635, 0.05926187833150228], [0.2998781204223633, 0.28731008370717365, 0.31819355487823486, 0.2952081759770711, 0.30543720722198486, 0.3001762231190999, 0.28645165761311847, 0.29993287722269696, 0.2818714777628581, 0.287714163462321], [0.013060490290323893, 0.015637636184692383, 0.02050459384918213, 0.01956442991892497, 0.021547714869181316, 0.016689777374267578, 0.014809727668762207, 0.015057841936747232, 0.011667331059773764, 0.015020489692687988], [0, 0, 0.380265752474467, 0.3569776217142741, 0.37829287846883136, 0, 0, 0, 0, 0.34629873434702557]]]

    bench.pretty_print_results(bench.get_ranking(results[0]), [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], True)