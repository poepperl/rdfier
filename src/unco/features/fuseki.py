from unco import UNCO_PATH
import subprocess
import os
import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

subprocess.Popen(r"D:\Dokumente\Repositories\unco\src\unco\features\start-server.bat")
