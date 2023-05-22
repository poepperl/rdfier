import random
import numpy as np

from unco.data.rdf_data import RDFData


class UncertaintyGenerator():
    """
    Class which generates pseudorandom uncertainty for a RDFData.

    Attributes
    ----------
    rdfdata : RDFData
        The RDFData, which should get the uncertainties.
    """
    def __init__(self, rdfdata : RDFData) -> None:
        self.rdfdata = rdfdata
        self.NUMBER_OF_ALTERNATIVES : int

    def add_pseudorand_uncertainty_flags(self, number_of_uncertain_columns: int=0, list_of_columns: list[int] =[], uncertainties_per_column: int = 0) -> RDFData:
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
            if number_of_uncertain_columns < 0:
                number_of_uncertain_columns = random.randrange(1, ncolums)
            elif number_of_uncertain_columns >= ncolums:
                raise IndexError("Number of uncertain columns to high.")

            uncertain_columns = random.sample(range(1, ncolums), number_of_uncertain_columns)

        else:
            # catch wrong inputs:
            if not(all(isinstance(n, int) for n in list_of_columns)):
                raise ValueError("List of columns includes none integers.")
            elif not(all(0 < n < ncolums for n in list_of_columns)) or len(list_of_columns) > ncolums:
                raise ValueError("Wrong column indices.")
            
            uncertain_columns = list_of_columns

        uncertainty_flags = {}
        for column in uncertain_columns:
            if uncertainties_per_column < 1 or uncertainties_per_column > nrows:
                uncertain_values = random.sample(range(0, nrows), random.randint(1, nrows)) # Get random row indices
            else:
                uncertain_values = random.sample(range(0, nrows), uncertainties_per_column)
            
            for row in uncertain_values:
                if len(str(self.rdfdata.data.iat[row,column]).split(";")) == 1:
                    uncertainty_flags[(row,column)] = {"mode":"ou"}
                else:
                    uncertainty_flags[(row,column)] = {"mode":"a"}
                

        self.rdfdata.uncertainties = uncertainty_flags
        return self.rdfdata
    

    def add_pseudorand_alternatives(self, min_number_of_alternatives : int = 1, max_number_of_alternatives : int = 3, list_of_columns: list[int] =[]) -> RDFData:
        """ Method to add alternatives to the existing uncertainty flags.

        Parameters
        ----------
        min_number_of_alternatives : int, optional
            The least number of alternatives, which should be added to every uncertainty flag. Has to be 1 or higher.
        max_number_of_alternatives : int, optional
            The largest number of alternatives, which should be added to every uncertainty flag. Has to be 1 or higher.
            If there is an entry which has already more then the maximum, this method has no effect on this entry.
        list_of_columns: list[int], optional
            List of columns which should get alternatives. If no columns are choosen, every column will be processed.
        """
        list_of_columns = list(set(list_of_columns)) # Remove all duplicates from list

        #Cache wrong inputs:
        if not(all(isinstance(n, int) for n in list_of_columns)):
            raise ValueError("List of columns includes none integers.")
        
        elif not(all(0 < n < self.rdfdata.data.shape[1] for n in list_of_columns)) or len(list_of_columns) > self.rdfdata.data.shape[1]:
            raise ValueError("Wrong column indices.")
        
        if min_number_of_alternatives < 1 or max_number_of_alternatives < 1 or min_number_of_alternatives > max_number_of_alternatives:
            raise ValueError("Wrong bounds for alternatives.")
        

        if len(list_of_columns) == 0:
            list_of_columns = list(range(len(self.rdfdata.data.columns)))
    	
        list_of_column_entries = []
        for column in list_of_columns:
            values_of_column = set(self.rdfdata.data.iloc[:,column].tolist())
            values_of_column = [str(entry).split(";") for entry in values_of_column]
            values_of_column = {element for sublist in values_of_column for element in sublist}
            values_of_column = [val for val in values_of_column if val != "nan"]
            list_of_column_entries.append(values_of_column)
        
        for (row,column) in self.rdfdata.uncertainties:
            if column in list_of_columns:
                self.rdfdata.uncertainties[(row,column)]["mode"] = "a"
                current_values = str(self.rdfdata.data.iat[row,column]).split(";")
                
                numb_additional_alternatives = random.randint(min_number_of_alternatives,max_number_of_alternatives) - len(current_values)

                if numb_additional_alternatives < 1:
                    continue

                values_of_column = [str(entry).strip() for entry in list_of_column_entries[column] if entry not in current_values]

                if numb_additional_alternatives > len(values_of_column):
                    print(f"Warning: Couldn't find {numb_additional_alternatives+len(current_values)} different entries in column {column}. Set the higher bound to {len(values_of_column)+len(current_values)}.")
                    numb_additional_alternatives = len(values_of_column)

                current_values += random.sample(values_of_column, numb_additional_alternatives)

                self.rdfdata.data.iat[row,column] = "; ".join(current_values)

                likelihoods = []
                sum = 0
                for _ in current_values:
                    randomvalue = random.randint(1,10)
                    sum += randomvalue
                    likelihoods.append(randomvalue)

                likelihoods = np.array(likelihoods)
                likelihoods = np.around(np.divide(likelihoods,sum),decimals=2)

                self.rdfdata.uncertainties[(row,column)]["likelihoods"] = likelihoods
        
        return self.rdfdata


if __name__ == "__main__":
    from unco import UNCO_PATH
    from pathlib import Path
    import pandas as pd
    file = open(str(Path(UNCO_PATH,"data/input/test_eingabeformat/eingabeformat.csv")), encoding='utf-8')

    rdfdata = RDFData(pd.read_csv(file))
    g = UncertaintyGenerator(rdfdata=rdfdata)
    print(g.add_pseudorand_alternatives().data)

"""
Bei Generierung von uncertainty flags dürfen nur Spalten in Fragen kommen, die ausschließlich Objekte beinhalten.
"""