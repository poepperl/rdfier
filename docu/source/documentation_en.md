Documentation
=============
This documentation can be used to get an insight into the input format and the operation of UnCo.
In addition, instructions are included on how to run the benchmark tests performed in the master thesis and how the benchmark can be extended with own models and SPARQL queries.
These can be customized so that the benchmark can be repeated with other data sets or other parameters.

Sections:
------
 * [Input Format](1_input_format.md)
 * [Instructions](2_instructions.md)
 * [Uncertainty Models](3_models.md)
 * [Automatic generated documentation of UnCo](unco.md)

Project Organization
--------------------

    ├── data
    |   ├── input           <- Example input files.
    |   ├── output          <- Output files.
    |   ├── results         <- Results and plots of the master thesis benchmark.
    │   └── thesis_graphs   <- Graphs and code which is shown in the thesis as figures.
    |
    ├── docu                <- This documentation of UnCo.
    │  
    ├── src
    |   ├── benchmark       <- Scripts and queries needed for benchmarking.
    |   ├── rdfier_app      <- The streamlit application RDFier.
    |   ├── unco            <- This is UnCo!
    |   └── setup.py        <- Makes project pip-installable (pip install -e ./src).
    |
    ├── __main__.py         <- Starts UnCo with "python .".
    |
    ├── README.md           <- Readme file to getting started.
    |
    ├── installation.bat/sh <- CMD/Shell Script to install UnCo.
    |
    ├── start_unco.bat/sh   <- CMD/Shell Script to start UnCo.
    |
    └── requirements.txt    <- Required python libraries.


Falsche Sprache? Ändere die Sprache zu -> [deutsch](dokumentation_de.md) <-