import pandas as pd
from warnings import warn

class RDFData:
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

    def __init__(self, dataframe: pd.DataFrame) -> None:
        """
        Parameters
        ----------
        path : str
            Path to the input-data.
        """
        self.data = dataframe
        self.triple_plan: dict = {}
        self.types_and_languages: dict[tuple[int,int], list[str]] = {}

        self.uncertainty_flags: dict = {}
        self.alternatives: dict = {}
        self.likelihoods: dict = {}

        self._generate_triple_plan()
        self._generate_type_and_language_plan()


    def _generate_triple_plan(self):
        """
            Method which locates the subject columns and the corresponding objects and saves it in the triple_plan.
        """
        first_col_has_ref = (False, '')
        first_col_objects = set()

        for index, column in enumerate(self.data):
            new_column_name = column

            splitlist = str(new_column_name).split("**")
            if len(splitlist) == 2:
                subject_id = splitlist[-1]
                new_column_name = splitlist[0]

                if index == 0:
                    first_col_has_ref = (True, subject_id)

                if subject_id in self.triple_plan:
                    if len(self.triple_plan[subject_id]["subject"]) > 0:
                        raise SyntaxError("Duplicate subject reference")
                    self.triple_plan[subject_id]["subject"] = set([index])
                    
                else:
                    self.triple_plan[subject_id] = {"subject" : set([index]), "object" : set()}

            elif len(splitlist) > 2:
                raise SyntaxError(f"Column {str(column)} has more than one subject reference marker '**'.")

            splitlist = str(new_column_name).split("__")
            if len(splitlist) == 2:
                object_id = splitlist[0]
                new_column_name = splitlist[1]

                if object_id in self.triple_plan:
                    self.triple_plan[object_id]["object"].add(index)

                else:
                    self.triple_plan[object_id] = {"object" : set([index]), "subject" : set()}

            elif len(splitlist) > 2:
                raise SyntaxError(f"Column {str(column)} has more than one object reference marker '__'.")

            elif index != 0:
                first_col_objects.add(index)


            if first_col_has_ref[0]:
                self.triple_plan[first_col_has_ref[1]]["object"].update(first_col_objects)
                self.triple_plan["**"] = self.triple_plan.pop(first_col_has_ref[1])

            else:
                self.triple_plan["**"] = {"object" : first_col_objects, "subject" : set([0])}
        
            self.data.rename({column : new_column_name}, axis=1, inplace=True)


    def _generate_type_and_language_plan(self):
        """
            Method which read the datatype or language of all columns.
        """
        # Column type or language:
        for col_index, column in enumerate(self.data):
            column_type_language, column_name = self._get_type_language(str(column))

            # Entry type or language:
            for cell_index, cell in enumerate(self.data[column]):
                splitlist = str(cell).split(";")
                cell_types_languages = splitlist
                for entry_index, entry in enumerate(splitlist):
                    tl, entry_name = self._get_type_language(entry)
                    splitlist[entry_index] = entry_name
                    cell_types_languages[entry_index] = tl if tl is not None else column_type_language if column_type_language is not None else self._get_datatype(entry)
                
                self.types_and_languages[(cell_index,col_index)] = cell_types_languages

                self.data.iat[cell_index,col_index] = "; ".join(splitlist) # Rename cell
            
            if column_name != str(column): self.data.rename({column : column_name}, axis=1, inplace=True) # Rename column


    def _get_type_language(self, string : str) -> tuple[str,str]:
        type_splitlist = string.split("^^")

        if len(type_splitlist) >= 2:
            return "^^" + type_splitlist[-1], string[:-len(type_splitlist[-1]) -2]

        language_splitlist = string.split("@")

        if len(language_splitlist) >= 2:
            if 1 <= len(language_splitlist[-1]) <= 3:
                return "@" + language_splitlist[-1], string[:-len(language_splitlist[-1]) -1]
            else:
                warn(f"\033[93mEntry \"{language_splitlist[-1]}\" is not a right language acronym.\033[0m")

        return None, string
        

    def _get_datatype(self, string : str) -> str:
        """
            Method which outputs the fitting datatype of a value.

        Parameters
        ----------
        string : str
            Entry of the csv table.
        """
        try:
            _ = int(string)
            return "^^xsd:long"
        except:
            pass
        
        try:
            _ = float(string)
            return "^^xsd:float"
        except:
            pass

        if string.lower() == "true" or string.lower() == "false":
            return "^^xsd:boolean"
        else:
            return None
        


if __name__ == "__main__":
    file = open(r"D:\Dokumente\Repositories\unco\tests\test_data\csv_testdata\eingabeformat.csv", encoding='utf-8')
    p = RDFData(pd.read_csv(file))
    print(p.data, p.types_and_languages)