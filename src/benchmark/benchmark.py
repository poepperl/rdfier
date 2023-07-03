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
MEAN_LOOPS = 3

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
        if fuseki: self.fserver.start_server()

        for model_numb in modellist:
            self._generate_graph_with_model(model_numb, fuseki)
            for index, query_numb in enumerate(querylist):
                uncertain_entry = list(self.graph_generator.rdfdata.uncertainties)[0] if len(self.graph_generator.rdfdata.uncertainties) > 0 else (0,0)
                print(f"Run query {query_numb} of model {model_numb}. #uncertainties = {len(self.graph_generator.rdfdata.uncertainties)}. #alternatives = {len(str(self.graph_generator.rdfdata.data.iat[uncertain_entry[0],uncertain_entry[1]]).split(';'))}")
                results[index].append(self._get_mean_of_medians(query_numb, model_numb, fuseki))

        if fuski: bench.fserver.stop_server()

        return results
    

    def benchmark_increasing_params(self, increasing_alternatives : bool = False, querylist : list[int] = [1,2,3,4,5,6], modellist : list[int] = [1,2,3,4,5,6,7,8,9,10], start : int = 0, stop : int = 100, step : int = 5, fuseki : bool = True):
        results = []
        X = range(start, stop, step)

        for count in X:
            if increasing_alternatives: un_generator = UncertaintyGenerator(self.graph_generator.rdfdata).add_pseudorand_alternatives(list_of_columns=[1,5,6,7,8,9], min_number_of_alternatives=count, max_number_of_alternatives=count) if count > 0 else self.graph_generator.rdfdata
            else: un_generator = UncertaintyGenerator(self.graph_generator.rdfdata).add_pseudorand_uncertainty_flags([2,3,4,5,6,9,10,11,12,18,19,20,21],min_uncertainties_per_column=count,max_uncertainties_per_column=count) if count > 0 else self.graph_generator.rdfdata

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
                print(X, output[index][modelindex])
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
            print(f"model {model}|", end="")
        
        print("\n",end="")

        for index, query in enumerate(querylist):
            print(f"query {query}: | ", end="")
            for res in resultlist[index]:
                print("%.3f" % res + " | ", end="")
            print("\n",end="")
    

if __name__ == "__main__":
    # Load data--------------------------------------------------------------------------------------------------------------------------
    rdfdata = RDFData(pd.read_csv(Path(UNCO_PATH,"tests/testdata/afe/syntatic.csv")))
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
    # print(bench.benchmark_increasing_params(increasing_alternatives=False, fuseki=fuski, start=0, step=20, stop=81))

    # Run benchmark numb of alternatives-------------------------------------------------------------------------------------------------
    # bench.graph_generator.rdfdata = UncertaintyGenerator(rdfdata).add_pseudorand_uncertainty_flags([1,5,6,7,8,9],min_uncertainties_per_column=1000,max_uncertainties_per_column=1000)
    # print(bench.benchmark_increasing_params(increasing_alternatives=True, fuseki=fuski, start=0, step=20, stop=81))

    res = [[[0.08469104766845703, 0.07808399200439453, 0.06835746765136719, 0.10638006528218587, 0.07305765151977539, 0.06998300552368164, 0.07248346010843913, 0.0690602461496989, 0.06766017278035481, 0.06931869188944499], [0.015707890192667644, 0.025973002115885418, 0.012813409169514975, 0.05173643430074056, 0.02250520388285319, 0.014169851938883463, 0.024888992309570312, 0.018030166625976562, 0.014025290807088217, 0.01558979352315267], [0.08903781572977702, 0.09984151522318523, 0.08716344833374023, 0.15055116017659506, 0.09960738817850749, 0.08437339464823405, 0.1028304894765218, 0.09190050760904948, 0.09216721852620442, 0.0792082150777181], [2.0398265520731607, 1.9846903483072917, 2.2785821755727134, 2.1261677742004395, 2.2358859380086265, 2.1606850624084473, 2.070892016092936, 2.1539820035298667, 2.0501851240793862, 2.0601109663645425], [0.07325100898742676, 0.06353457768758138, 0.10187284151713054, 0.09192641576131184, 0.12974794705708823, 0.0715787410736084, 0.06263184547424316, 0.05420811971028646, 0.042243639628092446, 0.04305267333984375], [0.0003399848937988281, 0.0002942085266113281, 2.6181044578552246, 2.453890005747477, 2.7400726477305093, 0.0003294944763183594, 0.00034737586975097656, 0.0003361701965332031, 0.0003291765848795573, 2.3866981665293374]], [[0.086272398630778, 0.27061033248901367, 0.0677031675974528, 0.6356423695882162, 0.2068814436594645, 0.06708033879597981, 0.26374419530232746, 0.07375375429789226, 0.0666051705678304, 0.07328089078267415], [0.015847206115722656, 0.21756871541341147, 0.014880180358886719, 0.594021717707316, 0.02696530024210612, 0.013694206873575846, 0.23552664120992026, 0.01972055435180664, 0.04045518239339193, 0.04542708396911621], [0.09497523307800293, 0.46875866254170734, 0.08943843841552734, 1.1764360268910725, 0.23612618446350098, 0.08190512657165527, 0.46989814440409344, 0.0898436705271403, 0.10357602437337239, 0.11399523417154948], [3.7973580360412598, 2.6048826376597085, 6.643818298975627, 4.0438400109608965, 6.627409140268962, 3.818562110265096, 2.9231244723002114, 2.640501101811727, 2.5400239626566568, 2.5334198474884033], [1.2642194430033367, 0.9427000681559244, 1.7770094871520996, 1.3002405961354573, 2.621354420979818, 1.1818923155466716, 0.967263380686442, 0.5455315907796224, 0.5979066689809164, 0.6030424435933431], [0.0002894401550292969, 0.00033704439798990887, 8.027082920074463, 4.312435547510783, 10.59276008605957, 0.00029913584391276043, 0.0002968311309814453, 0.0003124078114827474, 0.00033466021219889325, 2.90461794535319]], [[0.08183002471923828, 0.43810613950093585, 0.06679129600524902, 1.3617836634318035, 0.32682204246520996, 0.06870222091674805, 0.4914232889811198, 0.08408594131469727, 0.06739687919616699, 0.06634108225504558], [0.015862067540486652, 0.42241954803466797, 0.013955036799112955, 1.254604657491048, 0.025211254755655926, 0.01351769765218099, 0.46441348393758136, 0.023189544677734375, 0.0644685427347819, 0.09757320086161296], [0.0893710454305013, 0.9079437255859375, 0.08294637997945149, 2.398398001988729, 0.3959504763285319, 0.08239436149597168, 0.9176757335662842, 0.11020406087239583, 0.1352698008219401, 0.16382098197937012], [5.721442143122355, 3.3556063969930015, 11.839818080266317, 6.564631223678589, 10.961977561314901, 6.078630208969116, 4.054628690083821, 3.1973339716593423, 3.2096420923868814, 3.10544490814209], [2.5942413012186685, 1.9900075594584148, 3.5484045346577964, 2.601609547932943, 5.18766204516093, 2.3813014030456543, 2.05004874865214, 1.0929293632507324, 1.2118931611378987, 1.270156701405843], [0.0003273487091064453, 0.00028514862060546875, 14.70824408531189, 6.989267269770305, 18.909950574239094, 0.00029404958089192707, 0.0002674261728922526, 0.000284115473429362, 0.00035532315572102863, 3.6152528127034507]], [[0.07742222150166829, 0.6281081835428873, 0.0698987642923991, 1.8216745853424072, 0.5360192457834879, 0.06540799140930176, 0.6882257461547852, 0.0787493387858073, 0.06495300928751628, 0.07145857810974121], [0.016308069229125977, 0.6097137133280436, 0.015260140101114908, 1.8681182861328125, 0.026906172434488933, 0.01163784662882487, 0.6665810743967692, 0.021565357844034832, 0.08746798833211263, 0.12570953369140625], [0.08824539184570312, 1.2174735864003499, 0.08360004425048828, 3.6105907758076987, 0.5312391122182211, 0.08470408121744792, 1.3303381601969402, 0.09703930219014485, 0.16478610038757324, 0.18155996004740396], [7.300369501113892, 3.9444960753122964, 16.643882671991985, 8.772480567296347, 16.10204251607259, 8.056917905807495, 5.175352255503337, 3.876915693283081, 3.672452529271444, 3.7866358757019043], [3.7761877377827964, 2.9040501912434897, 5.577747821807861, 4.06414270401001, 8.0721435546875, 3.7730746269226074, 2.988154331843058, 1.619100570678711, 1.8619270324707031, 1.899234453837077], [0.0003089110056559245, 0.00035111109415690106, 20.78417420387268, 9.195519844690958, 27.845497131347656, 0.0002872149149576823, 0.0002761681874593099, 0.0003281434377034505, 0.0003743171691894531, 4.296311060587565]], [[0.08122984568277995, 0.9200599988301595, 0.06989073753356934, 2.3836638927459717, 0.6997876167297363, 0.0751495361328125, 0.9979053338368734, 0.08327515920003255, 0.07214641571044922, 0.07493472099304199], [0.016901254653930664, 0.922825813293457, 0.014647801717122396, 2.5903595288594565, 0.02804247538248698, 0.009694178899129232, 1.029646873474121, 0.01665814717610677, 0.12771121660868326, 0.15032545725504556], [0.08806435267130534, 1.825541655222575, 0.08768590291341145, 4.987562497456868, 0.714553435643514, 0.09294350941975911, 2.0595409870147705, 0.10618209838867188, 0.20325732231140137, 0.21286233266194662], [9.253055493036905, 5.2905410925547285, 23.085577964782715, 10.700867096583048, 22.309412320454914, 11.153229236602783, 6.689998308817546, 4.582963466644287, 4.306652943293254, 4.3086628913879395], [5.013238112131755, 4.030852238337199, 7.398965120315552, 5.282214959462483, 11.33811362584432, 5.294314463933309, 4.228471517562866, 2.129082520802816, 2.4554412364959717, 2.4985013802846274], [0.0003314812978108724, 0.00027879079182942707, 27.88282648722331, 11.47249166170756, 37.716989040374756, 0.0002516905466715495, 0.000339508056640625, 0.00025391578674316406, 0.0002627372741699219, 4.909851551055908]]]


    bench._plot_results_increasing_alternatives(range(0,81,20), res, [1,2,3,4,5,6], [1,2,3,4,5,6,7,8,9,10], True)