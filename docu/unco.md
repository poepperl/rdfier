# Table of Contents

* [unco](#unco)
* [unco.data.afe\_mapping\_pipeline](#unco.data.afe_mapping_pipeline)
  * [replace\_unreadable\_chars](#unco.data.afe_mapping_pipeline.replace_unreadable_chars)
  * [change\_afe\_coin\_id](#unco.data.afe_mapping_pipeline.change_afe_coin_id)
  * [change\_findspot](#unco.data.afe_mapping_pipeline.change_findspot)
  * [turn\_nomisma\_values\_to\_uris](#unco.data.afe_mapping_pipeline.turn_nomisma_values_to_uris)
  * [combine\_mint\_and\_denomination](#unco.data.afe_mapping_pipeline.combine_mint_and_denomination)
  * [simplify\_all\_id\_columns](#unco.data.afe_mapping_pipeline.simplify_all_id_columns)
  * [remove\_wrong\_context\_from\_obverse](#unco.data.afe_mapping_pipeline.remove_wrong_context_from_obverse)
  * [remove\_wrong\_context\_from\_reverse](#unco.data.afe_mapping_pipeline.remove_wrong_context_from_reverse)
  * [change\_gyear\_format](#unco.data.afe_mapping_pipeline.change_gyear_format)
  * [replace\_uncertainties\_with\_random\_certainties](#unco.data.afe_mapping_pipeline.replace_uncertainties_with_random_certainties)
  * [remove\_datetime](#unco.data.afe_mapping_pipeline.remove_datetime)
  * [remove\_uncertainties](#unco.data.afe_mapping_pipeline.remove_uncertainties)
  * [remove\_corrosion\_legend\_without\_obreverse](#unco.data.afe_mapping_pipeline.remove_corrosion_legend_without_obreverse)
  * [create\_synthetic\_afe](#unco.data.afe_mapping_pipeline.create_synthetic_afe)
  * [run\_pipeline\_on\_dataframe](#unco.data.afe_mapping_pipeline.run_pipeline_on_dataframe)
* [unco.data.analysis](#unco.data.analysis)
* [unco.data.rdf\_data](#unco.data.rdf_data)
  * [RDFData](#unco.data.rdf_data.RDFData)
    * [\_\_init\_\_](#unco.data.rdf_data.RDFData.__init__)
    * [data\_optimize](#unco.data.rdf_data.RDFData.data_optimize)
* [unco.data.uncertainty\_generator](#unco.data.uncertainty_generator)
  * [UncertaintyGenerator](#unco.data.uncertainty_generator.UncertaintyGenerator)
    * [add\_pseudorand\_uncertainty\_flags](#unco.data.uncertainty_generator.UncertaintyGenerator.add_pseudorand_uncertainty_flags)
    * [add\_pseudorand\_alternatives](#unco.data.uncertainty_generator.UncertaintyGenerator.add_pseudorand_alternatives)
* [unco.data](#unco.data)
* [unco.features.fuseki](#unco.features.fuseki)
  * [FusekiServer](#unco.features.fuseki.FusekiServer)
    * [\_\_init\_\_](#unco.features.fuseki.FusekiServer.__init__)
    * [start\_server](#unco.features.fuseki.FusekiServer.start_server)
    * [upload\_data](#unco.features.fuseki.FusekiServer.upload_data)
    * [delete\_graph](#unco.features.fuseki.FusekiServer.delete_graph)
    * [run\_query](#unco.features.fuseki.FusekiServer.run_query)
    * [stop\_server](#unco.features.fuseki.FusekiServer.stop_server)
* [unco.features.graph\_generator](#unco.features.graph_generator)
  * [GraphGenerator](#unco.features.graph_generator.GraphGenerator)
    * [\_\_init\_\_](#unco.features.graph_generator.GraphGenerator.__init__)
    * [load\_prefixes](#unco.features.graph_generator.GraphGenerator.load_prefixes)
    * [generate\_solution](#unco.features.graph_generator.GraphGenerator.generate_solution)
    * [run\_query](#unco.features.graph_generator.GraphGenerator.run_query)
    * [change\_to\_model\_9a](#unco.features.graph_generator.GraphGenerator.change_to_model_9a)
    * [change\_to\_model\_9b](#unco.features.graph_generator.GraphGenerator.change_to_model_9b)
* [unco.features.illustrator](#unco.features.illustrator)
  * [Illustrator](#unco.features.illustrator.Illustrator)
    * [\_\_init\_\_](#unco.features.illustrator.Illustrator.__init__)
    * [get\_illustration](#unco.features.illustrator.Illustrator.get_illustration)
* [unco.features](#unco.features)
* [unco.run](#unco.run)

<a id="unco"></a>

# unco

<a id="unco.data.afe_mapping_pipeline"></a>

# unco.data.afe\_mapping\_pipeline

<a id="unco.data.afe_mapping_pipeline.replace_unreadable_chars"></a>

#### replace\_unreadable\_chars

```python
def replace_unreadable_chars(dataframe: pd.DataFrame) -> pd.DataFrame
```

Replaces all uft-8 unreadable characters.

**Arguments**:

  -----------
  dataframe : pd.DataFrame
  Dataframe which should be updated

<a id="unco.data.afe_mapping_pipeline.change_afe_coin_id"></a>

#### change\_afe\_coin\_id

```python
def change_afe_coin_id(dataframe: pd.DataFrame) -> pd.DataFrame
```

Turns the ids in column "Coin^^uri" into "afe:"+str(id)

**Arguments**:

  -----------
  dataframe : pd.DataFrame
  Dataframe which should be updated

<a id="unco.data.afe_mapping_pipeline.change_findspot"></a>

#### change\_findspot

```python
def change_findspot(dataframe: pd.DataFrame) -> pd.DataFrame
```

Turns the urls in column "nmo:hasFindspot^^uri" into "gaz:"+str(id)

**Arguments**:

  -----------
  dataframe : pd.DataFrame
  Dataframe which should be updated

<a id="unco.data.afe_mapping_pipeline.turn_nomisma_values_to_uris"></a>

#### turn\_nomisma\_values\_to\_uris

```python
def turn_nomisma_values_to_uris(dataframe: pd.DataFrame) -> pd.DataFrame
```

Turns the values in nomisma columns "nm:"+str(value)

**Arguments**:

  -----------
  dataframe : pd.DataFrame
  Dataframe which should be updated

<a id="unco.data.afe_mapping_pipeline.combine_mint_and_denomination"></a>

#### combine\_mint\_and\_denomination

```python
def combine_mint_and_denomination(dataframe: pd.DataFrame) -> pd.DataFrame
```

Combines the two mint and denomination columns.

**Arguments**:

  -----------
  dataframe : pd.DataFrame
  Dataframe which should be updated

<a id="unco.data.afe_mapping_pipeline.simplify_all_id_columns"></a>

#### simplify\_all\_id\_columns

```python
def simplify_all_id_columns(dataframe: pd.DataFrame) -> pd.DataFrame
```

All id values will be replaced with "1".

**Arguments**:

  -----------
  dataframe : pd.DataFrame
  Dataframe which should be updated

<a id="unco.data.afe_mapping_pipeline.remove_wrong_context_from_obverse"></a>

#### remove\_wrong\_context\_from\_obverse

```python
def remove_wrong_context_from_obverse(dataframe: pd.DataFrame) -> pd.DataFrame
```

Removes reverse context from obverse.

**Arguments**:

  -----------
  dataframe : pd.DataFrame
  Dataframe which should be updated

<a id="unco.data.afe_mapping_pipeline.remove_wrong_context_from_reverse"></a>

#### remove\_wrong\_context\_from\_reverse

```python
def remove_wrong_context_from_reverse(dataframe: pd.DataFrame) -> pd.DataFrame
```

Removes obverse context from reverse.

**Arguments**:

  -----------
  dataframe : pd.DataFrame
  Dataframe which should be updated

<a id="unco.data.afe_mapping_pipeline.change_gyear_format"></a>

#### change\_gyear\_format

```python
def change_gyear_format(dataframe: pd.DataFrame) -> pd.DataFrame
```

Takes float entries of gyear columns and change them to int.

**Arguments**:

  -----------
  dataframe : pd.DataFrame
  Dataframe which should be updated

<a id="unco.data.afe_mapping_pipeline.replace_uncertainties_with_random_certainties"></a>

#### replace\_uncertainties\_with\_random\_certainties

```python
def replace_uncertainties_with_random_certainties(
        dataframe: pd.DataFrame) -> pd.DataFrame
```

Replaces all not-null-entries in the columns with "^^certainty" with pseudo random values between 0 and 1.

**Arguments**:

  -----------
  dataframe : pd.DataFrame
  Dataframe which should be updated

<a id="unco.data.afe_mapping_pipeline.remove_datetime"></a>

#### remove\_datetime

```python
def remove_datetime(dataframe: pd.DataFrame) -> pd.DataFrame
```

Remove all columns with "^^xsd:gYear".

**Arguments**:

  -----------
  dataframe : pd.DataFrame
  Dataframe which should be updated

<a id="unco.data.afe_mapping_pipeline.remove_uncertainties"></a>

#### remove\_uncertainties

```python
def remove_uncertainties(dataframe: pd.DataFrame) -> pd.DataFrame
```

Remove all columns with "^^certainty".

**Arguments**:

  -----------
  dataframe : pd.DataFrame
  Dataframe which should be updated

<a id="unco.data.afe_mapping_pipeline.remove_corrosion_legend_without_obreverse"></a>

#### remove\_corrosion\_legend\_without\_obreverse

```python
def remove_corrosion_legend_without_obreverse(
        dataframe: pd.DataFrame) -> pd.DataFrame
```

Remove all corrosions and legends, without a ob- or reverse.

**Arguments**:

  -----------
  dataframe : pd.DataFrame
  Dataframe which should be updated

<a id="unco.data.afe_mapping_pipeline.create_synthetic_afe"></a>

#### create\_synthetic\_afe

```python
def create_synthetic_afe(dataframe: pd.DataFrame, size: int) -> None
```

Takes the afe dataframe and size, and creates a new dataframe with new entries.

**Arguments**:

  -----------
  dataframe : pd.DataFrame
  Dataframe which should be used to generate the syntetic dataframe
  size : int
  Number of rows of the new dataframe

<a id="unco.data.afe_mapping_pipeline.run_pipeline_on_dataframe"></a>

#### run\_pipeline\_on\_dataframe

```python
def run_pipeline_on_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame
```

Takes float entries of gyear columns and change them to int.

**Arguments**:

  -----------
  dataframe : pd.DataFrame
  Dataframe which should be updated

<a id="unco.data.analysis"></a>

# unco.data.analysis

<a id="unco.data.rdf_data"></a>

# unco.data.rdf\_data

<a id="unco.data.rdf_data.RDFData"></a>

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

<a id="unco.data.rdf_data.RDFData.__init__"></a>

#### \_\_init\_\_

```python
def __init__(dataframe: pd.DataFrame) -> None
```

Parameters
----------
dataframe : pd.DataFrame
    Dataframe of the data which gets pseudorandom uncertainty.

<a id="unco.data.rdf_data.RDFData.data_optimize"></a>

#### data\_optimize

```python
def data_optimize(dataframe: pd.DataFrame, object_option=True)
```

Reduce the size of the input dataframe

Parameters
----------
df: pd.DataFrame
    Input dataframe which should get smaller.
object_option: bool
    If true, try to convert object to category.

<a id="unco.data.uncertainty_generator"></a>

# unco.data.uncertainty\_generator

<a id="unco.data.uncertainty_generator.UncertaintyGenerator"></a>

## UncertaintyGenerator Objects

```python
class UncertaintyGenerator()
```

Class which generates pseudorandom uncertainty for a RDFData.

Attributes
----------
rdfdata : RDFData
    The RDFData, which should get the uncertainties.

<a id="unco.data.uncertainty_generator.UncertaintyGenerator.add_pseudorand_uncertainty_flags"></a>

#### add\_pseudorand\_uncertainty\_flags

```python
def add_pseudorand_uncertainty_flags(
        list_of_columns=None,
        min_uncertainties_per_column: int = 0,
        max_uncertainties_per_column: int = 2) -> RDFData
```

Method to create random uncertainty flags.

Parameters
----------
list_of_columns: list[int]
    List of columns which should get uncertainty flags.
min_uncertainties_per_column: int
    Minimal number of uncertainties each column.
max_uncertainties_per_column: int
    Maximal number of uncertainties each column.

<a id="unco.data.uncertainty_generator.UncertaintyGenerator.add_pseudorand_alternatives"></a>

#### add\_pseudorand\_alternatives

```python
def add_pseudorand_alternatives(
        list_of_columns=None,
        min_number_of_alternatives: int = 1,
        max_number_of_alternatives: int = 3) -> RDFData
```

Method to add alternatives to the existing uncertainty flags.

Parameters
----------
min_number_of_alternatives : int
    The least number of alternatives, which should be added to every uncertainty flag. Has to be 1 or higher.
max_number_of_alternatives : int
    The largest number of alternatives, which should be added to every uncertainty flag. Has to be 1 or higher.
    If there is an entry which has already more then the maximum, this method has no effect on this entry.
list_of_columns: list[int]
    List of columns which should get alternatives. If no columns are choosen, every column will be processed.

<a id="unco.data"></a>

# unco.data

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

<a id="unco.features.illustrator"></a>

# unco.features.illustrator

<a id="unco.features.illustrator.Illustrator"></a>

## Illustrator Objects

```python
class Illustrator()
```

Class which gets a graphical version of a generated rdf file.

Attributes
----------
path : Path
    Path to the rdf data which should get a graphical version.

<a id="unco.features.illustrator.Illustrator.__init__"></a>

#### \_\_init\_\_

```python
def __init__(path: str | Path) -> None
```

Parameters
----------
path : str | Path
    Path to the rdf file.

<a id="unco.features.illustrator.Illustrator.get_illustration"></a>

#### get\_illustration

```python
def get_illustration(path: str | Path)
```

Method, which downloads the graphical version of the given rdf graph. Output will be saved in "data/output/downloaded_graph.png".

Attributes
----------
path : Path
    Path to the rdf data which should get a graphical version.

<a id="unco.features"></a>

# unco.features

<a id="unco.run"></a>

# unco.run

