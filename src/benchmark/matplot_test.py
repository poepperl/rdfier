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

        plt.ylim([0.17, 0.26])

        if increasing_alternatives: plt.savefig(Path(UNCO_PATH,f"src/benchmark/results/alternatives{query_numb}.pdf"), format="pdf", bbox_inches="tight")
        else: plt.savefig(Path(UNCO_PATH,f"src/benchmark/results/uncertainties{query_numb}.pdf"), format="pdf", bbox_inches="tight")

        plt.close(fig)
            # plt.show()
# Using Numpy to create an array X

  
# Assign variables to the y axis part of the curve
res =  [[[0.20999956130981445, 0.21000051498413086, 0.20399951934814453, 0.2214980125427246, 0.20150017738342285]], [[0.20800042152404785, 0.22763943672180176, 0.24899959564208984, 0.21899914741516113, 0.21399950981140137]], [[0.21650028228759766, 0.2238938808441162, 0.23693084716796875, 0.2200174331665039, 0.20300006866455078]], [[0.24049997329711914, 0.20400071144104004, 0.2558016777038574, 0.2459728717803955, 0.23819470405578613]], [[0.230940580368042, 0.21750116348266602, 0.2200000286102295, 0.23999977111816406, 0.23750066757202148]], [[0.2395012378692627, 0.21360015869140625, 0.25749969482421875, 0.2597391605377197, 0.25500035285949707]]]

newres = [([median(l[:])] for l in sublist) for sublist in res]

print(_plot_results_increasing_alternatives(range(0,301,30),res,querylist=[4],modellist=[1,1,1,1,1],increasing_alternatives=False))

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
