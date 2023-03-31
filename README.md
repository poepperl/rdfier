RDFier
======


Project Organization
--------------------

    ├── data
    │   ├── input           <- Daten von externen Quellen.
    │   └── output          <- Verarbeitete Daten.
    |
    ├── docs                <- Unsere Dokumenation von RDFier.
    │  
    ├── src                 <- Source code, um RDFier zu benutzen.
    |   ├── setup.py            <- Macht das Projekt durch pip installierbar (pip install -e .).
    |   ├── app                 <- Streamlit Webpage zum bedienen von RDFier.
    |   ├── app_masterarbeit    <- Streamlit Webpage inklusive uncertainty-generator und SPARQL-Schnittstelle.
    |   ├── fuseki              <- Fuseki Server für Benchmarktests.
    |   ├── unco                <- Das ist der RDFier!
    │       ├── data                <- Skripte/Klassen zum Bearbeiten, Analysieren oder Generieren von Daten.
    │       └── features            <- Features von RDFier.
    |
    ├── tests               <- Unittests.
    |
    ├── requirements.txt    <- Für die Entwicklungsumgebung erforderliche Module.
    |
    └── README.md           <- Dieses Dokument.

--------

Installation
------------

```shell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

RDFier starten
--------------
```shell
.venv\Scripts\activate
streamlit run src/app/RDFier.py
```

Dokumentation generieren und öffnen
-----------------------------------

```
cd docs
sphinx-apidoc -lfM -d 0 -o source/unco/ ../src/unco
make html
```

-> Öffne docs/build/html/index.html in Browser

