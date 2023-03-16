import random
import numpy as np

from unco.data.rdf_data import RDFData


class UncertaintyGenerator():

    def __init__(self, rdfdata : RDFData) -> None:
        self.rdfdata = rdfdata
        self.NUMBER_OF_ALTERNATIVES : int

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

        nrows, ncolums = self.rdfdata.data.shape

        list_of_columns = list(set(list_of_columns)) # Remove all duplicates from list

        if len(list_of_columns) == 0:
            # get random number of uncertainties between 1 and the number of columns
            if number_of_uncertain_columns <= 0:
                number_of_uncertain_columns = random.randrange(1, ncolums)
            elif number_of_uncertain_columns >= ncolums:
                raise IndexError("Number of uncertain columns to high.")

            uncertain_columns = random.sample(range(1, ncolums), number_of_uncertain_columns)

        else:
            # catch wrong inputs:
            if not(all(isinstance(n, int) for n in list_of_columns)):
                raise ValueError("List of columns includes non int elements.")
            elif not(all(n < ncolums and n > 0 for n in list_of_columns)) or len(list_of_columns) > ncolums:
                raise ValueError("Wrong column indices.")
            
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

        self.rdfdata.uncertainty_flags = uncertainty_flags


    def add_alternatives(self):
        for column in self.rdfdata.uncertainty_flags:
            values_of_column = set(self.rdfdata.data[self.rdfdata.data.columns[column]].tolist())
            for row in self.rdfdata.uncertainty_flags[column]:
                set_of_alternatives = values_of_column - {self.rdfdata.data.iat[row,column]}
                if self.NUMBER_OF_ALTERNATIVES < 1 or self.NUMBER_OF_ALTERNATIVES > len(set_of_alternatives):
                    self.rdfdata.alternatives[(row,column)] = random.sample(list(set_of_alternatives),random.randint(1,len(set_of_alternatives)))
                else:
                    self.rdfdata.alternatives[(row,column)] = random.sample(list(set_of_alternatives),self.NUMBER_OF_ALTERNATIVES)

    def add_likelihoods(self):
        for value in self.rdfdata.alternatives:
            likelihoods = []
            sum = 0
            for _ in self.rdfdata.alternatives[value]:
                randomvalue = random.randint(1,10)
                sum += randomvalue
                likelihoods.append(randomvalue)

            likelihoods = np.array(likelihoods)
            likelihoods = np.divide(likelihoods,sum)

            self.rdfdata.likelihoods[value] = likelihoods