import os
import subprocess
import psutil
import socket
import time
import requests
from unco import UNCO_PATH
from colorama import Fore

class FusekiServer:
    """
        Interface to the fuseki server.
    """

    def __init__(self, fuseki_path: str = os.path.join(UNCO_PATH, r"src\fuseki"), gb_ram: int = 4) -> None:
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
        self.starter_path = os.path.join(UNCO_PATH, r"src\unco\features\server_starter.bat")
        self._initialize()
        self.start_server()

    def _initialize(self) -> None:
        """
            Method, which creates the server_starter.bat which starts the fuseki server.
        """
        with open(self.starter_path, 'w') as starter:
            starter.write("echo 'Running fuseki server'\ncd \"" + self.FUSEKI_PATH + "\"\n")
            starter.write("java -Xmx" + str(self.GB_RAM) + "G -jar \"fuseki-server.jar\" --update --mem /ds %*")

    def start_server(self) -> None:
        """
            Method, which starts the fuseki server.
        """
        if self.server:
            print(Fore.YELLOW + "WARNING: Server is already running." + Fore.RESET)
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server = subprocess.Popen(self.starter_path, creationflags=subprocess.CREATE_NEW_CONSOLE, start_new_session=True)
            time.sleep(3)
    
    def upload_data(self, path: str) -> None:
        """
            Method, which uploads data in rdf or turtle files to the server

        Parameters
        ----------
        path : str
            Path to the file that should be uploaded.
        """
        if self.server == None:
            print(Fore.RED + "ERROR: Server is shut down. Please start the server." + Fore.RESET)
            return
        if path[-3:] == "rdf":
            headers = {'Content-Type': r'application/rdf+xml;charset=utf-8', 'Filename' : path}
        elif path[-3:] == "ttl":
            headers = {'Content-Type': r'text/turtle;charset=utf-8'}
        else:
            print(Fore.RED + "ERROR: Unknown Datatyp. Please use \".rdf\" or \".ttl\" files as input." + Fore.RESET)
            return
        data = open(path, 'r', encoding='utf-8').read()
        newdata = requests.post('http://localhost:3030/ds/data', data=data.encode('utf-8'), headers=headers)


    def stop_server(self) -> None:
        """
            Method, which stops the fuseki server.
        """
        if self.server:
            for child in psutil.Process(self.server.pid).children():
                child.kill()
            self.server = None
        else:
            print(Fore.YELLOW + "WARNING: Server already stopped." + Fore.RESET)

if __name__ == "__main__":
    f = FusekiServer()
    f.upload_data(r"D:\Dokumente\Repositories\unco\data\output\7.rdf")
    input()
    f.stop_server()


    # response = requests.post('http://localhost:3030/ds/sparql', data={'query': 'SELECT * WHERE {?sub ?pred ?obj .} LIMIT 10'})
    # print(response.json())