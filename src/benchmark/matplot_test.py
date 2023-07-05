# Importing libraries
import matplotlib.pyplot as plt
import numpy as np
from statistics import median, mean
from unco import UNCO_PATH
from pathlib import Path

def _plot_results_increasing_alternatives(X : range, results : list[list[list[float]]], querylist : list[int], modellist : list[int], increasing_alternatives : bool):
    output = [[[] for _ in modellist] for _ in querylist]
    for res in results:
        for query_numb, query_res in enumerate(res):
            for model_numb, model_res in enumerate(query_res):
                output[query_numb][model_numb].append(model_res)
    
    for index, query_numb in enumerate(querylist):
        fig = plt.figure()
        for modelindex, model_numb in enumerate(modellist):
            color, linestyle = "r", "-"
            if model_numb == 9: model_numb = "9a"
            model_numb = "9b" if model_numb == 10 else str(model_numb)
            plt.plot(X, output[index][modelindex], color=color, linestyle=linestyle, label=str(model_numb))

        if increasing_alternatives: plt.xlabel("#Alternatives per uncertain statement")
        else: plt.xlabel("#Uncertainties per column")

        plt.ylabel("Time in seconds")
        if increasing_alternatives: plt.title(f"Query {query_numb} with increasing numb alternatives")
        else: plt.title(f"Query {query_numb} with increasing numb uncertainties")

        plt.legend()

        plt.ylim([0.3, 0.5])

        if increasing_alternatives: plt.savefig(Path(UNCO_PATH,f"src/benchmark/results/alternatives{query_numb}.pdf"), format="pdf", bbox_inches="tight")
        else: plt.savefig(Path(UNCO_PATH,f"src/benchmark/results/uncertainties{query_numb}.pdf"), format="pdf", bbox_inches="tight")

        plt.close(fig)
            # plt.show()
# Using Numpy to create an array X

  
# raw:
res =  [[[0.3667670488357544, 0.3790719509124756, 0.32606780529022217, 0.33585381507873535, 0.32983875274658203]], [[0.3863178491592407, 0.33143317699432373, 0.3413112163543701, 0.35440266132354736, 0.35872411727905273]], [[0.35680723190307617, 0.3451271057128906, 0.38420426845550537, 0.35397255420684814, 0.3674168586730957]], [[0.37145090103149414, 0.38288307189941406, 0.38218069076538086, 0.4143906831741333, 0.36792635917663574]], [[0.39224886894226074, 0.4002656936645508, 0.38802504539489746, 0.41953885555267334, 0.42248988151550293]], [[0.3967059850692749, 0.43999016284942627, 0.41041624546051025, 0.39187800884246826, 0.4538313150405884]], [[0.42918217182159424, 0.3875526189804077, 0.48749709129333496, 0.41272807121276855, 0.4612743854522705]], [[0.4730185270309448, 0.47080671787261963, 0.4363013505935669, 0.4010847806930542, 0.4686990976333618]], [[0.3763235807418823, 0.42282629013061523, 0.3840603828430176, 0.405977725982666, 0.40064728260040283]], [[0.4184378385543823, 0.4318462610244751, 0.40443718433380127, 0.40221357345581055, 0.4983034133911133]], [[0.5098508596420288, 0.474212646484375, 0.4526008367538452, 0.42930054664611816, 0.45665645599365234]]]


newres = [([median(l)] for l in sublist) for sublist in res]

print(_plot_results_increasing_alternatives(range(0,301,30),newres,querylist=[4],modellist=[1],increasing_alternatives=False))

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
