from fileinput import filename
from pathlib import Path
from unco import UNCO_PATH
from colorama import Fore
import shutil
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
        """
            Method, which downloads the graphical version of the given rdf graph. Output will be saved in "data/output/downloaded_graph.png".
        """
        data = open(path, 'r', encoding='utf-8').read()
        params = {"rdf": data, "to": "png"}
        path = str(path)

        if path[-3:] == "rdf" or path[-3:] == "xml" or path[-3:] == "txt":
            params["from"] = "xml"
        elif path[-3:] == "ttl":
            params["from"] = "ttl"
        else:
            print(Fore.RED + "ERROR: Unknown Datatyp. Please use \".rdf\" or \".ttl\" files as input." + Fore.RESET)
            return
        response = requests.post('https://www.ldf.fi/service/rdf-grapher', params=params, stream=True)

        filename = str(Path(UNCO_PATH,"data/output/downloaded_graph.png"))
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                shutil.copyfileobj(response.raw, f)

if __name__ == "__main__":
    g = Grapher(Path(r"D:\Dokumente\Repositories\unco\data\output\graph_model_7.rdf"))