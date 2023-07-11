Uncertainty Comparator
======================

Description
-----------
This project contains tools for importing datasets with uncertainties, transforming them into rdf graphs and executing SPARQL queries.
Furthermore, benchmarks can be executed to compare different models of uncertainties in RDF graphs.

Project Organization
--------------------

    ├── data
    |   ├── input           <- Example input files.
    |   ├── output          <- Output files.
    |   ├── results         <- Results of the master thesis benchmarks.
    │   └── thesis_graphs   <- Graphs and Code which is shown in the thesis.
    |
    ├── docu                <- The documentation of UnCo.
    │  
    ├── execution           <- Execution and installation files.
    │  
    ├── src
    |   ├── benchmark       <- Scripts and queries needed for benchmarking.
    |   ├── rdfier_app      <- The streamlit application RDFier.
    |   ├── unco            <- This is UnCo!
    |   └── setup.py        <- Makes project pip-installable (pip install -e ./src).
    |
    ├── __main__.py         <- Starts UnCo with "python .".
    |
    ├── README.md           <- This document.
    |
    ├── installation.bat/sh <- CMD/Shell Script to install UnCo.
    |
    ├── start_unco.bat/sh   <- CMD/Shell Script to start UnCo.
    |
    └── requirements.txt    <- Required python libraries.

Installation and Execution
--------------------------
The project was tested on Windows and Linux (Ubuntu). Required installations: python 3.10 or higher and for linux python3.10-venv.
To install and execute UnCo, you can execute the files in the execution folder, or enter the following commands in the console (should be navigated in the project folder):

**Windows**:
```shell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python .
```

**Linux**:
```shell
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
python3 .
```

If you want to run a benchmark, you must first download a [Apache Jena Fuseki](https://jena.apache.org/download/index.cgi) server and install a suitable Java distribution.
When starting UnCo, the location of the server folder is requested. If no path is given, the program expects a "apache-jena-fuseki-4.8.0" folder in src.

Documentation
-------------
A documentation of UnCo is available in English ([here](docu/0_en_documentation.md)) and German ([here](docu/0_de_dokumentation.md)).

Update UnCo Documentation
-------------------------
```shell
cd docu/unco_docu
pydoc-markdown -I ../src -p unco --render-toc > unco.md
```
