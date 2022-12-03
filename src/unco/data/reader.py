import os
import csv
from colorama import Fore  # prints warnings in red
from src.unco import UNCO_PATH


class Reader:
    """
        Class that reads a file and creates a CSV object.

        Arguments:
            docpath: Path to the input file
    """

    path: str
    type: str

    def __init__(self, docpath: str) -> None:
        self.path = docpath
        self.initialise_type()

    def initialise_type(self) -> None:
        self.type = self.path[self.path.rfind(".")+1:]

        if len(self.type) > 4:
            print(Fore.RED + "Please enter a complete path with datatype-prefix!" + Fore.RESET)

    def read(self) -> csv:
        """
            Reads the input and returns a CSV object.
        """

        if self.type == "csv":
            try:
                file = open(self.path, 'r', encoding='utf-8')
                return csv.reader(file)

            except FileNotFoundError:
                print(Fore.RED + "Warning: There is no CSV file on this path." + Fore.RESET)
        
        elif self.type == "pdf":
            print(Fore.RED + "Warning: PDF not aviable." + Fore.RESET)
        else:
            print(Fore.RED + "Warning: Unknown File-Type!" + Fore.RESET)


path = os.path.join(UNCO_PATH, "tests/test_data/csv_testdata/unittest_readersv")
data = Reader(path).read()
