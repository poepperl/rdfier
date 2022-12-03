import csv

"""
    Class that reads a CSV table and saves as a dataset
    Args:
        csvpath: Path to the csv table
"""
class CSVReader:

    path: str

    def __init__(self,csvpath) -> None:
        self.path = csvpath


    def read(self) -> None:
        try:
            file = open(self.path,'r',encoding='utf-8')
            return csv.reader(file)

        except FileNotFoundError:
            print("There is no CSV file on this path.")