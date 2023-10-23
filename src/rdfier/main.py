from rdfier import RDFIER_PATH
import sys
from pathlib import Path
from streamlit.web import cli as stcli

def main():
    print("Start RDFier...")
    sys.argv = ["streamlit", "run", str(Path(RDFIER_PATH, "src/rdfier_app/RDFier.py")), "&>/content/logs.txt", "&"]
    sys.exit(stcli.main())

if __name__ == '__main__':
    main()