Dokumentation
=============
Diese Dokumentation kann dazu genutzt werden, um einen Einblick in das Eingabeformat und die Arbeitsweise von RDFier zu erhalten.
Diese lassen sich zudem individuell anpassen, sodass der Benchmark mit anderen Datensätzen oder anderen Parametern wiederholt werden kann.

Abschnitte:
-----------
 * [Eingabeformat](1_eingabeformat.md)
 * [Modellierungen von Unsicherheiten](3_modellierungen.md)
 * [Automatisch generierte Dokumentation von RDFier](rdfier.md)

Projekt Aufbau
--------------

    ├── data
    │   ├── input           <- Beispiel Eingabedaten.
    │   └── output          <- Speicherort der Ausgabe.
    │
    ├── docu                <- Diese Dokumentation.
    │  
    ├── src
    │   ├── rdfier_app      <- Die streamlit Anwendung RDFier.
    │   ├── scripts         <- Die Logik von RDFier!
    │   └── setup.py        <- Macht Projekt pip-installierbar (pip install -e ./src).
    │
    ├── README.md           <- Liesmich Datei als Kurzbeschreibung.
    │
    ├── installation.bat/sh <- CMD/Shell Skript zum installieren von RDFier.
    │
    ├── start_rdfier.bat/sh   <- CMD/Shell Skript zum starten von RDFier.
    │
    └── requirements.txt    <- Benötigte Python Bibliotheken.


Wrong language? Change language to -> [english](documentation_en.md) <-