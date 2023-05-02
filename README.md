RDFier
======


Project Organization
--------------------

    ├── data
    │   └── output          <- Output files.
    |
    ├── docs                <- The documentation of RDFier.
    │  
    ├── src
    |   ├── setup.py            <- Makes project pip-installable (pip install -e .).
    |   ├── app                 <- Streamlit webpage of the RDFier.
    |   ├── app_unco            <- Streamlit webpage includes a method to create pseudorandom uncertainties.
    |   ├── fuseki              <- Fuseki server for benchmarktests.
    |   ├── unco                <- This is the RDFier!
    │       ├── data
    │       └── features
    |
    ├── tests               <- Tests and test data.
    |
    ├── requirements.txt    <- Required python libraries.
    |
    └── README.md           <- This document.

--------

Installation
------------
Windows:
Required installations: python 3.10 or higher.
```shell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Linux:
Required installations: python3 and python3.10-venv.
```shell
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

Start RDFier
------------
```shell
streamlit run src/app/RDFier.py
```

