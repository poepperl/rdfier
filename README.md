UNCO
====


Project Organization
--------------------

    ├── data
    │   ├── external       <- Daten von externen Quellen.
    │   ├── interim        <- Ordner für zwischengespeicherte Daten.
    │   ├── processed      <- Verarbeitete Daten.
    │   └── raw            <- Original Daten.
    │  
    ├── docker             <- Hier werden die Docker Container abgelegt.
    |
    ├── docs               <- Unsere Dokumenation von TOS.
    │  
    ├── models             <- Von TOS genutzte Modelle.
    │  
    ├── notebooks          <- Jupyter notebooks.
    │  
    ├── references         <- Weitere hilfreiche Materialien.
    │  
    ├── reports            <- Generierte Analysen.
    │  
    ├── src                <- Source code, um TOS zu benutzen.
    |   ├── setup.py       <- Macht das Projekt durch pip installierbar (pip install -e .).
    |   ├── scripts        <- Skripte die nicht zu TOS gehören.
    |   ├── unco           <- Das ist UNCO!
    │       ├── data                <- Skripte/Klassen zum bearbeiten, analysieren oder generieren von Daten.
    │       ├── features            <- Skripte/Klassen, um aus Rohdaten Features für Modelle zu generieren.
    │       ├── models              <- Skripte, um Modelle zu trainieren und einzusetzen.
    │       └── visualization       <- Skripte für die Visualisierung von Ergebnissen.
    |
    ├── tests              <- Unittests.
    |
    ├── requirements.txt   <- Für die Entwicklungsumgebung erforderliche Module.
    |
    ├── README.md          <- Dieses Dokument.

--------

Getting started
---------------

```shell
python -m venv .venv                // nur bei erster Ausführung notwendig
.venv\Scripts\activate
pip install -r requirements.txt     // nur bei erster Ausführung notwendig
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

