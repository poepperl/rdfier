import pandas as pd
from warnings import warn

class RDFData:
    """
        Class that represents the dataset of an unco input.

    Attributes
    ----------
    data : pd.DataFrame
        DataFrame wich includes the data from Reader.
    triple_plan: dict
        Dictionary to save which columns are interpreted as subjects and their corresponding object columns. 
    types_and_languages: dict
        Dictionary to save the datatype or language of a value.
    uncertainty_flags: dict
        Dictionary to save some uncertainty flags. A flag is saved as: uncertainty_flags[column_indices] = list(row_indices)
    alternatives: dict
        Dictionary to save some alternatives for all uncertain values. The slternatives are saved as: alternatives[(row,column)] = list(alternatives)
    """

    def __init__(self, dataframe: pd.DataFrame) -> None:
        """
        Parameters
        ----------
        dataframe : pd.DataFrame
            Dataframe of the data which gets pseudorandom uncertainty.
        """
        self.data = dataframe
        self.triple_plan: dict = {}
        self.types_and_languages: dict[tuple[int,int], list[str]] = {}

        self.uncertainties : dict = {}

        self._generate_triple_plan()
        self._load_uncertainties()
        self._generate_type_and_language_plan()


    def _generate_triple_plan(self):
        """
            Method which locates the subject columns and the corresponding objects and save them in the triple_plan.
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
                    self.triple_plan[subject_id] = {"subject" : set([index]), "objects" : set(), "uncertainty" : set()}

            elif len(splitlist) > 2:
                raise SyntaxError(f"Column {str(column)} has more than one subject reference marker '**'.")

            splitlist = str(new_column_name).split("__")
            if len(splitlist) == 2:
                object_id = splitlist[0]
                new_column_name = splitlist[1]

                if len(us := new_column_name.split("^^")) > 1 and us[-1][:11] == "uncertainty":
                    self.triple_plan[object_id]["uncertainty"].add(index)
                elif object_id in self.triple_plan:
                    self.triple_plan[object_id]["objects"].add(index)
                else:
                    self.triple_plan[object_id] = {"objects" : set([index]), "subject" : set()}

            elif len(splitlist) > 2:
                raise SyntaxError(f"Column {str(column)} has more than one object reference marker '__'.")

            elif index != 0:
                first_col_objects.add(index)


            if first_col_has_ref[0]:
                self.triple_plan[first_col_has_ref[1]]["objects"].update(first_col_objects)
                self.triple_plan["**"] = self.triple_plan.pop(first_col_has_ref[1])

            else:
                self.triple_plan["**"] = {"objects" : first_col_objects, "subject" : set([0])}
        
            self.data.rename({column : new_column_name}, axis=1, inplace=True)


    def _load_uncertainties(self):
        for plan in self.triple_plan.values():
            sub_column = next(iter(plan["subject"]))
            if "uncertainty" in plan:
                if l := len(plan["uncertainty"])==1:
                    unc_column = next(iter(plan["uncertainty"]))
                    for row_index in range(len(self.data)):
                        uncertainties = self._get_uncertainty_dict(str(self.data.iat[row_index,sub_column]), str(self.data.iat[row_index,unc_column]))
                        if uncertainties : self.uncertainties[(row_index,sub_column)] = uncertainties
                elif l > 1:
                    raise SyntaxError(f"Subject-column {self.data.columns[sub_column]} has more than one uncertainty-column.")
            
    def _get_uncertainty_dict(self, subject : str, uncertainty : str) -> dict:
        # {(1,2):{"mode":"a", "likelihoods":[0.5,0.1,0.4]}}
        uncertainty = uncertainty.strip().lower()
        sub_splitlist = subject.split(";")
        unc_splitlist = uncertainty.split(";")

        if uncertainty == "c":
            return dict()
        elif uncertainty == "ou" and len(sub_splitlist)==1:
            return {"mode":"ou"}
        elif uncertainty == "a" and len(sub_splitlist)>1:
            return {"mode":"a"}
        elif uncertainty == "au":
            return {"mode":"au"}
        elif uncertainty == "u":
            return {"mode":"u"}
        elif len(unc_splitlist) == 1:
            try:
                numb = float(uncertainty)
                if numb == 0:
                    return {"mode":"u"}
                elif numb == 1:
                    return dict()
                elif 0 < numb < 1:
                    {"mode":"ou", "likelihoods":[numb]}
                else:
                    warn(f"\033[93mUncertainty \"{uncertainty}\" out of bounds. No uncertainty will be transmit.\033[0m")
            except:
                pass
        elif len(sub_splitlist) == len(unc_splitlist):
            try:
                unc_splitlist = [float(elem) for elem in unc_splitlist]
            except:
                pass
            if all(isinstance(n, float) for n in unc_splitlist):
                if sum(unc_splitlist) == 1:
                    return {"mode":"a", "likelihoods":unc_splitlist}
                elif 0 <= sum(unc_splitlist) < 1:
                    return {"mode":"au", "likelihoods":unc_splitlist}
            warn(f"\033[93mUnknown distribution \"{uncertainty}\". No uncertainties will be transmit.\033[0m")
            return dict()
        elif len(sub_splitlist) != len(unc_splitlist):
            warn(f"\033[93mEntry \"{subject}\" hasn't the correct number of uncertainties \"{uncertainty}\". No uncertainties will be transmit.\033[0m")
            return dict()
        else:
            warn(f"\033[93mEntry \"{subject}\" hasn't identiefiable uncertainties \"{uncertainty}\". No uncertainties will be transmit.\033[0m")
            return dict()


    def _generate_type_and_language_plan(self) -> None:
        """
            Method which read the datatype/language of all columns.
        """
        # Column type or language:
        for col_index, column in enumerate(self.data):
            column_type_language, column_name = self._get_type_language(str(column))

            # Entry type or language:
            for cell_index, cell in enumerate(self.data[column]):
                if pd.notnull(cell):
                    splitlist = str(cell).split(";")
                    cell_types_languages = splitlist.copy()
                    for entry_index, entry in enumerate(splitlist):
                        tl, entry_name = self._get_type_language(entry)
                        splitlist[entry_index] = entry_name.strip()
                        cell_types_languages[entry_index] = tl.strip() if tl is not None else column_type_language if column_type_language is not None else self._get_datatype(entry)
                    
                    self.types_and_languages[(cell_index,col_index)] = cell_types_languages

                    self.data.iat[cell_index,col_index] = "; ".join(splitlist) # Rename cell
            
            if column_name != str(column): self.data.columns.values[col_index] = column_name # Rename column


    def _get_type_language(self, string : str) -> tuple[str,str]:
        """
        Method which extracts the type/language of a string.
        """
        type_splitlist = string.split("^^")

        if len(type_splitlist) >= 2:
            return "^^" + type_splitlist[-1], string[:-len(type_splitlist[-1]) -2]

        language_splitlist = string.split("@")

        if len(language_splitlist) >= 2:
            if 1 <= len(language_splitlist[-1]) and len(language_splitlist[-1]) <= 3:
                return "@" + language_splitlist[-1], string[:-len(language_splitlist[-1]) -1]
            else:
                warn(f"\033[93mEntry \"{language_splitlist[-1]}\" is not a right language acronym.\033[0m")

        return None, string
        

    def _get_datatype(self, string : str) -> str:
        """
            Method which tries to find the best fitting datatype of a value.

        Parameters
        ----------
        string : str
            Value which should get a datatype.
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
    file = open(r"C:\Users\scrum\Documents\Repositories\unco\tests\test_data\csv_testdata\eingabeformat.csv", encoding='utf-8')
    p = RDFData(pd.read_csv(file))
    print(p.data, p.types_and_languages)