import csv

class CSVReader:
    """
        Class that reads a CSV table and saves as a dataset

        Arguments:
            csvpath: Path to the csv table
    """

    path: str

    def __init__(self,csvpath) -> None:
        self.path = csvpath

    def read(self) -> None:
        """
            Reads and returns a CSV file
        """
        try:
            file = open(self.path,'r',encoding='utf-8')
            return csv.reader(file)

        except FileNotFoundError:
            print("There is no CSV file on this path.")