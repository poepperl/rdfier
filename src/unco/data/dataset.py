import pandas as pd
import random
from unco.data import Reader
from colorama import Fore


class Dataset:
    """
        Class that adds a perturbation by creating random uncertainty.
    """

    data: pd.DataFrame
    uncertainty_flags: dict

    def __init__(self, path: str) -> None:
        self.data = Reader(path).read()

    def add_uncertainty_flags(self, number_of_uncertain_columns: int=0, list_of_columns: list[int] =[], uncertainties_per_column: int = 0) -> None:
        nrows, ncolums = self.data.shape

        list_of_columns = list(dict.fromkeys(list_of_columns)) # Remove all duplicates from list

        if len(list_of_columns) == 0:
            # get random number of uncertainties between 1 and the number of rows - 1
            if number_of_uncertain_columns <= 0: # Random number of uncertainty values between 1 and number of rows
                number_of_uncertain_columns = random.randrange(1, ncolums)
            elif number_of_uncertain_columns >= ncolums:
                print(Fore.RED + "ERROR: Number of Uncertanties to high." + Fore.RESET)
                return

            uncertain_columns = random.sample(range(1, ncolums), number_of_uncertain_columns)

        else:
            # catch wrong inputs:
            if not(all(isinstance(n, int) for n in list_of_columns)):
                print(Fore.RED + "ERROR: List of Columns includes non int elements." + Fore.RESET)
                return
            elif not(all(n < ncolums and n > 0 for n in list_of_columns)) or len(list_of_columns) > ncolums:
                print(Fore.RED + "ERROR: Wrong Column indices." + Fore.RESET)
                return
            
            uncertain_columns = list_of_columns

        uncertainty_flags = {}
        for column in uncertain_columns:
            if uncertainties_per_column < 1 or uncertainties_per_column > nrows-1:
                uncertain_values = random.sample(range(0, nrows), random.randint(1, nrows)) # Get random row indices
            else:
                uncertain_values = random.sample(range(0, nrows), uncertainties_per_column)
            
            for row in uncertain_values:
                uncertainty_flags[(row,column)] = 1

        self.uncertainty_flags = uncertainty_flags
