# Table of Contents

* [unco.features.graph\_generator](#unco.features.graph_generator)
  * [GraphGenerator](#unco.features.graph_generator.GraphGenerator)
    * [\_\_init\_\_](#unco.features.graph_generator.GraphGenerator.__init__)
    * [load\_prefixes](#unco.features.graph_generator.GraphGenerator.load_prefixes)
    * [generate\_solution](#unco.features.graph_generator.GraphGenerator.generate_solution)
    * [run\_query](#unco.features.graph_generator.GraphGenerator.run_query)
    * [change\_to\_model\_9a](#unco.features.graph_generator.GraphGenerator.change_to_model_9a)
    * [change\_to\_model\_9b](#unco.features.graph_generator.GraphGenerator.change_to_model_9b)

<a id="unco.features.graph_generator"></a>

# unco.features.graph\_generator

<a id="unco.features.graph_generator.GraphGenerator"></a>

## GraphGenerator Objects

```python
class GraphGenerator()
```

Class which creates an RDF-XML file.

Attributes
----------
rdfdata: RDFData
    RDFData which contains the data of the rdf graph.
graph: Graph
    RDF graph which will be created.
OUTPUT_FOLDER: Path
    Constant which holds the output path.
prefixes: dict
    Dictionary which contains the prefixes and namespaces which binds to the graph.

<a id="unco.features.graph_generator.GraphGenerator.__init__"></a>

#### \_\_init\_\_

```python
def __init__(rdfdata: RDFData) -> None
```

Parameters
----------
rdfdata: RDFData
    Object which contains the data of the rdf graph.

<a id="unco.features.graph_generator.GraphGenerator.load_prefixes"></a>

#### load\_prefixes

```python
def load_prefixes(path_data: str | pd.DataFrame) -> None
```

Loads prefixes of namespaces and bind them to the graph.

Parameters
----------
path_data: str | DataFrame
    Path to the csv file with header: (prefix, namespace) or DataFrame of the file.

<a id="unco.features.graph_generator.GraphGenerator.generate_solution"></a>

#### generate\_solution

```python
def generate_solution(model_id: int = 4, xml_format: bool = True) -> None
```

Generates and saves the RDF graph.

Attributes
----------
model_id: int
    Model ID, of the model which should be used to create the uncertain statements.
xml_format: bool
    If True, the generated graph will be saved in data/output/graph.ttl in turtle format.
    Otherwise it will be saved in data/output/graph.rdf in xml format.

<a id="unco.features.graph_generator.GraphGenerator.run_query"></a>

#### run\_query

```python
def run_query(query: str, save_result: bool = True) -> pd.DataFrame
```

Runs the given query on the generated rdf graph.

Parameters
----------
query: str
    String of the hole query.
save_result: bool
    If True, the method saves the result in data/output/query_results_fuseki.csv.

<a id="unco.features.graph_generator.GraphGenerator.change_to_model_9a"></a>

#### change\_to\_model\_9a

```python
def change_to_model_9a() -> None
```

Creates all rdf* uncertain statements of solution 9a.

<a id="unco.features.graph_generator.GraphGenerator.change_to_model_9b"></a>

#### change\_to\_model\_9b

```python
def change_to_model_9b() -> None
```

Creates all rdf* uncertain statements of solution 9b.

