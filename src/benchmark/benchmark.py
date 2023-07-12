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
        percentage_range = 0.05

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

                if mini > current_value + percentage_range:
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
    querylist = [1, 2, 3, 4, 5, 6]
    modellist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    x_range = range(0,101,10)

    results =  [[[0.06270170211791992, 0.05691227912902832, 0.06817564964294434, 0.06359953880310058, 0.06450319290161133, 0.061232566833496094, 0.05459847450256348, 0.04919285774230957, 0.05479879379272461, 0.04318046569824219], [0.02053356170654297, 0.019748783111572264, 0.020824623107910157, 0.026570510864257813, 0.033199644088745116, 0.020309972763061523, 0.019113779067993164, 0.01808953285217285, 0.015134334564208984, 0.015201425552368164], [0.05641021728515625, 0.06385979652404786, 0.0525702953338623, 0.061449623107910155, 0.060627412796020505, 0.06033854484558106, 0.05520443916320801, 0.055945539474487306, 0.05040454864501953, 0.05426173210144043], [0.29136996269226073, 0.2853096961975098, 0.31322517395019533, 0.2950986385345459, 0.3075510025024414, 0.29201083183288573, 0.2803955554962158, 0.29560580253601076, 0.2749161243438721, 0.2789217472076416], [0.01531391143798828, 0.01544809341430664, 0.017156410217285156, 0.017078399658203125, 0.020797300338745116, 0.016220808029174805, 0.014556026458740235, 0.012736749649047852, 0.009814929962158204, 0.01296701431274414], [0.0, 0.0, 0.37367968559265136, 0.35246667861938474, 0.37898979187011717, 0.0, 0.0, 0.0, 0.0, 0.3328798770904541]], [[0.06994552612304687, 0.07529587745666504, 0.0886767864227295, 0.08444981575012207, 0.06385774612426758, 0.07480897903442382, 0.07016692161560059, 0.048319005966186525, 0.04725289344787598, 0.04359216690063476], [0.03773932456970215, 0.03355569839477539, 0.028810644149780275, 0.04332270622253418, 0.02988858222961426, 0.048157691955566406, 0.04186396598815918, 0.02305326461791992, 0.01869654655456543, 0.019865894317626955], [0.07435116767883301, 0.06564950942993164, 0.07654151916503907, 0.08861041069030762, 0.06798248291015625, 0.07303709983825683, 0.06798777580261231, 0.06111221313476563, 0.0545198917388916, 0.05100040435791016], [0.34748306274414065, 0.30234508514404296, 0.4342813968658447, 0.35105056762695314, 0.41315560340881347, 0.33200297355651853, 0.30229172706604, 0.29718518257141113, 0.28795299530029295, 0.28743982315063477], [0.051798343658447266, 0.03770613670349121, 0.06114182472229004, 0.0525547981262207, 0.07925796508789062, 0.045672273635864256, 0.04364161491394043, 0.028217029571533204, 0.028911066055297852, 0.028015613555908203], [0.0, 0.0, 0.5141748428344727, 0.4025926113128662, 0.5520297050476074, 0.0, 0.0, 0.0, 0.0, 0.36527533531188966]], [[0.08694295883178711, 0.08219599723815918, 0.0993272304534912, 0.09266891479492187, 0.07904195785522461, 0.0848008632659912, 0.08598484992980956, 0.05001411437988281, 0.04968070983886719, 0.04518136978149414], [0.06900219917297364, 0.038468360900878906, 0.04713120460510254, 0.05694723129272461, 0.03292036056518555, 0.07577638626098633, 0.03525795936584473, 0.02704458236694336, 0.023259735107421874, 0.025067615509033202], [0.11722812652587891, 0.08257594108581542, 0.10186877250671386, 0.1266040325164795, 0.07914700508117675, 0.1144254207611084, 0.07880401611328125, 0.05848307609558105, 0.055096435546875, 0.05677361488342285], [0.4021268844604492, 0.32311477661132815, 0.5517960548400879, 0.403863525390625, 0.5220902442932129, 0.3854189395904541, 0.32810406684875487, 0.3063136100769043, 0.2913981914520264, 0.2935651779174805], [0.07863116264343262, 0.06331119537353516, 0.10530438423156738, 0.08459882736206055, 0.1412059783935547, 0.07849240303039551, 0.06832370758056641, 0.04041109085083008, 0.041514015197753905, 0.03946833610534668], [0.0, 0.0, 0.6677544593811036, 0.45408153533935547, 0.7424637317657471, 0.0, 0.0, 0.0, 0.0, 0.3926541328430176]], [[0.09516725540161133, 0.08097481727600098, 0.1318593978881836, 0.1019477367401123, 0.08725438117980958, 0.09007635116577148, 0.08863205909729004, 0.056437444686889646, 0.044529056549072264, 0.05230822563171387], [0.12851252555847167, 0.04525842666625977, 0.060208797454833984, 0.08155875205993653, 0.0394629955291748, 0.12444624900817872, 0.04858331680297852, 0.030222034454345702, 0.02748870849609375, 0.029585790634155274], [0.1859353542327881, 0.09738454818725586, 0.12843456268310546, 0.16398930549621582, 0.09357676506042481, 0.1770728588104248, 0.09734253883361817, 0.06701726913452148, 0.06536235809326171, 0.06343321800231934], [0.4477811813354492, 0.34080018997192385, 0.6559427738189697, 0.45470943450927737, 0.6224158763885498, 0.431348180770874, 0.3404392242431641, 0.3053009510040283, 0.2971173286437988, 0.3015629291534424], [0.1090250015258789, 0.08440346717834472, 0.14644951820373536, 0.11938686370849609, 0.2100149631500244, 0.10159239768981934, 0.08537774085998535, 0.051767730712890626, 0.052731657028198244, 0.05418481826782227], [0.0, 0.0, 0.8066299438476563, 0.5058370113372803, 0.9474135398864746, 0.0, 0.0, 0.0, 0.0, 0.421160364151001]], [[0.11812767982482911, 0.08448481559753418, 0.11819162368774414, 0.12414593696594238, 0.10541214942932128, 0.09656643867492676, 0.0962334156036377, 0.04971070289611816, 0.04737730026245117, 0.043468809127807616], [0.20247554779052734, 0.051922178268432616, 0.07105712890625, 0.09244813919067382, 0.0462648868560791, 0.1936439037322998, 0.0548515796661377, 0.030860233306884765, 0.03224339485168457, 0.03627896308898926], [0.26014037132263185, 0.11099181175231934, 0.15230059623718262, 0.18853259086608887, 0.10388426780700684, 0.24670696258544922, 0.11360507011413574, 0.07017250061035156, 0.06430864334106445, 0.06605448722839355], [0.4789896488189697, 0.35166258811950685, 0.7328461647033692, 0.4839143753051758, 0.6953327655792236, 0.4456156253814697, 0.3574251174926758, 0.3114920616149902, 0.3016945838928223, 0.3001981735229492], [0.12645816802978516, 0.10511183738708496, 0.17036685943603516, 0.13842945098876952, 0.24928712844848633, 0.11850366592407227, 0.0993344783782959, 0.061474180221557616, 0.06255383491516113, 0.06332187652587891], [0.0, 0.0, 0.8994784832000733, 0.5354189395904541, 1.0819977283477784, 0.0, 0.0, 0.0, 0.0, 0.42611188888549806]],[[0.1209108829498291, 0.09948859214782715, 0.12171015739440919, 0.12946367263793945, 0.09976177215576172, 0.11379103660583496, 0.08269281387329101, 0.046356725692749026, 0.04652724266052246, 0.04960808753967285], [0.2781414031982422, 0.05526599884033203, 0.07780427932739258, 0.10330381393432617, 0.04396886825561523, 0.26040945053100584, 0.056447410583496095, 0.033635187149047854, 0.034366703033447264, 0.03962597846984863], [0.3382169246673584, 0.11505270004272461, 0.17364392280578614, 0.2010650157928467, 0.10999932289123535, 0.3206783294677734, 0.11880393028259277, 0.07337079048156739, 0.06810541152954101, 0.06785588264465332], [0.4891160488128662, 0.3624875545501709, 0.7743882179260254, 0.502201509475708, 0.7302164077758789, 0.4627906322479248, 0.3619384765625, 0.3144434928894043, 0.3004148483276367, 0.30259137153625487], [0.13620758056640625, 0.10628552436828613, 0.18758387565612794, 0.1478198528289795, 0.26893153190612795, 0.12692465782165527, 0.10639142990112305, 0.0648202896118164, 0.06621794700622559, 0.06553025245666504], [0.0, 0.0, 0.9515719413757324, 0.5538968563079834, 1.1548775672912597, 0.0, 0.0, 0.0, 0.0, 0.43314261436462403]], [[0.11744933128356934, 0.09035472869873047, 0.12799582481384278, 0.12547402381896972, 0.09289512634277344, 0.10714311599731445, 0.08997864723205566, 0.048425149917602536, 0.045536375045776366, 0.044516563415527344], [0.27864370346069334, 0.05739526748657227, 0.08128314018249512, 0.10708818435668946, 0.046973800659179686, 0.2660097122192383, 0.05807089805603027, 0.03254513740539551, 0.03456525802612305, 0.039609432220458984], [0.332107400894165, 0.12609543800354003, 0.17626385688781737, 0.2059793472290039, 0.11199283599853516, 0.3175309181213379, 0.1211477279663086, 0.07028012275695801, 0.07114176750183106, 0.06574926376342774], [0.49223899841308594, 0.3606904983520508, 0.7832499027252198, 0.5073958396911621, 0.7473167896270752, 0.463502311706543, 0.36044607162475584, 0.3100477695465088, 0.30335540771484376, 0.3008507251739502], [0.13801164627075196, 0.11170763969421386, 0.18572373390197755, 0.15269479751586915, 0.27593188285827636, 0.1287778854370117, 0.11368098258972167, 0.06350407600402833, 0.06949453353881836, 0.07053303718566895], [0.0, 0.0, 0.9516029834747315, 0.5633317947387695, 1.1747754573822022, 0.0, 0.0, 0.0, 0.0, 0.43113088607788086]], [[0.12328095436096191, 0.08195114135742188, 0.13503627777099608, 0.11643648147583008, 0.08933281898498535, 0.10671167373657227, 0.09021582603454589, 0.05138339996337891, 0.04340219497680664, 0.04624729156494141], [0.28378820419311523, 0.0556067943572998, 0.07987747192382813, 0.09786801338195801, 0.04801158905029297, 0.2646922588348389, 0.05809087753295898, 0.03499259948730469, 0.034508562088012694, 0.036737489700317386], [0.3368710517883301, 0.1181257724761963, 0.17307486534118652, 0.2006700038909912, 0.1126053810119629, 0.31870670318603517, 0.11969842910766601, 0.07471418380737305, 0.06888780593872071, 0.06759853363037109], [0.49408783912658694, 0.3585516929626465, 0.7800713062286377, 0.503504753112793, 0.7617876529693604, 0.46067171096801757, 0.36762657165527346, 0.31807432174682615, 0.3040506362915039, 0.3056027412414551], [0.13949503898620605, 0.11296682357788086, 0.18656978607177735, 0.1524686336517334, 0.28011441230773926, 0.12657723426818848, 0.11124310493469239, 0.06643953323364257, 0.06790480613708497, 0.0704279899597168], [0.0, 0.0, 0.9585537433624267, 0.5546057224273682, 1.185865879058838, 0.0, 0.0, 0.0, 0.0, 0.4380989074707031]], [[0.10274305343627929, 0.08893299102783203, 0.1253274440765381, 0.11350226402282715, 0.08923416137695313, 0.10664749145507812, 0.08295578956604004, 0.04698801040649414, 0.04878687858581543, 0.04467649459838867], [0.27355151176452636, 0.056771278381347656, 0.08032307624816895, 0.102374267578125, 0.04820761680603027, 0.26752519607543945, 0.05657296180725098, 0.034652185440063474, 0.0351318359375, 0.03570699691772461], [0.33469357490539553, 0.12070460319519043, 0.1745680809020996, 0.20177221298217773, 0.11356973648071289, 0.32260894775390625, 0.12019886970520019, 0.06842637062072754, 0.07147560119628907, 0.06581974029541016], [0.4967495441436768, 0.36660146713256836, 0.7910932064056396, 0.5110498905181885, 0.7612167358398437, 0.4606935024261475, 0.36288909912109374, 0.31090869903564455, 0.3005084037780762, 0.30964059829711915], [0.14075140953063964, 0.10933036804199218, 0.19204063415527345, 0.15445895195007325, 0.2865120887756348, 0.12753648757934571, 0.11590723991394043, 0.06553707122802735, 0.0699528694152832, 0.0717848300933838], [0.0, 0.0, 0.9681431293487549, 0.5619255542755127, 1.210822296142578, 0.0, 0.0, 0.0, 0.0, 0.4401393413543701]], [[0.11237297058105469, 0.09270071983337402, 0.1307145118713379, 0.11462244987487794, 0.09423460960388183, 0.10181717872619629, 0.07620229721069335, 0.05173897743225098, 0.04437112808227539, 0.04512348175048828], [0.27698116302490233, 0.05754861831665039, 0.08053417205810547, 0.10347824096679688, 0.047257518768310545, 0.2689004898071289, 0.05821857452392578, 0.035333871841430664, 0.03574395179748535, 0.0353546142578125], [0.3341559886932373, 0.11940479278564453, 0.17516088485717773, 0.20773930549621583, 0.11420063972473145, 0.31488981246948244, 0.12277755737304688, 0.076617431640625, 0.06985225677490234, 0.06979336738586425], [0.49816255569458007, 0.36463079452514646, 0.7868345737457275, 0.5164425373077393, 0.7657093048095703, 0.4622819423675537, 0.3583415985107422, 0.3137543201446533, 0.2977473258972168, 0.30479040145874026], [0.14072260856628419, 0.109474515914917, 0.1937272071838379, 0.15527048110961914, 0.2877651691436768, 0.128248929977417, 0.11233687400817871, 0.06589016914367676, 0.06982345581054687, 0.07038187980651855], [0.0, 0.0, 0.969097089767456, 0.5695304870605469, 1.2074855327606202, 0.0, 0.0, 0.0, 0.0, 0.4392543792724609]], [[0.10453824996948242, 0.09739794731140136, 0.12422523498535157, 0.11314983367919922, 0.09165153503417969, 0.11610875129699708, 0.09293675422668457, 0.04944906234741211, 0.044295740127563474, 0.04461030960083008], [0.27614545822143555, 0.057990217208862306, 0.08392109870910644, 0.10902523994445801, 0.047722816467285156, 0.2608382225036621, 0.0567631721496582, 0.035107660293579104, 0.03540935516357422, 0.03829517364501953], [0.33458595275878905, 0.12295136451721192, 0.17358713150024413, 0.21243038177490234, 0.11268954277038574, 0.31675329208374026, 0.1232375144958496, 0.07268671989440918, 0.06751275062561035, 0.06905918121337891], [0.4940345764160156, 0.36315150260925294, 0.7903341293334961, 0.5172687530517578, 0.7479097843170166, 0.4662722110748291, 0.3671274185180664, 0.3151897430419922, 0.30296993255615234, 0.3105643272399902], [0.1401008129119873, 0.11044778823852539, 0.19441461563110352, 0.1581294059753418, 0.28211050033569335, 0.12833142280578613, 0.1117976188659668, 0.06912212371826172, 0.06707043647766113, 0.07147855758666992], [0.0, 0.0, 0.9761860370635986, 0.5729422569274902, 1.191323184967041, 0.0, 0.0, 0.0, 0.0, 0.4416214942932129]]]

    if len(x_range) > 2:
        bench._plot_results_increasing_params(True, x_range, results, querylist, modellist)

    print("End-Results:")
    bench.pretty_print_results(results[-1], querylist, modellist)
    print("End-Ranking:")
    bench.pretty_print_results(bench.get_ranking(results[-1]), querylist, modellist, True)