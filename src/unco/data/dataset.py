import csv
import random
from unco.data import Reader
from colorama import Fore


class Dataset:
    """
        Class that adds a perturbation by creating random uncertainty.
    """

    data: csv.reader

    def __init__(self, path: str) -> None:
        self.data = Reader(path).read()

    def add_uncertainty_flags(self, number_of_uncertainties: int=0, list_of_columns: list[int] =[]) -> None:
        first_line = next(self.data)
        ncolums = len(next(self.data))


        if len(list_of_columns) == 0:
            # get random number of uncertainties between 1 and the number of rows - 1
            if number_of_uncertainties <= 0: # Random number of uncertainty values between 1 and number of rows
                number_of_uncertainties = random.randrange(1, ncolums)
            elif number_of_uncertainties >= ncolums:
                print(Fore.RED + "ERROR: Number of Uncertanties to high." + Fore.RESET)
                return

            uncertain_columns = random.sample(range(1, ncolums), number_of_uncertainties)

        else:
            # catch wrong inputs:
            if not(all(isinstance(n, int) for n in list_of_columns)):
                print(Fore.RED + "ERROR: List of Columns includes non int elements." + Fore.RESET)
                return
            elif not(all(n < ncolums and n > 0 for n in list_of_columns)) or len(list_of_columns) > ncolums:
                print(Fore.RED + "ERROR: Wrong Column indices." + Fore.RESET)
                return
            
            uncertain_columns = list_of_columns

        print(uncertain_columns)

        # for column in random_columns:
        #     column_name = first_line[column]
        #     column_name = column_name[column_name.rfind("#")+1:]
        #     column_name += "*hasUncertainty"
        #     next(self.data).append(column_name)

p = Dataset(r"D:\Dokumente\Repositories\unco\tests\test_data\csv_testdata\unittest_reader.csv")
p.add_uncertainty_flags(3, [])
