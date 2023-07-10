Uncertainty Comparator
======================


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
    ├── __main__.py         <- Starts UnCo with "python ."
    |
    ├── README.md           <- This document.
    |
    └── requirements.txt    <- Required python libraries.

--------

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
