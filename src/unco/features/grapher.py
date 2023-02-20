from pathlib import Path
import requests

class Grapher():
    """
        Class which gets a graphical version of a generated rdf file.

    Attributes
    ----------
    
    """

    def __init__(self, path: str | Path) -> None:
        """
        Parameters
        ----------
        path : str | Path
            Path to the rdf file.
        """
        self.path = path
        self.get_illustration(path)
    

    def get_illustration(self, path : str | Path):
        # data = open(path, 'r', encoding='utf-8').read()
        headers = {"rdf": '''<?xml version="1.0" encoding="utf-8"?>
<rdf:RDF
   xmlns:nmo="http://nomisma.org/ontology#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:un="http://www.w3.org/2005/Incubator/urw3/XGRurw3-20080331/Uncertainty.owl"
>
  <rdf:Description rdf:nodeID="nmohasMintnmcomama">
    <un:hasUncertainty rdf:resource="http://nomisma.org/id/uncertain_value"/>
    <rdf:value rdf:resource="http://nomisma.org/id/comama"/>
  </rdf:Description>
  <rdf:Description rdf:nodeID="icoin_1c0">
    <nmo:hasMint rdf:nodeID="nmohasMintnmcomama"/>
  </rdf:Description>
  <rdf:Description rdf:nodeID="icoin_2c0">
    <nmo:hasMint rdf:resource="http://nomisma.org/id/comama"/>
  </rdf:Description>
  <rdf:Description rdf:nodeID="icoin_0c0">
    <nmo:hasMint rdf:nodeID="nmohasMintnmcomama"/>
  </rdf:Description>
</rdf:RDF>''', "from": "xml", "to": "png"}
        response = requests.post('https://www.ldf.fi/service/rdf-grapher', headers=headers)
        print(response.text)

if __name__ == "__main__":
    g = Grapher("")