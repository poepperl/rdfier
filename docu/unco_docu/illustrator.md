# Table of Contents

* [unco.features.illustrator](#unco.features.illustrator)
  * [Illustrator](#unco.features.illustrator.Illustrator)
    * [\_\_init\_\_](#unco.features.illustrator.Illustrator.__init__)
    * [get\_illustration](#unco.features.illustrator.Illustrator.get_illustration)

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

