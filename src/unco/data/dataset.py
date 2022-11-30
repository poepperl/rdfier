import csv

class Dataset:
    """
    Class that reads a CSV table and saves as a dataset
    Args:
        csvpath: Path to the csv table
    """

    path: str

    def __init__(self,csvpath) -> None:
        self.path = csvpath


    def read(self) -> None:
        print("reading...")
        try:
            file = open(self.path,'r',encoding='utf-8')
        
        except FileNotFoundError:
            print("Error reading csv file")
            return
        
        csv_file = csv.reader(file)
        for elem in csv_file:
            for cell in elem:
                print(cell)

data = Dataset(r"D:\Dokumente\Repositories\unco\tests\test_data\1\testData_3.csv")
data.read()