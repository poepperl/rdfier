import streamlit as st

st.set_page_config(
    page_title="Funktionsweise",
    layout="wide")

st.title('Über das Modul')

st.write(
    """
    Dieses Modul wurde im Rahmen der Masterarbeit von Luca Pöpperl entwickelt, um unterschiedliche Modellierungen für Uncertainty
    in RDF-Graphen zu untersuchen und Benchmarktests mit diesen durchzuführen.
    Diese Webapplikation bietet eine einfache Möglichkeit, CSV-Daten in RDF-Graphen zu konvertieren, indem es eine Mapping-Syntax verwendet,
    welche auf der Seite [📝Eingabeformat](http://localhost:8501/Eingabeformat) genauer beschrieben wird.

    Auf der [Startseite](http://localhost:8501) können eigene csv-Tabellen eingegeben werden und der daraus resultierende Graph angezeigt werden.
    Nachdem eine csv-Datei hochgeladen wurde können zunächst weitere Konfigurationen vorgenommen werden:
    - Zunächst wird die eingegebene csv-Tabelle angezeigt. Dabei lassen sich alle Felder der Tabelle bearbeiten und mit Klick auf eine Spaltenüberschrift,
    lassen sich die jeweiligen Spalten sortieren.
    - Im Bereich "RDF Format" kann das Ausgabeformat (Turtle oder XML) ausgewählt werden.
    - Durch das deaktivieren von "Graphische Darstellung", wird der Graph nur in einem Textfeld, im ausgewählten Format ausgegeben.
    Standardmäßig wird zusätzlich eine graphische Darstellung generiert.
    - Durch den Upload einer Präfixtabelle, lassen sich Präfixe, welche in der Eingabe enthalten sind, mit den gewünschten Namensräumen verknüpfen.
    Diese müssen im csv-Format eingegeben werden und erwartet eine Tabelle mit den Spalten (prefix,namespace).

    Nun lässt sich der RDF Graph generieren. Nachdem ein Graph einmal generiert wurde, lassen sich alle oben genannten Konfigurationen "live" anpassen,
    sodass die Auswirkungen auf den Graphen erkennbar sind.
    """
)