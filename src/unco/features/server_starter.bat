echo 'Running fuseki server'
cd "c:\users\scrum\documents\repositories\unco\src\fuseki"
java -Xmx4G -jar "fuseki-server.jar" --update --mem /ds %*