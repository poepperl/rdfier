# Table of Contents

* [unco.features.fuseki](#unco.features.fuseki)
  * [FusekiServer](#unco.features.fuseki.FusekiServer)
    * [\_\_init\_\_](#unco.features.fuseki.FusekiServer.__init__)
    * [start\_server](#unco.features.fuseki.FusekiServer.start_server)
    * [upload\_data](#unco.features.fuseki.FusekiServer.upload_data)
    * [delete\_graph](#unco.features.fuseki.FusekiServer.delete_graph)
    * [run\_query](#unco.features.fuseki.FusekiServer.run_query)
    * [stop\_server](#unco.features.fuseki.FusekiServer.stop_server)

<a id="unco.features.fuseki"></a>

# unco.features.fuseki

<a id="unco.features.fuseki.FusekiServer"></a>

## FusekiServer Objects

```python
class FusekiServer()
```

Interface to the fuseki server.

Attributes
----------
FUSEKI_PATH: str
    Path to the fuseki server folder.
server: subprocess.Popen
    Server instance, if the fuseki server is running.

<a id="unco.features.fuseki.FusekiServer.__init__"></a>

#### \_\_init\_\_

```python
def __init__(fuseki_path: str | Path = Path(UNCO_PATH, "src/fuseki")) -> None
```

Parameters
----------
fuseki_path: str | Path
    Path to the fuseki server folder.

<a id="unco.features.fuseki.FusekiServer.start_server"></a>

#### start\_server

```python
def start_server() -> None
```

Method, which starts the fuseki server.

<a id="unco.features.fuseki.FusekiServer.upload_data"></a>

#### upload\_data

```python
def upload_data(path: str) -> None
```

Method, which uploads data in rdf or turtle files to the server

Parameters
----------
path: str
    Path to the file that should be uploaded.

<a id="unco.features.fuseki.FusekiServer.delete_graph"></a>

#### delete\_graph

```python
def delete_graph() -> None
```

Method, which deletes the current graph ds.

<a id="unco.features.fuseki.FusekiServer.run_query"></a>

#### run\_query

```python
def run_query(query: str, save_result: bool = True) -> pd.DataFrame
```

Method, which runs a given SPARQL query on the fuseki server and outputs the result in json format.

Parameter
---------
query: str
    String of the hole query.
save_result: bool
    If True, the method saves the result in data/output/query_results_fuseki.csv.

<a id="unco.features.fuseki.FusekiServer.stop_server"></a>

#### stop\_server

```python
def stop_server() -> None
```

Method, which stops the fuseki server.

