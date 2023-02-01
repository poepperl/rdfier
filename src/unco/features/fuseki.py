from unco import UNCO_PATH
import os
import subprocess
import psutil
import socket
import time
import requests
from SPARQLWrapper import SPARQLWrapper
from colorama import Fore

class FusekiServer:
    """
        Class that starts a server on which the requests are tested

    Attributes
    ----------
    data : pd.DataFrame
        DataFrame wich includes the data from Reader.
    """

    def __init__(self, fuseki_path: str = os.path.join(UNCO_PATH, r"src\fuseki"), mb_ram: int = 8200, data_path: str = None) -> None:
        """
        Parameters
        ----------
        fuseki_path : str
            Path to the fuseki server folder.
        mb_ram : int
            RAM size in MB for the fuseki server.
        data_path : str
            Path to the data which should be uploaded.
        """
        self.FUSEKI_PATH = fuseki_path
        self.MB_RAM = mb_ram
        self.server = None
        self.starter_path = os.path.join(UNCO_PATH, r"src\unco\features\server_starter.bat")
        self._initialize()
        self.start_server()

    def _initialize(self) -> None:
        """
            Method, which creates the server_starter.bat which starts the fuseki server.
        """
        with open(self.starter_path, 'w') as starter:
            starter.write("echo 'Running fuseki server'\ncd \"" + self.FUSEKI_PATH + "\"\n")
            starter.write("java -Xmx" + str(self.MB_RAM) + "M -jar \"fuseki-server.jar\" --update --mem /ds %*")

    def start_server(self) -> None:
        """
            Method, which starts the fuseki server
        """
        if self.server:
            print(Fore.YELLOW + "WARNING: Server is already running." + Fore.RESET)
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server = subprocess.Popen(self.starter_path, creationflags=subprocess.CREATE_NEW_CONSOLE, start_new_session=True)
            time.sleep(3)

    def stop_server(self) -> None:
        """
            Method, which stops the fuseki server
        """
        if self.server:
            for child in psutil.Process(self.server.pid).children():
                child.kill()
            self.server = None
        else:
            print(Fore.YELLOW + "WARNING: There is no server to stop." + Fore.RESET)

if __name__ == "__main__":
    f = FusekiServer()
    data = open(r'D:\Dokumente\Repositories\unco\data\output\7.rdf', 'r', encoding='utf-8').read()
    headers = {'Content-Type': r'application/rdf+xml;charset=utf-8'}
    newdata = requests.post('http://localhost:3030/ds/data', data=data.encode('utf-8'), headers=headers)


    response = requests.post('http://localhost:3030/ds/sparql', data={'query': 'SELECT * WHERE {?sub ?pred ?obj .} LIMIT 10'})
    print(response.json())