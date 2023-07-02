Eingabeformat
=============
Die Hauptaufgabe des RDFiers ist es, aus einem Datenset in Form einer csv-Datei, einen RDF-Graph zu bauen. Da komplexere Konzepte in RDF-Graphen nicht ohne Weiteres aus einem beliebigen Format gelesen werden können, wird hier beschrieben wie solche in der Eingabe codiert werden können.

Grundstruktur
-------------
Die Grundstruktur der Eingabe ist folgende:
<img src="images/basic_structure.JPG" alt="basic_structure" width="1000"/>

Somit bezeichnet üblicherweise die erste Spalte Subjekte und die darauf folgenden Spalten Objekte mit dem jeweiligen Prädikat im Spaltennamen. Aus dem Schaubild enstehen somit die RDF-Aussagen (subject, predicate1, object1), (subject, predicate2, object2) und (subject, predicate3, object3).

Häufig verwendete Namensräume stehen dabei direkt zu Verfügung. Dazu gehören:
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

Weitere Namensräume lassen sich mit einer csv-Tabelle mit den gleichen Spalten hinzufügen oder die oben definierten überschreiben.

URI's, Literale und leere Knoten
--------------------------------
RDF-Graphen besitzen Ressourcen in Form von URI's, Literalen und leeren Knoten. Damit ein Zelleneintrag richtig interpretiert wird, muss zusätzlich zu dem Wert auch der Typ der Ressource angegeben werden. Die folgenden Einträge sind möglich, wobei die Werte in geschwungenen Klammern `{}` durch die erwünschten Werte ersetzt werden müssen.
 * `<{URI}>^^uri` zum Angeben einer vollständigen URI, wie z.B.: "<http://nomisma.org/id/rome>^^uri".
 * `{prefix}:{label}^^uri` zum Angeben einer abgekürzten URI, wie z.B.: "nm:rome^^uri".
 * `{value}` bzw. `{value}^^xsd:string` zum Angeben eines Literals, wie z.B. "2023".
 * `{name}^^blank` zum Angeben eines leeren Knotens. Der Wert von *name* hat dabei keine Bedeutung und wird intern verworfen.

Somit wird der Marker "^^" dazu verwendet den Typ der Ressource anzugeben. Prädikate müssen vom Typ URI sein, weshalb der Marker im Spaltennamen keinen Einfluss auf den Typ des Prädikats hat. Stattdessen kann der Marker an dieser Stelle als Typzuweisung für alle Einträge der Spalte ohne eigenen Typ genutzt werden.

**Beispiel**:
|coins^^uri|nmo:hasMaterial^^uri      |
|:---      |:---                      |
|afe:5     |nm:ar                     |
|afe:13    |kryptonite^^blank         |
|afe:29    |<http://nomisma.org/id/ae>|

Das Stichwort `coin` ist im Spaltennamen der ersten Spalte der Subjekte und definiert somit kein Prädikat, es wird vom Programm verworfen und hat keine Auswirkungen.
Die beiden `^^uri` Marker weisen allen Einträgen in ihren Spalten den Typ URI zu, wenn diese keinen eigenen Typ haben. Daher werden die Einträge `nm:ar` und `<http://nomisma.org/id/ae>` als URI gelesen.
Da es für Kryptonit keine URI im Namensraum *nm* gibt, wird diese durch einen leeren Knoten realisiert, indem `^^blank` als Marker genutzt wird. Der Eintrag `kryptonite` hat dabei keinen Einfluss und wird vom Programm verworfen.


Datentypen und Sprachen
-----------------------
Zu Literalen lassen sich in RDF-Graphen Datentypen und Sprachen zuordnen. Daher braucht es eine Möglichkeit diese in der Eingabe zu kennzeichnen.
Hier kann die gleiche Syntax genutzt werden wie im Turtle-Format:
 * `literal^^{URI_of_datatype}` zum Angeben eines Datentyps.
 * `literal@{country ISO code}` zum Angeben einer Sprache.

Da nur Literale Datentypen und Sprachen besitzen können, wird keine zusätzliche Typ Markierung benötigt. Somit werden Einträge der Form *value^^URI* immer als Literal mit Datentyp interpretiert. Die URI kann dabei wie oben bereits beschrieben durch eine vollständige URI `<{URI}>` oder eine abgekürzte URI `{prefix}:{label}` angegeben werden.
Eine Sprache lässt sich durch eine zweistellige ISO Kennzeichnung angeben. Eine Liste mit allen Länder Codes lässt sich [hier](https://en.wikipedia.org/wiki/ISO_3166-1#Current_codes) finden.
Ähnlich zu den Ressourcen Typen, lassen sich auch diese Marker in den Spaltenkopf verschieben, um allen Einträgen ohne Ressourcentyp, Datentyp und Sprachen einen Wert zuzuordnen.

**Beispiel**:
|coins^^uri|nmo:hasMaterial^^uri      |nmo:hasWeight^^xsd:decimal|
|:---      |:---                      |:---                      |
|afe:5     |nm:ar                     |5.24                      |
|afe:13    |kryptonite^^blank         |too heavy to weigh@en     |
|afe:29    |<http://nomisma.org/id/ae>|1.16                      |


Mehrfacheinträge
----------------
Häufig besitzen RDF-Aussagen das gleiche Subjekt-Prädikat-Paar. Für die Eingabe bedeutet das, dass sich beide Aussagen auf die selbe Zelle der CSV beziehen können.
Aus diesem Grund lassen sich in die Zellen mit Objekten auch Mehrfacheinträge getrennt durch ein Semikolon `;` erstellen. So lässt sich leicht für das obige Beispiel der Text in einer zweiten Sprache angeben: `too heavy to weigh@en; zu schwer zum wiegen@de`.


Verkettete Aussagen
-------------------
Um auch Aussagen darstellen zu können wie "A ist mit B befreundet und B hat den Namen Luca", lässt sich die oben gezeigte Grundstruktur verändern.
Durch den Marker `**{id}` am Ende des Spaltennamens lässt sich einer Spalte eine ID zuordnen und somit als Subjekt-Spalte markieren.
Die ID darf dabei eine beliebige Zeichekette sein.
Auf eine Subjekt-Spalte mit ID kann dann mit dem Marker `{id}__` (doppelter Unterstrich) am Anfang eines Spaltennamens referenziert werden, sodass die Spalte Objekte und das Prädikat zur referenzierten Subjekt-Spalte enthält. Für unser Beispiel sieht das wie Folgt aus:

|coins^^uri|nmo:hasMaterial^^uri**1   |nmo:hasWeight^^xsd:decimal|1__rdf:value               |
|:---      |:---                      |:---                      |:---                       |
|afe:5     |nm:ar                     |5.24                      |                           |
|afe:13    |kryptonite^^blank         |too heavy to weigh@en     |kryptonite@en; Kryptonit@de|
|afe:29    |<http://nomisma.org/id/ae>|1.16                      |                           |

Durch diese Veränderung wird die zweite Spalte nun zusätzlich als Subjekt-Spalte interpretiert und die vierte Spalte enthält die dazu gehörenden Objekte und das Prädikat. Dadurch entstehen zwei neue Kanten vom leeren Knoten ausgehend mit dem Prädikat `rdf:value` und den beiden Objekten `kryptonite` und `Kryptonit`.
Durch die Zuweisung bleiben die ursprünglichen RDF-Aussagen unbetroffen.
Auch lässt sich eine Spalte, die auf eine andere Subjekt-Spalte referenziert wiederrum eine ID zuweisen, usw.


Unsichere Aussagen
------------------
Auch die Angabe von unsicheren Aussagen, lassen sich in der Eingabe vermerken.
Dazu wird der Spalte der Aussage wie oben beschrieben eine ID zugewiesen, auf die verwiesen werden kann und mit dem Marker `^^certainty` am Ende des Spaltennamens kann den Aussagen eine Unsicherheit zugewiesen werden.
Wichtig ist hierbei, dass die Zuweisung der Unsicherheit zellenweise erfolgt und alle Mehrfacheinträge dann als Unsicherheit mit Alternativen gewertet werden.
Fügen wir unserem Beispiel Unsicherheiten hinzu:

|coins^^uri|nmo:hasMaterial^^uri**1   |nmo:hasWeight^^xsd:decimal|1__rdf:value               |uncertainMaterial^^certainty|
|:---      |:---                      |:---                      |:---                       |:---                        |
|afe:5     |nm:ar; nm:billon          |5.24                      |                           |0.8; 0.2                    |
|afe:13    |kryptonite^^blank         |too heavy to weigh@en     |kryptonite@en; Kryptonit@de|u                           |
|afe:29    |<http://nomisma.org/id/ae>|1.16                      |                           |                            |

Hier wurden manchen RDF-Aussagen der Form *afe:ID nmo:hasMaterial {object}* als unsicher markiert.
Mit dem Eintrag `u` wurde lediglich beschrieben, dass es unsicher ist, dass die Münze `afe:13` aus Kryptonit besteht.
Da für den Eintrag `nm:ar; nm:billon` eine Unsicherheit eingetragen wurde, werden die beiden Werte als Alternativen betrachtet.
Die Einträge `0.8; 0.2` sind gewichtete Unsicherheiten. Somit ist die Aussage *afe:13 nmo:hasMaterial nm:ar* unsicher mit der Gewichtung `0.8` und die Aussage *afe:13 nmo:hasMaterial nm:billon* unsicher mit der Gewichtung `0.2`.

Für die Angabe der Unsicherheit gelten Folgende Einschränkungen:
 * Einfache Einträge können mit `u` als unsicher vermerkt werden. Stattdessen kann auch eine einzelne Gewichtung angegeben werden. Die Gewichtung 0 bedeutet in diesem Zusammenhang "vollkommen unsicher" und die Gewichtung "1" ist gleichbedeutend zu "sicher".
 * Mehrfacheinträge lassen sich durch `a` (für *alternatives*) als Unsicherheit mit Alternativen kennzeichnen. Stattdessen kann auch eine Gewichtung angegeben werden, wobei zu jeder Alternative eine Gewichtung erhalten muss.