# Importing libraries
import matplotlib.pyplot as plt
import numpy as np
from statistics import median, mean
from unco import UNCO_PATH
from pathlib import Path

def _get_color_linestyle_of_model(model_numb):
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


def _plot_results_increasing_alternatives(X : range, results : list[list[list[float]]], querylist : list[int], modellist : list[int], increasing_alternatives : bool):
    output = [[[] for _ in modellist] for _ in querylist]
    for res in results:
        for query_numb, query_res in enumerate(res):
            for model_numb, model_res in enumerate(query_res):
                output[query_numb][model_numb].append(model_res)

    print(output)
    
    for index, query_numb in enumerate(querylist):
        fig = plt.figure()
        for modelindex, model_numb in enumerate(modellist):
            color, linestyle = _get_color_linestyle_of_model(model_numb)
            if model_numb == 9: model_numb = "9a"
            model_numb = "9b" if model_numb == 10 else str(model_numb)
            plt.plot(X, output[index][modelindex], color=color, linestyle=linestyle, label=str(model_numb))

        if increasing_alternatives: plt.xlabel("#Alternatives per uncertain statement")
        else: plt.xlabel("#Uncertainties per column")

        plt.ylabel("Time in seconds")
        if increasing_alternatives: plt.title(f"Query {query_numb} with increasing numb alternatives")
        else: plt.title(f"Query {query_numb} with increasing numb uncertainties")

        plt.legend()

        plt.ylim([0.275, 0.345])

        if increasing_alternatives: plt.savefig(Path(UNCO_PATH,f"src/benchmark/results/alternatives{query_numb}.pdf"), format="pdf", bbox_inches="tight")
        else: plt.savefig(Path(UNCO_PATH,f"src/benchmark/results/uncertainties{query_numb}.pdf"), format="pdf", bbox_inches="tight")

        plt.close(fig)
            # plt.show()
# Using Numpy to create an array X

  
# raw
res = [[[0.3024468421936035, 0.3058197498321533, 0.2983407974243164, 0.2959461212158203, 0.30339860916137695]], [[0.30780458450317383, 0.29729676246643066, 0.2864241600036621, 0.2939164638519287, 0.28676533699035645]], [[0.2875950336456299, 0.27978515625, 0.31277966499328613, 0.2993745803833008, 0.2902514934539795]], [[0.2828695774078369, 0.2927517890930176, 0.30527186393737793, 0.30955934524536133, 0.3211488723754883]], [[0.29859352111816406, 0.3061981201171875, 0.29262852668762207, 0.30455923080444336, 0.314939022064209]], [[0.2896077632904053, 0.2975587844848633, 0.3111274242401123, 0.31333327293395996, 0.30880260467529297]], [[0.3023543357849121, 0.300731897354126, 0.29773497581481934, 0.2962164878845215, 0.31465959548950195]], [[0.2914106845855713, 0.30298447608947754, 0.2993009090423584, 0.3402993679046631, 0.31679630279541016]], [[0.29311275482177734, 0.2964742183685303, 0.30347347259521484, 0.3030707836151123, 0.3175034523010254]], [[0.2934846878051758, 0.2985258102416992, 0.3026702404022217, 0.3075077533721924, 0.29090380668640137]], [[0.30495166778564453, 0.3066704273223877, 0.3052840232849121, 0.29404139518737793, 0.30280375480651855]]]


# median = 5
res = [[[0.29636168479919434, 0.2897617816925049, 0.28014183044433594, 0.2897520065307617, 0.2961111068725586]], [[0.29355907440185547, 0.28906798362731934, 0.29695582389831543, 0.2818918228149414, 0.29229140281677246]], [[0.285813570022583, 0.3025074005126953, 0.2935147285461426, 0.2932004928588867, 0.3064994812011719]], [[0.2976827621459961, 0.29065370559692383, 0.3011651039123535, 0.3026092052459717, 0.2998518943786621]], [[0.2984023094177246, 0.2933347225189209, 0.3057522773742676, 0.29184699058532715, 0.2958400249481201]], [[0.29602622985839844, 0.3001694679260254, 0.2952561378479004, 0.2848789691925049, 0.29725050926208496]], [[0.28856348991394043, 0.29941630363464355, 0.2885887622833252, 0.30037760734558105, 0.29854679107666016]], [[0.2908923625946045, 0.30759167671203613, 0.2930283546447754, 0.293520450592041, 0.29308581352233887]], [[0.2976961135864258, 0.3001866340637207, 0.29857707023620605, 0.2934887409210205, 0.29244089126586914]], [[0.29976844787597656, 0.3026876449584961, 0.29271578788757324, 0.2918055057525635, 0.31423473358154297]], [[0.30762767791748047, 0.303739070892334, 0.29829931259155273, 0.302797794342041, 0.31133055686950684]]]

newres = [([mean(l)] for l in sublist) for sublist in res]

print(_plot_results_increasing_alternatives(range(0,301,30),res,querylist=[4],modellist=[1,1,1,1,1],increasing_alternatives=False))

#print(_plot_results_increasing_alternatives(range(0,10001,1000),res3,querylist=[1,2,3,4,5,6],modellist=[1,2,3,4,5,6,7,8,9,10],increasing_alternatives=False))


# X = range(len(res[0][0]))[:10]

# results = res[0]

# plt.plot(X, results[0][:10], color='r', label='1')
# plt.plot(X, results[1][:10], color='b', label='2')
# plt.plot(X, results[2][:10], color='g', label='3')
# plt.plot(X, results[3][:10], color='y', label='4')
# plt.plot(X, results[4][:10], color='m', label='5')
# plt.plot(X, results[5][:10], color='c', label='6')
# plt.plot(X, results[6][:10], color='k', label='7')
# plt.plot(X, results[7][:10], color='y', label='8')

# plt.xlabel("#Uncertainties per column")
# plt.ylabel("Time")
# plt.title(f"Query {4} with increasing numb uncertainties")

# plt.legend()
# plt.show()

# print([l[:10] for l in results])
