UNCO
====


Project Organization
--------------------

    ├── data
    │   ├── input           <- Daten von externen Quellen.
    │   └── output          <- Verarbeitete Daten.
    |
    ├── docs                <- Unsere Dokumenation von UNCO.
    │  
    ├── src                 <- Source code, um UNCO zu benutzen.
    |   ├── setup.py            <- Macht das Projekt durch pip installierbar (pip install -e .).
    |   ├── app                 <- Streamlit Webpage zum bedienen von UNCO.
    |   ├── app_masterarbeit    <- Streamlit Webpage inklusive uncertainty-generator und SPARQL-Schnittstelle.
    |   ├── fuseki              <- Fuseki Server für Benchmarktests.
    |   ├── unco                <- Das ist UNCO!
    │       ├── data                <- Skripte/Klassen zum Bearbeiten, Analysieren oder Generieren von Daten.
    │       └── features            <- Features von UNCO.
    |
    ├── tests               <- Unittests.
    |
    ├── requirements.txt    <- Für die Entwicklungsumgebung erforderliche Module.
    |
    └── README.md           <- Dieses Dokument.

--------

Getting started
---------------

```shell
python -m venv .venv                // nur bei erster Ausführung notwendig
.venv\Scripts\activate
pip install -r requirements.txt     // nur bei erster Ausführung notwendig
streamlit run src/app/Startseite.py
```

UNCO starten
------------
```shell
.venv\Scripts\activate
streamlit run src/app/Startseite.py
```

oder für die Version mit SPARQL-Schnittstelle und randomisierter Unsicherheit:

```shell
.venv\Scripts\activate
streamlit run src/app_masterarbeit/Startseite.py
```

Dokumentation generieren
------------------------

```
cd docs
sphinx-apidoc -lfM -d 0 -o source/unco/ ../src/unco
make html
```

-> Öffne docs/build/html/index.html in Browser

Create package
--------------

```shell
python src/setup.py sdist
```

