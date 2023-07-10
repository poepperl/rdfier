# Table of Contents

* [unco.data.rdf\_data](#unco.data.rdf_data)
  * [RDFData](#unco.data.rdf_data.RDFData)
    * [\_\_init\_\_](#unco.data.rdf_data.RDFData.__init__)
    * [data\_optimize](#unco.data.rdf_data.RDFData.data_optimize)

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

