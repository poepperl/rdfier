from rdfier import RDFIER_PATH
import sys
from pathlib import Path
from streamlit.web import cli as stcli

def main():
    sys.argv = ["streamlit", "run", str(Path(RDFIER_PATH, "src/rdfier_app/RDFier.py"))]
    sys.exit(stcli.main())

if __name__ == '__main__':
    main()