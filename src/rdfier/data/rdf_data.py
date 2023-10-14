from __future__ import annotations

from warnings import warn

import numpy as np
import pandas as pd


class RDFData:
    """
        Class that represents the RDF data.

    Attributes
    ----------
    data : pd.DataFrame
        Pandas dataframe which includes the data in the defined input format.
    triple_plan: dict
        Dictionary to save which columns are interpreted as subjects and their corresponding object columns.
    types_and_languages: dict
        Dictionary to save the datatype or language of a value.
    uncertainties: dict
        Dictionary with (row, column) of an uncertain cell as key and the uncertainty as value.
    """

    def __init__(self, dataframe: pd.DataFrame) -> None:
        """
        Parameters
        ----------
        dataframe : pd.DataFrame
            Dataframe of the data which gets pseudorandom uncertainty.
        """
        self.data = self.data_optimize(dataframe)
        self.triple_plan: dict = {}
        self.types_and_languages: dict[tuple[int, int], list[str]] = {}
        self.uncertainties: dict = {}

        self._generate_triple_plan()
        self._load_uncertainties()
        self._generate_type_and_language_plan()

    def data_optimize(self, dataframe: pd.DataFrame, object_option=False):
        """
        Reduce the size of the input dataframe

        Parameters
        ----------
        dataframe: pd.DataFrame
            Input dataframe which should get smaller.
        object_option: bool
            If true, try to convert object to category.
        """

        # loop columns in the dataframe to downcast the dtype
        for col in dataframe.columns:
            # process the int columns
            if dataframe[col].dtype == "int":
                col_min = dataframe[col].min()
                col_max = dataframe[col].max()
                # if all are non-negative, change to uint
                if col_min >= 0:
                    if col_max < np.iinfo(np.uint8).max:
                        dataframe[col] = dataframe[col].astype(np.uint8)
                    elif col_max < np.iinfo(np.uint16).max:
                        dataframe[col] = dataframe[col].astype(np.uint16)
                    elif col_max < np.iinfo(np.uint32).max:
                        dataframe[col] = dataframe[col].astype(np.uint32)
                    else:
                        dataframe[col] = dataframe[col]
                else:
                    # if it has negative values, downcast based on the min and max
                    if (
                        col_max < np.iinfo(np.int8).max
                        and col_min > np.iinfo(np.int8).min
                    ):
                        dataframe[col] = dataframe[col].astype(np.int8)
                    elif (
                        col_max < np.iinfo(np.int16).max
                        and col_min > np.iinfo(np.int16).min
                    ):
                        dataframe[col] = dataframe[col].astype(np.int16)
                    elif (
                        col_max < np.iinfo(np.int32).max
                        and col_min > np.iinfo(np.int32).min
                    ):
                        dataframe[col] = dataframe[col].astype(np.int32)
                    else:
                        dataframe[col] = dataframe[col]

            # process the float columns
            elif dataframe[col].dtype == "float":
                col_min = dataframe[col].min()
                col_max = dataframe[col].max()
                # downcast based on the min and max
                if (
                    col_min > np.finfo(np.float32).min
                    and col_max < np.finfo(np.float32).max
                ):
                    dataframe[col] = dataframe[col].astype(np.float32)
                else:
                    dataframe[col] = dataframe[col]

            if object_option:
                if dataframe[col].dtype == "object":
                    if len(dataframe[col].value_counts()) < 0.5 * dataframe.shape[0]:
                        dataframe[col] = dataframe[col].astype("category")

        return dataframe

    def _generate_triple_plan(self):
        """
        Method which locates the subject columns and the corresponding objects and save them in the triple_plan.
        """
        first_col_has_ref = (False, "")
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
                    self.triple_plan[subject_id]["subject"] = {index}

                else:
                    self.triple_plan[subject_id] = {
                        "subject": {index},
                        "objects": set(),
                        "certainties": set(),
                    }

            elif len(splitlist) > 2:
                raise SyntaxError(
                    f"Column {str(column)} has more than one subject reference marker '**'."
                )

            splitlist = str(new_column_name).split("__")
            if len(splitlist) == 2:
                object_id = splitlist[0]
                new_column_name = splitlist[1]

                if (
                    len(us := new_column_name.split("^^")) > 1
                    and us[-1][:11] == "certainty"
                ):
                    self.triple_plan[object_id]["certainties"].add(index)
                elif object_id in self.triple_plan:
                    self.triple_plan[object_id]["objects"].add(index)
                else:
                    self.triple_plan[object_id] = {
                        "objects": {index}, "subject": set()}

            elif len(splitlist) > 2:
                raise SyntaxError(
                    f"Column {str(column)} has more than one object reference marker '__'."
                )

            elif index != 0:
                first_col_objects.add(index)

            if first_col_has_ref[0]:
                self.triple_plan[first_col_has_ref[1]]["objects"].update(
                    first_col_objects
                )
                self.triple_plan["**"] = self.triple_plan.pop(
                    first_col_has_ref[1])

            else:
                self.triple_plan["**"] = {"objects":
                                          first_col_objects, "subject": {0}}

            self.data.rename({column: new_column_name}, axis=1, inplace=True)

    def _load_uncertainties(self) -> None:
        """
        Takes all uncertainty columns from the triple_plan and load their uncertainties into th uncertainties dictionary.
        """
        for plan in self.triple_plan.values():
            if "certainties" in plan:
                sub_column = next(iter(plan["subject"]))
                if (lenght := len(plan["certainties"])) == 1:
                    unc_column = next(iter(plan["certainties"]))
                    for row_index in range(len(self.data)):
                        if pd.notna(self.data.iat[row_index, unc_column]):
                            uncertainties = self._get_uncertainty_dict(
                                str(self.data.iat[row_index, sub_column]),
                                str(self.data.iat[row_index, unc_column]),
                            )
                            if uncertainties:
                                self.uncertainties[
                                    (row_index, sub_column)
                                ] = uncertainties
                elif lenght > 1:
                    raise SyntaxError(
                        f"Subject-column {self.data.columns[sub_column]} has more than one certainty-column."
                    )

    def _get_uncertainty_dict(self, subjects: str, uncertainty: str) -> dict:
        """
        Method to generate a dictionary with all important informations about a uncertain statement
        like if it has alternatives and which weights.

        Parameters
        ----------
        subjects: str
            String of the subject(s) which get(s) the uncertainty. The uncertain statement is a nested statement and
            refers to the statement which has the subject(s) as its object(s).
        uncertainty: str
            String of the uncertainty mode. Can be `u` for uncertain or `a` for alternatives. Will be removed in a future release.
        """
        uncertainty = uncertainty.strip().lower()
        sub_splitlist = subjects.split(";")
        unc_splitlist = uncertainty.split(";")

        if uncertainty == "c":
            return dict()
        elif uncertainty == "ou" and len(sub_splitlist) == 1:
            return {"mode": "ou"}
        elif uncertainty == "a" and len(sub_splitlist) > 1:
            return {"mode": "a"}
        elif uncertainty == "au":
            return {"mode": "au"}
        elif uncertainty == "u":
            return {"mode": "u"}
        elif len(unc_splitlist) == 1:
            try:
                numb = float(uncertainty)
                if 0 <= numb < 1:
                    return {"mode": "ou", "weights": [numb]}
                elif numb == 1:
                    return dict()
                elif not pd.isna(numb):
                    warn(
                        f'\033[93mUncertainty "{uncertainty}" out of bounds. No uncertainty will be transmit.\033[0m'
                    )
                    return dict()
            except:
                pass
        elif len(sub_splitlist) == len(unc_splitlist):
            try:
                unc_splitlist = [float(elem) for elem in unc_splitlist]
            except:
                pass
            if all(isinstance(n, float) for n in unc_splitlist):
                if sum(unc_splitlist) == 1:
                    return {"mode": "a", "weights": unc_splitlist}
                elif 0 <= sum(unc_splitlist) < 1:
                    return {"mode": "au", "weights": unc_splitlist}
            warn(
                f'\033[93mUnknown distribution "{uncertainty}". No uncertainties will be transmit.\033[0m'
            )
            return dict()
        elif len(sub_splitlist) != len(unc_splitlist):
            warn(
                f'\033[93mEntry "{subjects}" hasn\'t the correct number of uncertainties "{uncertainty}".'
                f" No uncertainties will be transmit.\033[0m"
            )
            return dict()
        else:
            warn(
                f'\033[93mEntry "{subjects}" hasn\'t identiefiable uncertainties "{uncertainty}". '
                f"No uncertainties will be transmit.\033[0m"
            )
            return dict()

    def _generate_type_and_language_plan(self) -> None:
        """
        Method which read the datatype/language of all columns.
        """
        # Column type or language:
        for col_index, column in enumerate(self.data):
            column_type_language, column_name = self._get_datatype_language(
                str(column))

            # Entry type or language:
            for cell_index, cell in enumerate(self.data.iloc[:, col_index]):
                if pd.notnull(cell):
                    splitlist = str(cell).split(";")
                    cell_types_languages = splitlist.copy()
                    for entry_index, entry in enumerate(splitlist):
                        tl, entry_name = self._get_datatype_language(entry)
                        splitlist[entry_index] = entry_name.strip()
                        cell_types_languages[entry_index] = (
                            tl.strip()
                            if tl != ""
                            else column_type_language
                            if column_type_language != ""
                            else self._get_fitting_datatype(entry)
                        )

                    self.types_and_languages[
                        (cell_index, col_index)
                    ] = cell_types_languages

                    self.data.iat[cell_index, col_index] = "; ".join(
                        splitlist
                    )  # Rename cell

            if column_name != str(column):
                # Rename column
                self.data.columns.values[col_index] = column_name

    def _get_datatype_language(self, entry: str) -> tuple[str, str]:
        """
        Method which extracts the type/language of a string.

        Parameters
        ----------
        entry: str
            String of a cell entry.
        """
        greek2latin = str.maketrans(
            "ΑαΒβΓγΔδΕεΖζΗηΘθΙιΚκΛλΜμΝνΞξΟοΠπΡρΣσςΤτΥυΦφΧχΨψΩω・•",
            "AaBbGgDdEeZzHhJjIiKkLlMmNnXxOoPpRrSssTtUuFfQqYyWw..",
        )
        entry = entry.translate(greek2latin)
        type_splitlist = entry.split("^^")

        if len(type_splitlist) >= 2:
            return "^^" + type_splitlist[-1], entry[: -len(type_splitlist[-1]) - 2]

        language_splitlist = entry.split("@")

        if len(language_splitlist) >= 2:
            if 1 <= len(language_splitlist[-1]) <= 3:
                return (
                    "@" + language_splitlist[-1],
                    entry[: -len(language_splitlist[-1]) - 1],
                )
            else:
                warn(
                    f'\033[93mEntry "{language_splitlist[-1]}" is not a right language acronym.\033[0m'
                )

        return "", entry

    def _get_fitting_datatype(self, string: str) -> str:
        """
            Method which tries to find the best fitting datatype of a value.

        Parameters
        ----------
        string : str
            Value for which no datatype or language was specified.
        """
        try:
            _ = int(string)
            return "^^xsd:long"
        except:
            pass

        try:
            _ = float(string)
            return "^^xsd:decimal"
        except:
            pass

        if string.lower() == "true" or string.lower() == "false":
            return "^^xsd:boolean"
        else:
            return ""
