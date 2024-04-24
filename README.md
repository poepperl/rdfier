RDFier
======

Description
-----------
This project contains tools for importing datasets with uncertainties, transforming them into rdf graphs and executing SPARQL queries.

You want to test the module? -> https://rdfier.streamlit.app/

Project Organization
--------------------

    ├── data
    │   ├── input           <- Example input files.
    │   └── output          <- Output files.
    │
    ├── docu                <- This documentation of RDFier.
    │  
    ├── src
    │   ├── rdfier_app      <- The streamlit application RDFier.
    │   ├── scripts         <- This is RDFier!
    │   └── setup.py        <- Makes project pip-installable (pip install -e ./src).
    │
    │
    ├── README.md           <- Readme file to getting started.
    │
    └── pyproject.toml      <- Required python libraries.

Installation and Execution
--------------------------

```shell
pip install poetry # for Linux use pip3 instead
poetry config virtualenvs.path "{project-dir}/.venv"
poetry lock
poetry shell
poetry install
streamlit run src/rdfier_app/RDFier.py
```


Documentation
-------------
A documentation of RDFier is available in English ([here](docu\source\documentation_en.md)) and German ([here](docu\source\dokumentation_de.md)).

Update RDFier Documentation
---------------------------
```shell
pydoc-markdown -I src -p scripts --render-toc > docu/source/rdfier.md
```
