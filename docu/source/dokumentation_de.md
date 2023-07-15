Dokumentation
=============
Diese Dokumentation kann dazu genutzt werden, um einen Einblick in das Eingabeformat und die Arbeitsweise von UnCo zu erhalten.
Zudem ist eine Anleitung enthalten, wie die in der Masterthesis ausgeführten Benchmarktests selbst ausgeführt werden können und wie der Benchmark mit eigenen Modellierungen und SPARQL-Anfragen erweitert werden kann.
Diese lassen sich zudem individuell anpassen, sodass der Benchmark mit anderen Datensätzen oder anderen Parametern wiederholt werden kann.

Abschnitte:
-----------
 * [Eingabeformat](1_eingabeformat.md)
 * [Anleitungen](2_anleitungen.md)
 * [Modellierungen von Unsicherheiten](3_modellierungen.md)
 * [Automatisch generierte Dokumentation von UnCo](unco.md)

Project Aufbau
--------------

    ├── data
    |   ├── input           <- Beispiel Eingabedaten.
    |   ├── output          <- Speicherort der Ausgabe.
    |   ├── results         <- Benchmarkergebnisse der Masterthesis.
    │   └── thesis_graphs   <- Graphen und Code aus der Masterthesis.
    |
    ├── docu                <- Diese Dokumentation.
    │  
    ├── src
    |   ├── benchmark       <- Klassen und Queries, die für den Benchmark genutzt wurden.
    |   ├── rdfier_app      <- Die streamlit Anwendung RDFier.
    |   ├── unco            <- Das ist UnCo!
    |   └── setup.py        <- Macht Projekt pip-installierbar (pip install -e ./src).
    |
    ├── __main__.py         <- Startet UnCo mit "python .".
    |
    ├── README.md           <- Liesmich Datei als Kurzbeschreibung.
    |
    ├── installation.bat/sh <- CMD/Shell Skript zum installieren von UnCo.
    |
    ├── start_unco.bat/sh   <- CMD/Shell Skript zum starten von UnCo.
    |
    └── requirements.txt    <- Benötigte Python Bibliotheken.


Wrong language? Change language to -> [english](documentation_en.md) <-