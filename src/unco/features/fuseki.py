import subprocess
import psutil
import time
import requests
import pandas as pd
import os
from io import StringIO
from pathlib import Path
from unco import UNCO_PATH


class FusekiServer:
    """
    Interface to the fuseki server.

    Attributes
    ----------
    FUSEKI_PATH: str
        Path to the fuseki server folder.
    server: subprocess.Popen
        Server instance, if the fuseki server is running.
    """

    def __init__(self, fuseki_path: str | Path = Path(UNCO_PATH, "src/apache-jena-fuseki-4.8.0")) -> None:
        """
        Parameters
        ----------
        fuseki_path: str | Path
            Path to the fuseki server folder.
        """
        self.FUSEKI_PATH = str(fuseki_path)
        self.server = None

        self._initialize()

    def _initialize(self) -> None:
        """
            Method, which creates the server_starter.bat which starts the fuseki server.
        """
        starter_path = str(Path(UNCO_PATH, "src/unco/features/server_starter"))
        if os.name == "nt":
            starter_path += ".bat"
            with open(starter_path, 'w') as starter:
                starter.write(f"echo 'Running fuseki server'\n{self.FUSEKI_PATH[:2]}\ncd \"" + self.FUSEKI_PATH + "\"\n")
                starter.write("java -Xmx4G -jar \"fuseki-server.jar\" --update --mem /ds %*")
        elif os.name == "posix":
            starter_path += ".sh"
            with open(starter_path, 'w') as starter:
                starter.write(f'FUSEKI_HOME="{self.FUSEKI_PATH}" \nPORT="3030" \ncd "{self.FUSEKI_PATH}" \njava -Xmx4G -jar fuseki-server.jar --update --mem /ds &')
            
            os.system(f"chmod u=rwx,g=r,o=r {starter_path}")
        else:
            print(f"Unknown system{os.name}. Please contact the admin.")

    def start_server(self) -> None:
        """
            Method, which starts the fuseki server.
        """
        if os.name == "nt":
            if self.server:
                raise RuntimeError("Server is already running.")
            else:
                self.server = subprocess.Popen(str(Path(UNCO_PATH, "src/unco/features/server_starter.bat")), creationflags=subprocess.CREATE_NEW_CONSOLE, start_new_session=True)
                time.sleep(2)
        elif os.name == "posix":
            if self.server:
                raise RuntimeError("Server is already running.")
            else:
                self.server = subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', f'cd {str(Path(UNCO_PATH, "src/unco/features"))}; ./server_starter.sh; bash'], stdout=subprocess.PIPE, preexec_fn=os.setsid)
                time.sleep(2)
        else:
            print(f"Unknown system{os.name}. Please contact the admin. Notice: the benchmark is currently not aviable for Mac users.")
    
    def upload_data(self, path: str) -> None:
        """
            Method, which uploads data in rdf or turtle files to the server

        Parameters
        ----------
        path: str
            Path to the file that should be uploaded.
        """
        if self.server is None:
            raise RuntimeError("Server is shut down. Please start the server.")
        if path[-3:] == "rdf" or path[-3:] == "xml" or path[-3:] == "txt":
            headers = {'Content-Type': r'application/rdf+xml;charset=utf-8', 'Filename' : path}
        elif path[-3:] == "ttl":
            headers = {'Content-Type': r'text/turtle;charset=utf-8'}
        else:
            raise ValueError("Unknown Datatype. Please use \".rdf\" or \".ttl\" files as input.")
        data = open(path, 'r', encoding='latin1').read()
        requests.post('http://localhost:3030/ds/data', data=data.encode('utf-8'), headers=headers)

    def delete_graph(self) -> None:
        """
            Method, which deletes the current graph ds.
        """  
        sparql_query = """
        DELETE WHERE {
            ?s ?p ?o
        }
        """
        requests.post(f"http://localhost:3030/ds/update", headers={"Content-Type": "application/sparql-update"}, data=sparql_query)

    def run_query(self, query: str, save_result : bool = True) -> pd.DataFrame | None:
        """
        Method, which runs a given SPARQL query on the fuseki server and outputs the result in json format.

        Parameter
        ---------
        query: str
            String of the hole query.
        save_result: bool
            If True, the method saves the result in data/output/query_results_fuseki.csv.
        """
        headers = {"Accept": "text/csv"}
        params = {"query": query}
        response = requests.get('http://localhost:3030/ds/query', params=params, headers=headers)

        result = StringIO(response.text)

        if save_result:
            csvdata = pd.read_csv(result, encoding='utf-8')
            csvdata.to_csv(str(Path(UNCO_PATH, "data/output/query_results_fuseki.csv")))
            return csvdata

    def stop_server(self) -> None:
        """
            Method, which stops the fuseki server.
        """
        if os.name == "nt":
            if self.server:
                for child in psutil.Process(self.server.pid).children():
                    child.kill()
                self.server = None
            else:
                raise RuntimeError("Server is already stopped.")
        elif os.name == "posix":
            subprocess.call(['pkill', 'gnome-terminal'])
            self.server = None
        else:
            print(f"Unknown system{os.name}. Please contact the admin.")
