echo 'Running fuseki server'
cd "d:\dokumente\repositories\unco\src\fuseki"
java -Xmx8200M -jar "fuseki-server.jar" --update --mem /ds %*