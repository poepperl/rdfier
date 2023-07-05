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

        if increasing_alternatives: plt.savefig(Path(UNCO_PATH,f"src/benchmark/results/alternatives{query_numb}.pdf"), format="pdf", bbox_inches="tight")
        else: plt.savefig(Path(UNCO_PATH,f"src/benchmark/results/uncertainties{query_numb}.pdf"), format="pdf", bbox_inches="tight")

        plt.close(fig)
            # plt.show()
# Using Numpy to create an array X

  
# Assign variables to the y axis part of the curve
res = [[[0.15069304572211373, 0.15085617701212564, 0.15370845794677734, 0.15122056007385254, 0.1516537136501736]], [[0.16597739855448404, 0.1627038319905599, 0.16442243258158365, 0.16751029756334093, 0.1638078424665663]], [[0.1623457537757026, 0.16207019488016763, 0.16527247428894043, 0.1633881992763943, 0.16375992033216688]], [[0.16111095746358237, 0.16391105122036403, 0.16527003712124294, 0.1652098231845432, 0.1648352411058214]], [[0.16353403197394478, 0.16847825050354004, 0.16490175988939074, 0.16743932829962838, 0.16585230827331543]], [[0.17244786686367458, 0.16675109333462185, 0.1686302555931939, 0.16781581772698295, 0.171199984020657]], [[0.1655393441518148, 0.17048419846428764, 0.16892147064208984, 0.1673551400502523, 0.16916412777370876]], [[0.17337348726060656, 0.16865441534254286, 0.16850108570522732, 0.16805964046054417, 0.17017054557800293]], [[0.16918887032402885, 0.1724821991390652, 0.16984997855292427, 0.16951468255784777, 0.17186999320983887]], [[0.17826999558342826, 0.16903795136345756, 0.17122038205464682, 0.17364393340216744, 0.174570984310574]], [[0.1702345477210151, 0.17188172870212132, 0.17435974544949, 0.1745857662624783, 0.17589900228712294]], [[0.17118904325697157, 0.17250272962782118, 0.17428962389628092, 0.17587614059448242, 0.18145765198601616]], [[0.17326686117384169, 0.1755183537801107, 0.17801343070136177, 0.17972509066263834, 0.17737862798902723]], [[0.17434846030341256, 0.17444406615363228, 0.17775424321492514, 0.1795810063680013, 0.18141012721591526]], [[0.17601241005791557, 0.175962766011556, 0.181295288933648, 0.17987187703450522, 0.1907762951321072]], [[0.175698545244005, 0.17945305506388345, 0.18312425083584255, 0.1809693972269694, 0.19029582871331108]], [[0.1858748330010308, 0.1873696910010444, 0.1949040624830458, 0.19421945677863228, 0.19235891766018337]], [[0.18003739251030815, 0.1857103771633572, 0.18699600961473253, 0.18612019220987955, 0.1871164639790853]], [[0.18090168635050455, 0.18214307890997994, 0.18533354335361057, 0.18741562631395128, 0.18814685609605578]], [[0.1821992662217882, 0.18882706430223253, 0.1869451469845242, 0.18805678685506186, 0.198206451204088]], [[0.18696517414516872, 0.18239378929138184, 0.18567885292900932, 0.19150858455234104, 0.19087433815002441]]] 


newres = [([mean(l[:])] for l in sublist) for sublist in res]

print(_plot_results_increasing_alternatives(range(0,1001,50),newres,querylist=[4],modellist=[1],increasing_alternatives=False))

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
