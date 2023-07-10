# Table of Contents

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

