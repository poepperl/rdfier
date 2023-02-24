import pandas as pd
import random
import numpy as np
from unco.data import Reader
from colorama import Fore


class Dataset:
    """
        Class that represents the dataset of an unco input.

    Attributes
    ----------
    data : pd.DataFrame
        DataFrame wich includes the data from Reader.
    uncertainty_flags: dict
        Dictionary to save some uncertainty flags. A flag is saved as: uncertainty_flags[column_indices] = list(row_indices)
    alternatives: dict
        Dictionary to save some alternatives for all uncertain values. The slternatives are saved as: alternatives[(row,column)] = list(alternatives)
    """

    def __init__(self, path_data: str | pd.DataFrame) -> None:
        """
        Parameters
        ----------
        path : str
            Path to the input-data.
        """
        if type(path_data) == pd.DataFrame:
            self.data = path_data
        else:
            self.data = Reader(path_data).read()
        self.uncertainty_flags: dict = {}
        self.alternatives: dict = {}
        self.likelihoods: dict = {}
        self.NUMBER_OF_ALTERNATIVES : int = 0

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

        list_of_columns = list(set(list_of_columns)) # Remove all duplicates from list

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
            uncertainty_flags[column] = []
            if uncertainties_per_column < 1 or uncertainties_per_column > nrows:
                uncertain_values = random.sample(range(0, nrows), random.randint(1, nrows)) # Get random row indices
            else:
                uncertain_values = random.sample(range(0, nrows), uncertainties_per_column)
            
            for row in uncertain_values:
                uncertainty_flags[column].append(row)

        self.uncertainty_flags = uncertainty_flags


    def add_alternatives(self):
        for column in self.uncertainty_flags:
            values_of_column = set(self.data[self.data.columns[column]].tolist())
            for row in self.uncertainty_flags[column]:
                set_of_alternatives = values_of_column - {self.data.iat[row,column]}
                if self.NUMBER_OF_ALTERNATIVES < 1 or self.NUMBER_OF_ALTERNATIVES > len(set_of_alternatives):
                    self.alternatives[(row,column)] = random.sample(list(set_of_alternatives),random.randint(1,len(set_of_alternatives)))
                else:
                    self.alternatives[(row,column)] = random.sample(list(set_of_alternatives),self.NUMBER_OF_ALTERNATIVES)

    def add_likelihoods(self):
        for value in self.alternatives:
            likelihoods = []
            sum = 0
            for alternative in self.alternatives[value]:
                randomvalue = random.randint(1,10)
                sum += randomvalue
                likelihoods.append(randomvalue)

            likelihoods = np.array(likelihoods)
            likelihoods = np.divide(likelihoods,sum)

            self.likelihoods[value] = likelihoods

if __name__ == "__main__":
    p = Dataset(r"D:\Dokumente\Repositories\unco\tests\test_data\csv_testdata\1certain2uncertainMints\input_data.csv")
    # p = Dataset(r"D:\Dokumente\Repositories\unco\tests\test_data\csv_testdata\cointest_5.csv")
    p.add_uncertainty_flags(number_of_uncertain_columns=1,uncertainties_per_column=3)
    # p.add_alternatives()
    # p.add_likelihoods()
    print(p.uncertainty_flags)