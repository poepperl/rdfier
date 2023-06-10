#!/bin/bash

FUSEKI_HOME="/pfad/zum/fuseki-server"

PORT="3030"

CONFIG_FILE="config.ttl"

JAVA_HOME="/home/luca/Downloads/jre1.8.0_371/bin"

# Wechsle zum Fuseki-Verzeichnis
cd "/home/luca/Dokumente/repositories/unco/src/fuseki"

# Starte den Fuseki-Server im Hintergrund
./fuseki-server &

echo "Fuseki-Server wurde gestartet. Überprüfen Sie http://localhost:$PORT, um auf die Benutzeroberfläche zuzugreifen."
