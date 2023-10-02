# Table of Contents

* [scripts](#scripts)
* [scripts.data.rdf\_data](#scripts.data.rdf_data)
  * [RDFData](#scripts.data.rdf_data.RDFData)
    * [\_\_init\_\_](#scripts.data.rdf_data.RDFData.__init__)
    * [data\_optimize](#scripts.data.rdf_data.RDFData.data_optimize)
* [scripts.data](#scripts.data)
* [scripts.features.graph\_generator](#scripts.features.graph_generator)
  * [GraphGenerator](#scripts.features.graph_generator.GraphGenerator)
    * [\_\_init\_\_](#scripts.features.graph_generator.GraphGenerator.__init__)
    * [load\_prefixes](#scripts.features.graph_generator.GraphGenerator.load_prefixes)
    * [generate\_graph](#scripts.features.graph_generator.GraphGenerator.generate_graph)
    * [run\_query](#scripts.features.graph_generator.GraphGenerator.run_query)
    * [change\_to\_model\_9a](#scripts.features.graph_generator.GraphGenerator.change_to_model_9a)
    * [change\_to\_model\_9b](#scripts.features.graph_generator.GraphGenerator.change_to_model_9b)
* [scripts.features.illustrator](#scripts.features.illustrator)
  * [Illustrator](#scripts.features.illustrator.Illustrator)
    * [\_\_init\_\_](#scripts.features.illustrator.Illustrator.__init__)
    * [get\_illustration](#scripts.features.illustrator.Illustrator.get_illustration)
* [scripts.features](#scripts.features)

<a id="scripts"></a>

# scripts

<a id="scripts.data.rdf_data"></a>

# scripts.data.rdf\_data

<a id="scripts.data.rdf_data.RDFData"></a>

## RDFData Objects

```python
class RDFData()
```

Class that represents the RDF data.

Attributes
----------
data : pd.DataFrame
    Pandas dataframe which includes the data in the defined input format.
triple_plan: dict
    Dictionary to save which columns are interpreted as subjects and their corresponding object columns. 
types_and_languages: dict
    Dictionary to save the datatype or language of a value.
uncertainties: dict
    Dictionary with (row, column) of an uncertain cell as key and the uncertainty as value.

<a id="scripts.data.rdf_data.RDFData.__init__"></a>

#### \_\_init\_\_

```python
def __init__(dataframe: pd.DataFrame) -> None
```

Parameters
----------
dataframe : pd.DataFrame
    Dataframe of the data which gets pseudorandom uncertainty.

<a id="scripts.data.rdf_data.RDFData.data_optimize"></a>

#### data\_optimize

```python
def data_optimize(dataframe: pd.DataFrame, object_option=False)
```

Reduce the size of the input dataframe

Parameters
----------
dataframe: pd.DataFrame
    Input dataframe which should get smaller.
object_option: bool
    If true, try to convert object to category.

<a id="scripts.data"></a>

# scripts.data

<a id="scripts.features.graph_generator"></a>

# scripts.features.graph\_generator

<a id="scripts.features.graph_generator.GraphGenerator"></a>

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

<a id="scripts.features.graph_generator.GraphGenerator.__init__"></a>

#### \_\_init\_\_

```python
def __init__(rdfdata: RDFData) -> None
```

Parameters
----------
rdfdata: RDFData
    Object which contains the data of the rdf graph.

<a id="scripts.features.graph_generator.GraphGenerator.load_prefixes"></a>

#### load\_prefixes

```python
def load_prefixes(path_data: str | pd.DataFrame) -> None
```

Loads prefixes of namespaces and bind them to the graph.

Parameters
----------
path_data: str | DataFrame
    Path to the csv file with header: (prefix, namespace) or DataFrame of the file.

<a id="scripts.features.graph_generator.GraphGenerator.generate_graph"></a>

#### generate\_graph

```python
def generate_graph(model_id: int = 8, xml_format: bool = False) -> None
```

Generates and saves the RDF graph.

Attributes
----------
model_id: int
    Model ID, of the model which should be used to create the uncertain statements.
xml_format: bool
    If True, the generated graph will be saved in data/output/graph.ttl in turtle format.
    Otherwise it will be saved in data/output/graph.rdf in xml format.

<a id="scripts.features.graph_generator.GraphGenerator.run_query"></a>

#### run\_query

```python
def run_query(query: str, save_result: bool = True) -> pd.DataFrame | None
```

Runs the given query on the generated rdf graph.

Parameters
----------
query: str
    String of the hole query.
save_result: bool
    If True, the method saves the result in data/output/query_results_fuseki.csv.

<a id="scripts.features.graph_generator.GraphGenerator.change_to_model_9a"></a>

#### change\_to\_model\_9a

```python
def change_to_model_9a() -> None
```

Creates all rdf* uncertain statements of solution 9a.

<a id="scripts.features.graph_generator.GraphGenerator.change_to_model_9b"></a>

#### change\_to\_model\_9b

```python
def change_to_model_9b() -> None
```

Creates all rdf* uncertain statements of solution 9b.

<a id="scripts.features.illustrator"></a>

# scripts.features.illustrator

<a id="scripts.features.illustrator.Illustrator"></a>

## Illustrator Objects

```python
class Illustrator()
```

Class which gets a graphical version of a generated rdf file.

Attributes
----------
path : Path
    Path to the rdf data which should get a graphical version.

<a id="scripts.features.illustrator.Illustrator.__init__"></a>

#### \_\_init\_\_

```python
def __init__(path: str | Path) -> None
```

Parameters
----------
path : str | Path
    Path to the rdf file.

<a id="scripts.features.illustrator.Illustrator.get_illustration"></a>

#### get\_illustration

```python
def get_illustration(path: str | Path)
```

Method, which downloads the graphical version of the given rdf graph. Output will be saved in "data/output/downloaded_graph.png".

Attributes
----------
path : Path
    Path to the rdf data which should get a graphical version.

<a id="scripts.features"></a>

# scripts.features

