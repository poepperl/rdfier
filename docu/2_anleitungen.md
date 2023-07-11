# Anleitungen

In dieser Anleitung wird beschrieben, wie UnCo gestartet werden kann und wie die in der Masterthesis beschriebenen Benchmarktests ausgeführt werden können.

## Installation

Um UnCo zu installieren kann *installation.bat* (für Windows) bzw. *installation.sh* (für Linux) ausgeführt werden. Dadurch wird eine virtuelle Umgebung *.venv* erstellt, in der alle benötigten Python Bibliotheken installiert werden. Alternativ können auch die Befehle in der *README.md* ausgeführt werden.

Hinweis: Sollten bei Linux Berechtigungsfehler entstehen, kann es hilfreich sein mit `chmod u=rwx,g=r,o=r installation.sh` dem Skript die notwendigen Rechte zu vergeben. Das gleiche sollte mit *start_unco.sh* ausgeführt werden.

## Bedienungsanleitung

Um UnCo zu starten kann die Ausführungsdatei *start_unco* (.bat für Windows und .sh für Linux) ausgeführt werden, oder im Terminal in den Projektordner navigiert und folgende Befehle ausgeführt werden:
```shell
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux
python .
```

Danach wird das Python Skript *\_\_main\_\_.py* ausgeführt.
Nun kann ausgewählt werden, ob die Streamlit Applikation RDFier oder ein Benchmark ausgeführt werden soll.
Zu jeder Zeit kann durch Eingabe von `Q`, das Terminal geschlossen werden.
Bei der Eingabe von Parametern gibt der eingeklammerte Wert einen Hinweis darauf, welcher Wert standardmäßig ausgewählt wird, wenn die Eingabe leer gelassen wird.
Durch die Eingabe einer `1` wird die App sofort gestartet, bei `0` werden zum Ausführen eines Benchmarks zunächst folgende Parameter abgefragt:

 * **Pfad des Fuseki Servers**: Die Angabe erfolgt durch einen vollständigen oder einen relativen Pfad ausgehend von dem Projektordner. Standardmäßig rechnet das Programm mit einem Fuseki Server der Version 4.8.0 im Ordner src.
 * **Pfad zum Eingabe-Datensatz**: Die Angabe erfolgt durch einen vollständigen oder einen relativen Pfad ausgehend von dem Projektordner.
 * **Pfad zur Namensraum-Tabelle**: Die Angabe erfolgt durch einen vollständigen oder einen relativen Pfad ausgehend von dem Projektordner.
 * **Auswahl des steigenden Parameters**: Welcher Parameter soll schrittweise erhöht werden? Wenn kein Parameter erhöht werden soll hat die Auswahl keine Auswirkung.
 * **Auswahl der bearbeitenden Spalten**: Welche Spalten sollen schrittweise bearbeitet werden? Die Angabe erfolgt durch Spaltennummern getrennt durch Kommata.
 * **Auswahl der Modellierungen**: Welche Modellierungen sollen verglichen werden? Die Angabe erfolgt durch IDs von Modellierungen getrennt durch Kommata. Mehrfachauswahl möglich.
 * **Auswahl der SPARQL-Anfragen**: Welche Queries sollen für den Vergleich genutzt werden? Die Angabe erfolgt durch IDs von Queries getrennt durch Kommata.
 * **Auswahl des Parameter-Bereichs**: In welchem Bereich soll der Parameter getestet werden? Die Angabe erfolgt durch drei Ganzzahlen `start`, `stop` und `step`, die für die Erzeugung einer Python Range `range(start, stop, step)` genutzt wird. Soll kein Parameter erhöht werden können die Standardwerte genutzt und somit die Eingabe leer gelassen werden.

## Ausführungen der Masterthesis
Im Rahmen meiner Masterthesis wurden einige Benchmarktests mit UnCo ausgeführt. Im Folgenden wird beschrieben, wie die dort ausgeführten selbst ausgeführt werden können.
Als Datensatz wurde eine aus der AFE Datenbank extrahierte Tabelle genutzt. Da diese zum Großteil nicht veröffentlichte Daten enthält, kann der Datensatz nicht zur Verfügung gestellt werden. Ein vergleichbarer Datensatz mit den bereits veröffentlichten Daten befindet sich in `data/input/afe_public.csv`.

### Abschnitt 4.1.7 Messverfahren und Leistungskennzahlen
In diesem Abschnitt wurden Versuche mit verschiedenen Verfahren durchgeführt, welche Ausreißer und Störungen in Messungen vermeiden sollen.
Zur Erzeugung der Abbildung 4.15 (a) muss zunächst die Anzahl der berechneten Mediane und Mittelwerte manuell auf 1 gesetzt werden.
Dazu muss in `src/benchmark/benchmark.py` in Zeile 48 und 49 die beiden Konstanten auf 1 gesetzt werden.
Bei der Ausführung von UnCo wurden folgende Parameter genutzt:
 * **Datensatz**: AFE-Datensatz
 * **Steigender Parameter**: Anzahl Unsicherheiten (0)
 * **Spalten**: Standardwert
 * **Modellierungen**: 1, 1, 1, 1, 1
 * **Queries**: 4
 * **Bereich**: Start: 0; Stopp: 301; Schrittgröße: 30

Nach der Ausführung befindet sich in `data/results/plots/uncertainties4.pdf` die Ergebnisse der Ausführung, welche in der Masterthesis als Abbildung 4.15 (a) vorhanden ist. Grafik (b) ist durch das manuelle Errechnen des Medians entstanden.

Für die Erzeugung von Abbildung 4.16 (a), muss zunächst die Konstante `self.MEDIAN_LOOPS` wieder auf 5 gesetzt werden. Danach kann UnCo mit den gleichen Parametern wie eben beschrieben gestartet werden.
Abbildung 4.16 (a) zeigt die daraus entstandene Grafik, jedoch mit dem gleichen Sichtfeld wie schon in Abbildung 4.15. Die Grafik (b) wurde manuell aus dem Mittelwert errechnet.

Hinweis: Stellen Sie sicher, dass die hier veränderten Konstanten wieder auf den vorherigen Wert gesetzt werden. Für noch robustere Ergebnisse können natürlich auch höhere Werte genutzt werden, wobei vorallem die Wahl von `self.MEAN_LOOPS` erhebliche Auswirkungen auf die Laufzeit besitzt.

### Abschnitt 4.2.1 Vergleich bezüglich AFE
In diesem Abschnitt wurde ein Benchmarktest auf die unbearbeitete Version des AFE Datensatzes ausgeführt.
Bei der Ausführung von UnCo wurden folgende Parameter genutzt:
 * **Datensatz**: AFE-Datensatz
 * **Steigender Parameter**: Standardwert (keine Auswirkung)
 * **Spalten**: Standardwert (keine Auswirkung)
 * **Modellierungen**: Standardwert
 * **Queries**: Standardwert
 * **Bereich**: Standardwerte

Nach der Ausführung werden die Ergebnisse im Terminal ausgegeben.

### Abschnitt 4.2.2 Vergleich bei steigender Anzahl Unsicherheiten
In diesem Abschnitt wurde ein Benchmarktest mit steigender Anzahl Unsicherheiten ausgeführt.
Bei der Ausführung von UnCo wurden folgende Parameter genutzt:
 * **Datensatz**: AFE-Datensatz ohne Angaben von Unsicherheiten
 * **Steigender Parameter**: Anzahl Unsicherheiten (0)
 * **Spalten**: Standardwert
 * **Modellierungen**: Standardwert
 * **Queries**: Standardwert
 * **Bereich**: Start: 0; Stopp: 10001; Schrittgröße: 1000

Da der genutzte Arbeitsspeicher nicht ausgereicht hat, wurden die Ergebnisse der Masterthesis aus drei einzelnen Ausführungen zusammengetragen.
Dafür wurden die Bereiche (0, 5000, 1000), (5000, 8000, 1000) und (8000, 10001, 1000) genutzt.
Nach der Ausführung werden die Ergebnisse in `data/results/plots/uncertainties{queryID}.pdf` gespeichert, sowie die genaue Liste der Ergebnisse im Terminal ausgegeben.

### Abschnitt 4.2.3 Vergleich bei steigender Anzahl Alternativen
In diesem Abschnitt wurde ein Benchmarktest mit steigender Anzahl Alternativen ausgeführt.
Bei der Ausführung von UnCo wurden folgende Parameter genutzt:
 * **Datensatz**: AFE-Datensatz
 * **Steigender Parameter**: Anzahl Alternativen (1)
 * **Spalten**: Standardwert
 * **Modellierungen**: Standardwert
 * **Queries**: Standardwert
 * **Bereich**: Start: 0; Stopp: 101; Schrittgröße: 10

Da der genutzte Arbeitsspeicher nicht ausgereicht hat, wurden die Ergebnisse der Masterthesis aus drei einzelnen Ausführungen zusammengetragen.
Dafür wurden die Bereiche (0, 40, 10), (40, 80, 10) und (80, 101, 10) genutzt.
Nach der Ausführung werden die Ergebnisse in `data/results/plots/alternatives{queryID}.pdf` gespeichert, sowie die genaue Liste der Ergebnisse im Terminal ausgegeben.

### Abschnitt 4.2.4 Vergleich bei künstlich erzeugten Datensätzen
In diesem Abschnitt wurde ein Benchmarktest auf synthetisch erzeugten Datensätzen basierend auf AFE ausgeführt.
Bei der Ausführung von UnCo wurden folgende Parameter genutzt:
 * **Datensatz**: synthetischer AFE-Datensatz
 * **Steigender Parameter**: Anzahl Unsicherheiten (0)
 * **Spalten**: Standardwert
 * **Modellierungen**: Standardwert
 * **Queries**: Standardwert
 * **Bereich**: Start: 10000; Stopp: 10001; Schrittgröße: 1

Nach der Ausführung werden die Ergebnisse im Terminal ausgegeben.

## Erweiterung des Benchmarks
UnCo wurde speziell so angelegt, dass auch neue Modellierungen und Queries hinzugefügt werden können. Dazu müssen folgende Dateien bearbeitet werden:

**Hinzufügen einer Modellierung mit ID X**:
 * *src/unco/features/graph_generator.py*: Eine neue Methode *_generate_uncertain_statement_model_X* muss erstellt werden, welche äquivalent zu den anderen Methoden die Modellierung beinhaltet. Als Eingabe sind die Ressourcen *subject*, *predicate*, *object*, sowie eine Gewichtung *weight* und der Spaltenindex *index* des Objekts verfügbar.
 Anschließend muss die Modellierung in der Methode *generate_graph* eingebunden werden. Dazu wird diese äquivalent zu den anderen Modellierungen als neuer *case X:* eingebunden und die benötigten Parameter übergeben.
 * *src/benchmark/queries/*: Hier werden zu jeder Modellierung die verfügbaren Queries gespeichert. Bei einer neuen Modellierung muss ein neuer Ordner *modelX* hinzugefügt werden, in dem die Dateien *query1.rq* bis *query6.rq* enthalten sind. In diesen Dateien sind die jeweiligen SPARQL-Queries enthalten.
 * Optional: In *\_\_main\_\_.py* kann die ID X hinzugefügt werden, um beim Standardwert auch die neue Modellierung auszuführen. Dazu muss lediglich `str(X)` in die Liste `all_model_ids` in Zeile 21 eingefügt werden.

**Hinzufügen einer Query mit ID Y**:
 * *src/benchmark/queries/*: Hier werden zu jeder Modellierung die verfügbaren Queries gespeichert. Bei einer neuen Query muss in jedem enthaltenen Ordner die Datei *queryY.rq* hinzugefügt werden. Dort muss die SPARQL-Query passend zur jeweiligen Modellierung enthalten sein.
 * Optional: In *\_\_main\_\_.py* kann die ID Y hinzugefügt werden, um beim Standardwert auch die neue Queries auszuführen. Dazu muss lediglich `str(Y)` in die Liste `all_query_ids` in Zeile 22 eingefügt werden.