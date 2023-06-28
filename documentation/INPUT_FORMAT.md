INPUT FORMAT
============
Die Hauptaufgabe des RDFiers ist es, aus einem Datenset in Form einer csv-Datei, einen RDF-Graph zu bauen. Da komplexere Konzepte in RDF-Graphen nicht ohne weiteres aus einer csv-Tabelle gelesen werden können, wird hier beschrieben wie diese in der Eingabe codiert werden können.

Grundstruktur
-------------
Die Grundstruktur der Eingabe ist folgende:
BILD EINFÜGEN

Somit bezeichnet üblicherweise die erste Spalte Subjekte und die darauf folgenden Spalten Objekte mit dem jeweiligen Prädikat im Spaltenkopf. Aus dem Schaubild erstehen somit die Kanten (ex:subject1, ex:predicate1, ex:object1), (ex:subject1, ex:predicate2, ex:object2) und (ex:subject1, ex:predicate3, ex:object3).

Manche Namensräume müssen nicht selbst eingefügt werden, sondern stehen bereits zur Verfügung. Dazu gehören:
|prefix  |namespace                                                               |
|:---    |:---                                                                    |
|amt     |http://academic-meta-tool.xyz/vocab#                                    |
|bmo     |http://collection.britishmuseum.org/id/ontology/                        |
|crm     |http://www.cidoc-crm.org/cidoc-crm/                                     |
|crminf  |http://www.cidoc-crm.org/crminf/sites/default/files/CRMinf_v0.7_.rdfs#  |
|dcterms |http://purl.org/dc/terms/                                               |
|dcmitype|http://purl.org/dc/dcmitype/                                            |
|edtfo   |http://periodo.github.io/edtf-ontology/edtfo.ttl#                       |
|foaf    |http://xmlns.com/foaf/0.1/                                              |
|geo     |http://www.w3.org/2003/01/geo/wgs84_pos#                                |
|nm      |http://nomisma.org/id/                                                  |
|nmo     |http://nomisma.org/ontology#                                            |
|org     |http://www.w3.org/ns/org#                                               |
|rdf     |http://www.w3.org/1999/02/22-rdf-syntax-ns#                             |
|rdfs    |http://www.w3.org/2000/01/rdf-schema#                                   |
|skos    |http://www.w3.org/2004/02/skos/core#                                    |
|un      |http://www.w3.org/2005/Incubator/urw3/XGR-urw3-20080331/Uncertainty.owl#|
|xsd     |http://www.w3.org/2001/XMLSchema#                                       |

Weitere Namensräume lassen sich mit einer csv-Tabelle mit der gleichen Struktur hinzufügen oder die oben definierten überschreiben.

URI's, literals and blank nodes
-------------------------------
RDF-Graphen besitzt Ressourcen in Form von URI's, Literalen und leeren Knoten. Damit ein Zelleneintrag richtig interpretiert wird, muss zusätzlich zu dem Wert auch der Typ der Ressource angegeben werden. Die folgenden Einträge sind möglich, wobei die in geschwungenen Klammern `{}` Werte Platzhalter sind.
 * `<{URI}>^^uri` zum Angeben einer vollständigen URI, wie z.B.: "<http://nomisma.org/id/rome>^^uri"
 * `{prefix}:{label}^^uri` zum Angeben einer abgekürzten URI, wie z.B.: "nm:rome^^uri"
 * `{value}` zum Angeben eines Literals, wie z.B. "2023"
 * `{name}^^blank` zum Angeben eines leeren Knotens. Der Wert von *name* hat dabei keine Bedeutung und wird intern verworfen.

> [!hint] Subjekte dürfen müssen vom Typ URI oder leerer Knoten sein und Prädikate müssen vom Typ URI sein.

Datentypen und Sprachen
-----------------------
Da Literale



Verkettete Aussagen
-------------------
Um auch Aussagen darstellen zu können wie "A ist mit B befreundet und B hat den Namen Luke", lässt sich die oben gezeigte Grundstruktur ändern.
