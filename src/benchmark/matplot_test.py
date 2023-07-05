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

        plt.ylim([0.3, 0.55])

        if increasing_alternatives: plt.savefig(Path(UNCO_PATH,f"src/benchmark/results/alternatives{query_numb}.pdf"), format="pdf", bbox_inches="tight")
        else: plt.savefig(Path(UNCO_PATH,f"src/benchmark/results/uncertainties{query_numb}.pdf"), format="pdf", bbox_inches="tight")

        plt.close(fig)
            # plt.show()
# Using Numpy to create an array X

  
# Assign variables to the y axis part of the curve
res =  [[[0.38080573081970215, 0.316852331161499, 0.3379244804382324, 0.3287019729614258, 0.34969663619995117]], [[0.34711742401123047, 0.3708319664001465, 0.34216833114624023, 0.43318843841552734, 0.33252525329589844]], [[0.3596370220184326, 0.3578023910522461, 0.39238595962524414, 0.3565254211425781, 0.37126874923706055]], [[0.3596820831298828, 0.40100741386413574, 0.3925654888153076, 0.3901376724243164, 0.3600575923919678]], [[0.40846753120422363, 0.35976338386535645, 0.4034082889556885, 0.3903515338897705, 0.3989386558532715]], [[0.41994810104370117, 0.3809683322906494, 0.37306761741638184, 0.4149298667907715, 0.43570995330810547]], [[0.40250587463378906, 0.3576483726501465, 0.42460012435913086, 0.4025695323944092, 0.42385244369506836]], [[0.4422879219055176, 0.4428822994232178, 0.44832801818847656, 0.4070460796356201, 0.3711812496185303]], [[0.4477231502532959, 0.4345686435699463, 0.42743682861328125, 0.44341349601745605, 0.44094061851501465]], [[0.461592435836792, 0.4093797206878662, 0.4344189167022705, 0.4288461208343506, 0.45568299293518066]], [[0.43532657623291016, 0.4022219181060791, 0.4777402877807617, 0.48148345947265625, 0.5474080848693848]]]

newres = [([median(l[:])] for l in sublist) for sublist in res]

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
