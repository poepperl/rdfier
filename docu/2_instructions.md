# Instructions

This manual describes how to start UnCo and how to run the benchmarktests described in my master thesis.

## Operating instructions

To start UnCo you can execute the file *execution/start_unco* (.bat for windows and .sh for linux), or open a terminal, navigate to the project folder and run the following commands:
```shell
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux
python .
```

After that the python script *\_\_main\_\_.py* will be executed.
Now it can be selected whether the streamlit application RDFier or a benchmark should be executed.
At any time the terminal can be closed by entering `Q`.
When entering parameters, the bracketed value gives an indication of which value will be selected by default if the input is left blank.
Entering a `1` will start the app immediately, entering `0` will first prompt for the following parameters to run a benchmark:

 * **Path of the Fuseki server**: This is specified by a full path or a relative path starting from the project folder. By default, the program computes with a Fuseki Server version 4.8.0 in the src folder.
 * **Path to the input dataset**: Specified by a full or a relative path starting from the project folder.
 * **Path to namespace table**: Specified by a full or relative path starting from the project folder.
 * **Selection of increasing parameter**: Which parameter should be incremented? If no parameter is to be incremented, the selection has no effect.
 * **Selection of the columns to be edited**: Which columns should be edited step by step? The specification is made by column numbers separated by commas.
 * **Selection of modelings**: Which modelings are to be compared? The specification is made by IDs of modelings separated by commas. Multiple selection possible.
 * **Selection of SPARQL queries**: Which queries should be used for comparison? This is specified by IDs of modeling separated by commas.
 * **Selection of parameter range**: In which range should the parameter be tested? The specification is done by three integers `start`, `stop` and `step`, which is used to generate a Python `range(start, stop, step)`. If no parameter is to be incremented the default values can be used and thus the input can be left empty.

## Executions of the master thesis
In the context of my master thesis some benchmark tests with UnCo were executed. In the following it is described how the ones executed there can be executed themselves.
As data set a table extracted from the AFE database was used. Since this contains mostly unpublished data, the dataset cannot be made available. A comparable data set with the already published data can be found in `data/input/afe_public.csv`.

### Section 4.1.7 Measurement methods and performance indicators
In this section, experiments were conducted using various procedures designed to avoid outliers and noise in measurements.
To generate Figure 4.15 (a), the number of calculated medians and means must first be manually set to 1.
For this, in `src/benchmark/benchmark.py` in line 48 and 49 the two constants must be set to 1.
The following parameters were used when running UnCo:
 * **Dataset**: AFE dataset
 * **Increasing parameter**: Number of uncertainties (0)
 * **Columns**: Default value
 * **Models**: 1, 1, 1, 1
 * **Queries**: 4
 * **Range**: Start: 0; Stop: 301; Step size: 30

After execution, in `data/results/plots/uncertainties4.pdf` is the results of the execution, which is present in the master thesis as Figure 4.15 (a). Graph (b) is created by manually calculating the median.

For the generation of figure 4.16 (a), first the constant `self.MEDIAN_LOOPS` has to be set to 5 again. After that UnCo can be started with the same parameters as just described.
Figure 4.16 (a) shows the resulting graph, but with the same field of view as already shown in Figure 4.15. The graph (b) was calculated manually from the mean value.

Note: Make sure that the constants changed here are set back to the previous value. For even more robust results, higher values can of course be used, whereby especially the choice of 'self.MEAN_LOOPS' has a significant impact on the runtime.

### Section 4.2.1 Comparison with respect to AFE
In this section, a benchmark test was run on the unprocessed version of the AFE dataset.
The following parameters were used when running UnCo:
 * **Dataset**: AFE dataset
 * **Increasing parameter**: Default value (no effect).
 * **Columns**: Default value (no effect)
 * **Models**: Default value
 * **Queries**: Default value
 * **Range**: Default values

After execution, the results are output in the terminal.

### Section 4.2.2 Comparison with increasing number of uncertainties
In this section, a benchmark test was executed with increasing number of uncertainties.
The following parameters were used when executing UnCo:
 * **Dataset**: AFE dataset with no uncertainties specified.
 * **Increasing parameter**: Number of uncertainties (0)
 * **Columns**: Default value
 * **Models**: Default value
 * **Queries**: Default value
 * **Range**: Start: 0; Stop: 10001; Step size: 1000.

Since the used working memory was not sufficient, the results of the master thesis were compiled from three individual executions.
For this, the ranges (0, 5000, 1000), (5000, 8000, 1000) and (8000, 10001, 1000) were used.
After the execution, the results are saved in `data/results/plots/uncertainties{queryID}.pdf`, as well as the exact list of results is printed in the terminal.

### Section 4.2.3 Comparison with increasing number of alternatives
In this section, a benchmark test was executed with increasing number of alternatives.
The following parameters were used when running UnCo:
 * **Dataset**: AFE dataset
 * **Increasing parameter**: Number of alternatives (1)
 * **Columns**: Default value
 * **Models**: Default value
 * **Queries**: Default value
 * **Range**: Start: 0; Stop: 101; Step Size: 10.

Since the used working memory was not sufficient, the results of the master thesis were compiled from three individual executions.
The ranges (0, 40, 10), (40, 80, 10) and (80, 101, 10) were used for this purpose.
After the execution, the results are saved in `data/results/plots/alternatives{queryID}.pdf`, as well as the exact list of results is printed in the terminal.