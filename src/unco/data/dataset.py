import csv
import random
from src.unco.data import Reader
from colorama import Fore


class Dataset:
    """
        Class that adds a perturbation by creating random uncertainty.
    """

    data: csv.reader

    def __init__(self, path: str) -> None:
        self.data = Reader(path).read()

    def add_uncertainty(self, number_of_uncertainties=0) -> None:
        first_line = next(self.data)
        ncolums = len(next(self.data))

        # get random number of uncertainties between 1 and the number of rows
        if number_of_uncertainties <= 0:
            number_of_uncertainties = random.randrange(1, ncolums)
        elif number_of_uncertainties > ncolums-1:
            print(Fore.RED + "ERROR: Number of Uncertanties to high." + Fore.RESET)
            return

        random_columns = random.sample(range(1, ncolums), number_of_uncertainties)

        for column in random_columns:
            column_name = first_line[column]
            column_name = column_name[column_name.rfind("#")+1:]
            column_name += "*hasUncertainty"
            next(self.data).append(column_name)

        discard_first = False

        for line in self.data:
            if discard_first:
                pass
            else:
                discard_first = True


p = Dataset(r"C:\Users\poepperl\Documents\Repositories\tests\test_data\csv_testdata\testData_3.csv")
p.add_uncertainty(2)
