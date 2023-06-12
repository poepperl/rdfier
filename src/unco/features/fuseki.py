import subprocess
import psutil
import time
import requests
import pandas as pd
import os
import signal
from io import StringIO
from pathlib import Path
from unco import UNCO_PATH

OUTPUT_FOLDER  = Path(UNCO_PATH, "data/output")

class FusekiServer:
    """
        Interface to the fuseki server.
    """

    def __init__(self, fuseki_path: str = str(Path(UNCO_PATH, "src/fuseki")), gb_ram: int = 4) -> None:
        """
        Parameters
        ----------
        fuseki_path : str
            Path to the fuseki server folder.
        mb_ram : int
            RAM size in GB for the fuseki server.
        """
        self.FUSEKI_PATH = fuseki_path
        self.GB_RAM = gb_ram
        self.server = None
        self.starter_path : str
        self._initialize()

    def _initialize(self) -> None:
        """
            Method, which creates the server_starter.bat which starts the fuseki server.
        """
        if os.name == "nt":
            self.starter_path = str(Path(UNCO_PATH, "src/unco/features/server_starter.bat"))
            with open(self.starter_path, 'w') as starter:
                starter.write("echo 'Running fuseki server'\ncd \"" + self.FUSEKI_PATH + "\"\n")
                starter.write("java -Xmx" + str(self.GB_RAM) + "G -jar \"fuseki-server.jar\" --update --mem /ds %*")
        elif os.name == "posix":
            self.starter_path = str(Path(UNCO_PATH, "src/unco/features/server_starter.sh"))
            with open(self.starter_path, 'w') as starter:
                starter.write(f'FUSEKI_HOME="{self.FUSEKI_PATH}" \nPORT="3030" \ncd "{self.FUSEKI_PATH}" \n./fuseki-server &')
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
                self.server = subprocess.Popen(self.starter_path, shell=True, start_new_session=True)
                time.sleep(3)
        elif os.name == "posix":
            if self.server:
                raise RuntimeError("Server is already running.")
            else:
                self.server = subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', 'cd /home/luca/Dokumente/repositories/unco/src/unco/features; ./server_starter.sh; bash'], stdout=subprocess.PIPE, preexec_fn=os.setsid)
                time.sleep(3)
        else:
            print(f"Unknown system{os.name}. Please contact the admin.")
    
    def upload_data(self, path: str) -> None:
        """
            Method, which uploads data in rdf or turtle files to the server

        Parameters
        ----------
        path : str
            Path to the file that should be uploaded.
        """
        if self.server == None:
            raise RuntimeError("Server is shut down. Please start the server.")
        if path[-3:] == "rdf" or path[-3:] == "xml" or path[-3:] == "txt":
            headers = {'Content-Type': r'application/rdf+xml;charset=utf-8', 'Filename' : path}
        elif path[-3:] == "ttl":
            headers = {'Content-Type': r'text/turtle;charset=utf-8'}
        else:
            raise ValueError("Unknown Datatyp. Please use \".rdf\" or \".ttl\" files as input.")
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


    def run_query(self, query : str) -> pd.DataFrame:
        """
            Method, which runs a given SPARQL query on the fuseki server and outputs the result in json format.
        """
        headers = {"Accept" : "text/csv"}
        params = {"query" : query}
        response = requests.get('http://localhost:3030/ds/query', params=params, headers=headers)

        csvdata = pd.read_csv(StringIO(response.text), encoding='utf-8')

        csvdata.to_csv(str(Path(OUTPUT_FOLDER, "query_results_fuseki.csv")))

        return pd.DataFrame(csvdata)


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
        else:
            print(f"Unknown system{os.name}. Please contact the admin.")


if __name__ == "__main__":
    f = FusekiServer()
    f.start_server()
    f.upload_data(str(Path(UNCO_PATH,"data/output/graph.ttl")))
    query = """
    PREFIX nmo: <http://nomisma.org/ontology#>
    PREFIX nm: <http://nomisma.org/id/>

    SELECT ?s ?p ?o
    WHERE {
        ?s ?p ?o .
    }
    """
    # SELECT ?s { ?s nmo:hasMint nm:comama }

    # SELECT ?s { <<?s nmo:hasMint nm:comama>> un:hasUncertainty nm:uncertain_value }

    # SELECT ?s { BIND (<<?s nmo:hasMint nm:comama>> AS ?tripel) ?tripel un:hasUncertainty nm:uncertain_value }
    

    print(f.run_query(query))
    time.sleep(20)
    f.stop_server()
    #f.delete_graph()
    #print(f.run_query(query))
    #time.sleep(5)
    #f.stop_server()


    # response = requests.post('http://localhost:3030/ds/sparql', data={'query': 'SELECT * WHERE {?sub ?pred ?obj .} LIMIT 10'})
    # print(response.json())