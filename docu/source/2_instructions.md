# Instructions

This manual describes how to start UnCo and how to run the benchmark tests described in my master thesis.

## Installation

Python 3.10 or higher is required to use the program. The benchmark is executed using an Apache Jena Fuseki server, which is already included in the electronic appendix of the master thesis. Fuseki requires a suitable Java installation (Java 11.0.19 was used to run the benchmark of the thesis).

To install UnCo you can execute *installation.bat* (for Windows) or *installation.sh* (for Linux). This creates a virtual environment *.venv* in which all required python libraries are installed. Alternatively, the commands in *README.md* can be executed.

Note: If permission errors occur on Linux, it may be helpful to use `chmod u=rwx,g=r,o=r installation.sh` to give the script the necessary permissions. The same should be executed with *start_unco.sh*.

## Operating instructions

To start UnCo you can execute the file *start_unco* (.bat for windows and .sh for linux), or open a terminal, navigate to the project folder and run the following commands:
```shell
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux
python .
```

After that the python script *\_\_main\_\_.py* will be executed.
Now it can be selected whether the streamlit application RDFier or a benchmark should be executed.
At any time the terminal can be closed by entering `Q`.
When entering parameters, the value in brackets gives an indication of which value will be selected by default if the input is left blank.
Entering a `1` will start the app immediately, entering `0` will first prompt for the following parameters to run a benchmark:

 * **Path of the Fuseki server**: This is specified by a full path or a relative path starting from the project folder. By default, the program computes with a (Fuseki Server)[https://jena.apache.org/download/index.cgi] version 4.8.0 in the src folder.
 * **Path to the input dataset**: Specified by a full or a relative path starting from the project folder.
 * **Path to namespace table**: Specified by a full or relative path starting from the project folder.
 * **Selection of increasing parameter**: Which parameter should be increased? If no parameter is to be increased, the selection has no effect.
 * **Selection of the columns to be edited**: Which columns should be edited step by step? The specification is made by column numbers separated by commas.
 * **Selection of models**: Which models are to be compared? The specification is made by model IDs separated by commas. Multiple selection possible.
 * **Selection of SPARQL queries**: Which queries should be used for comparison? This is specified by query IDs separated by commas.
 * **Selection of parameter range**: In which range should the parameter be tested? The specification is done by three integers `start`, `stop` and `step`, which is used to generate a python range `range(start, stop, step)`. If no parameter is to be incremented the default values can be used and thus the input can be left empty.

## Executions of the master thesis
In the context of my master thesis some benchmark tests with UnCo were executed. In the following it is described how them can be executed themselves.
As dataset a table extracted from the AFE database was used. Since this contains mostly unpublished data, the dataset cannot be made available. A comparable dataset with the already published data can be found in `data/input/afe_public.csv`.

### Section 4.1.7 Measurement methods and metric
In this section, experiments were conducted using various procedures designed to avoid outliers and noise in measurements.
To generate Figure 4.17 (a), the number of calculated medians and means must first be manually set to 1.
For this, in `src/benchmark/benchmark.py` in line 48 and 49 the two constants must be set to 1.
The following parameters were used when running UnCo:
 * **Dataset**: AFE dataset
 * **Increasing parameter**: Number of uncertainties (0)
 * **Columns**: Default value
 * **Models**: 1, 1, 1, 1
 * **Queries**: 4
 * **Range**: start: 0; stop: 301; step: 30

After execution, in `data/results/plots/uncertainties4.pdf` is the result of the execution, which is present in the master thesis as figure 4.17 (a). Graph (b) is created by manually calculating the median.

For the generation of figure 4.18 (a), first the constant `self.MEDIAN_LOOPS` has to be set to 5 again. After that UnCo can be started with the same parameters as just described.
Figure 4.18 (a) shows the resulting graph, but with the same field of view as already shown in Figure 4.17. The graph (b) was calculated manually from the mean value.

Note: Make sure that the constants changed here are set back to the previous value. For even more robust results, higher values can of course be used, whereby especially the choice of `self.MEAN_LOOPS` has a significant impact on the runtime.

Besides the simple output of the runtimes, UnCo also generates the rankings described there.
To set the tolerance range of same ranks, in `src/benchmark/benchmark.py` line 276 the value of `tolerance` must be edited.
By default, this is set to 0.05, i.e. 5%.

### Section 4.2.1 Comparison with respect to AFE
In this section, a benchmark test was run on the unprocessed version of the AFE dataset.
The following parameters were used when running UnCo:
 * **Dataset**: AFE dataset
 * **Increasing parameter**: Default value (no effect)
 * **Columns**: Default value (no effect)
 * **Models**: Default value
 * **Queries**: Default value
 * **Range**: Default values

After execution, the results are printed in the terminal.

### Section 4.2.2 Comparison with increasing number of uncertainties
In this section, a benchmark test was executed with increasing number of uncertainties.
The following parameters were used when executing UnCo:
 * **Dataset**: AFE dataset with no specified uncertainties
 * **Increasing parameter**: Number of uncertainties (0)
 * **Columns**: Default value
 * **Models**: Default value
 * **Queries**: Default value
 * **Range**: start: 0; stop: 10001; step: 1000.

Since the used main memory was not sufficient, the results of the master thesis were compiled from three individual executions.
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
 * **Range**: start: 0; stop: 101; step: 10.

Since the used main memory was not sufficient, the results of the master thesis were compiled from three individual executions.
The ranges (0, 40, 10), (40, 80, 10) and (80, 101, 10) were used for this purpose.
After the execution, the results are saved in `data/results/plots/alternatives{queryID}.pdf`, as well as the exact list of results is printed in the terminal.

### Section 4.2.4 Comparison on synthetic generated Datasets
In this section, a benchmark test was run on synthetically generated datasets based on AFE.
A synthetically generated dataset of the published part of AFE is located in `data/thesis_data/afe/synthetic.csv`.
The following parameters were used when running UnCo:
 * **Dataset**: synthetic AFE dataset.
 * **Increasing parameter**: Number of uncertainties (0)
 * **Columns**: Default value
 * **Models**: Default value
 * **Queries**: Default value
 * **Range**: start: 10000; stop: 10001; step: 1.

After execution, the results are printed to the terminal.

## Extension of the benchmark
UnCo has been specially created so that new models and queries can easily be added. For this purpose, the following files must be edited:

**Adding a model with ID X**:
 * *src/unco/features/graph_generator.py*: A new method *_generate_uncertain_statement_model_X* must be created, which contains the model equivalent to the other methods. The resources *subject*, *predicate*, *object*, as well as a uncertainty weight *weight* and the column index *index* of the object are available as input.
 Subsequently, the model must be integrated in the method *generate_graph*. To do this, include it equivalent to the other models as a new *case X:* and add the required parameters.
 * *src/benchmark/queries/*: Here the available queries are stored for each model. With a new model a new folder *modelX* must be added, in which the files *query1.rq* to *query6.rq* are contained. In these files the respective SPARQL queries are contained.
 * Optional: In *\_\_main\_\_.py* the ID X can be added to execute the new model as default. To do this, just add `str(X)` to the `all_model_ids` list in line 21.

**Adding a query with ID Y**:
* *src/benchmark/queries/*: Here the available queries are stored for each model. With a new query the file *queryY.rq* must be added in each contained folder. There the SPARQL query must be contained suitably to the respective model.
 * Optional: In *\_\_main\_\_.py* the ID Y can be added, in order to execute the new queries as default. To do this, just add `str(Y)` to the `all_query_ids` list in line 22.