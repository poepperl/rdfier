from unco import UNCO_PATH
import subprocess
import requests
import socket

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    subprocess.Popen(r"D:\Dokumente\Repositories\unco\src\unco\features\start-server.bat")