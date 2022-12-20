import pandas as pd
import random
from unco.data import Reader
from colorama import Fore


class Dataset:
    """
        Class that adds a perturbation by creating random uncertainty.

    Attributes
    ----------
    data : pd.DataFrame
        DataFrame wich includes the data from Reader.
    uncertainty_flags: dict
        Dictionary to save some uncertainty flags. A flag is saved as: uncertainty_flags[(ID,column_index)] = 1
    """

    data: pd.DataFrame
    uncertainty_flags: dict

    def __init__(self, path: str) -> None:
        """
        Parameters
        ----------
        path : str
            Path to the input-data.
        """
        self.data = Reader(path).read()

    def add_uncertainty_flags(self, number_of_uncertain_columns: int=0, list_of_columns: list[int] =[], uncertainties_per_column: int = 0) -> None:
        """ Method to create random uncertaintie flags.

        Parameters
        ----------
        number_of_uncertain_columns : int, optional
            The number of columns, which get uncertainty flags. Only used, if list_of_columns is empty. By default, the number is chosen randomly between 1 and the number of columns.
        list_of_columns: list[int], optional
            List of columns which should get uncertainty flags.
        uncertainties_per_column: int, optional
            Number of uncertainties each column. By default, the number is chosen randomly each column beween 1 and the number of rows.
        """

        nrows, ncolums = self.data.shape

        list_of_columns = list(dict.fromkeys(list_of_columns)) # Remove all duplicates from list

        if len(list_of_columns) == 0:
            # get random number of uncertainties between 1 and the number of columns
            if number_of_uncertain_columns <= 0:
                number_of_uncertain_columns = random.randrange(1, ncolums)
            elif number_of_uncertain_columns >= ncolums:
                print(Fore.RED + "ERROR: Number of uncertan columns to high." + Fore.RESET)
                return

            uncertain_columns = random.sample(range(1, ncolums), number_of_uncertain_columns)

        else:
            # catch wrong inputs:
            if not(all(isinstance(n, int) for n in list_of_columns)):
                print(Fore.RED + "ERROR: List of columns includes non int elements." + Fore.RESET)
                return
            elif not(all(n < ncolums and n > 0 for n in list_of_columns)) or len(list_of_columns) > ncolums:
                print(Fore.RED + "ERROR: Wrong column indices." + Fore.RESET)
                return
            
            uncertain_columns = list_of_columns

        uncertainty_flags = {}
        for column in uncertain_columns:
            if uncertainties_per_column < 1 or uncertainties_per_column > nrows-1:
                uncertain_values = random.sample(range(0, nrows), random.randint(1, nrows)) # Get random row indices
            else:
                uncertain_values = random.sample(range(0, nrows), uncertainties_per_column)
            
            for row in uncertain_values:
                uncertainty_flags[(self.data.iat[row,0],column)] = 1

        self.uncertainty_flags = uncertainty_flags