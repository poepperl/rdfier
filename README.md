RDFier
======

Description
-----------
This project contains tools for importing datasets with uncertainties, transforming them into rdf graphs and executing SPARQL queries.

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

**Windows**:
```shell
pip install poetry
poetry config virtualenvs.path "{project-dir}/.venv"
poetry lock
.venv\Scripts\activate
poetry install
```

**Linux**:
```shell
pip3 install poetry
poetry config virtualenvs.path "{project-dir}/.venv"
poetry lock
source .venv/bin/activate
poetry install
```

Documentation
-------------
A documentation of RDFier is available in English ([here](docu/0_en_documentation.md)) and German ([here](docu/0_de_dokumentation.md)).

Update RDFier Documentation
---------------------------
```shell
pydoc-markdown -I src -p scripts --render-toc > docu/source/rdfier.md
```
