# Table of Contents

* [unco.data.uncertainty\_generator](#unco.data.uncertainty_generator)
  * [UncertaintyGenerator](#unco.data.uncertainty_generator.UncertaintyGenerator)
    * [add\_pseudorand\_uncertainty\_flags](#unco.data.uncertainty_generator.UncertaintyGenerator.add_pseudorand_uncertainty_flags)
    * [add\_pseudorand\_alternatives](#unco.data.uncertainty_generator.UncertaintyGenerator.add_pseudorand_alternatives)

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

