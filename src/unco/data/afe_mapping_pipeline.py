from sys import prefix
import pandas as pd
from pathlib import Path
from random import random

from unco import data

def change_afe_coin_id(dataframe : pd.DataFrame) -> pd.DataFrame:
    """
        Turns the ids in column "Coin^^uri" into "afe:"+str(id)
    
        Parameters:
        -----------
        dataframe : pd.DataFrame
            Dataframe which should be updated
    """
    dataframe["Coin^^uri"] = dataframe["Coin^^uri"].apply(lambda x: "afe:"+str(x) if pd.notna(x) else pd.NA)
    return dataframe

def change_findspot(dataframe : pd.DataFrame) -> pd.DataFrame:
    """
        Turns the urls in column "nmo:hasFindspot^^uri" into "gaz:"+str(id)
    
        Parameters:
        -----------
        dataframe : pd.DataFrame
            Dataframe which should be updated
    """
    dataframe["nmo:hasFindspot^^uri"] = dataframe["nmo:hasFindspot^^uri"].apply(lambda x: pd.NA if pd.isna(x) else "gaz:" + str(x)[-7:])
    return dataframe

def turn_nomisma_values_to_uris(dataframe : pd.DataFrame) -> pd.DataFrame:
    """
        Turns the values in nomisma columns "nm:"+str(value)
    
        Parameters:
        -----------
        dataframe : pd.DataFrame
            Dataframe which should be updated
    """
    dataframe["nmo:hasMaterial^^uri**Ma"] = dataframe["nmo:hasMaterial^^uri**Ma"].apply(lambda x: "nm:"+str(x) if pd.notna(x) else pd.NA)
    dataframe["nmo:hasMint^^uri**Mi"] = dataframe["nmo:hasMint^^uri**Mi"].apply(lambda x: "nm:"+str(x) if pd.notna(x) else pd.NA)
    dataframe["nmo:hasMint2^^uri"] = dataframe["nmo:hasMint2^^uri"].apply(lambda x: "nm:"+str(x) if pd.notna(x) else pd.NA)
    dataframe["nmo:hasDenomination^^uri**De"] = dataframe["nmo:hasDenomination^^uri**De"].apply(lambda x: "nm:"+str(x) if pd.notna(x) else pd.NA)
    dataframe["nmo:hasDenomination2^^uri"] = dataframe["nmo:hasDenomination2^^uri"].apply(lambda x: "nm:"+str(x) if pd.notna(x) else pd.NA)

    return dataframe

def combine_mint_and_denomination(dataframe : pd.DataFrame) -> pd.DataFrame:
    """
        Combines the two mint and denomination columns.
    
        Parameters:
        -----------
        dataframe : pd.DataFrame
            Dataframe which should be updated
    """
    dataframe["nmo:hasMint^^uri**Mi"] = dataframe[["nmo:hasMint^^uri**Mi","nmo:hasMint2^^uri"]].apply(lambda x: "; ".join(x) if pd.notna(x[1]) and pd.notna(x[0]) else x[0], axis =1)
    dataframe["nmo:hasDenomination^^uri**De"] = dataframe[["nmo:hasDenomination^^uri**De","nmo:hasDenomination2^^uri"]].apply(lambda x: "; ".join(x) if pd.notna(x[1]) and pd.notna(x[0]) else x[0], axis =1)

    return dataframe.drop(["nmo:hasMint2^^uri","nmo:hasDenomination2^^uri"],axis=1)

def simplify_all_id_columns(dataframe : pd.DataFrame) -> pd.DataFrame:
    """
        All id values will be replaced with "1".
    
        Parameters:
        -----------
        dataframe : pd.DataFrame
            Dataframe which should be updated
    """
    dataframe["nmo:hasDie^^blank**Di"] = dataframe["nmo:hasDie^^blank**Di"].apply(lambda x: str(1) if pd.notna(x) else x)
    dataframe["nmo:hasObverse^^blank**Ob"] = dataframe["nmo:hasObverse^^blank**Ob"].apply(lambda x: str(1) if pd.notna(x) else x)
    dataframe["nmo:hasReverse^^blank**Re"] = dataframe["nmo:hasReverse^^blank**Re"].apply(lambda x: str(1) if pd.notna(x) else x)

    return dataframe

def remove_wrong_context_from_obverse(dataframe : pd.DataFrame) -> pd.DataFrame:
    """
        Removes reverse context from obverse.
    
        Parameters:
        -----------
        dataframe : pd.DataFrame
            Dataframe which should be updated
    """
    dataframe["Ob__rdfs:comment"] = dataframe["Ob__rdfs:comment"].apply(lambda x: str(x).split("Vs.: ")[-1] if pd.notna(x) else pd.NA)
    dataframe["Ob__rdfs:comment"] = dataframe["Ob__rdfs:comment"].apply(lambda x: str(x).split("Obv.: ")[-1] if pd.notna(x) else pd.NA)
    dataframe["Ob__rdfs:comment"] = dataframe["Ob__rdfs:comment"].apply(lambda x: str(x).split("Av.: ")[-1] if pd.notna(x) else pd.NA)
    dataframe["Ob__rdfs:comment"] = dataframe["Ob__rdfs:comment"].apply(lambda x: str(x).split("Obv: ")[-1] if pd.notna(x) else pd.NA)
    dataframe["Ob__rdfs:comment"] = dataframe["Ob__rdfs:comment"].apply(lambda x: str(x).split("Ob: ")[-1] if pd.notna(x) else pd.NA)

    dataframe["Ob__rdfs:comment"] = dataframe["Ob__rdfs:comment"].apply(lambda x: str(x).split("Rev.: ")[0] if pd.notna(x) else pd.NA)
    dataframe["Ob__rdfs:comment"] = dataframe["Ob__rdfs:comment"].apply(lambda x: str(x).split("Rs.: ")[0] if pd.notna(x) else pd.NA)
    dataframe["Ob__rdfs:comment"] = dataframe["Ob__rdfs:comment"].apply(lambda x: str(x).split("Rev: ")[0] if pd.notna(x) else pd.NA)
    dataframe["Ob__rdfs:comment"] = dataframe["Ob__rdfs:comment"].apply(lambda x: str(x).split("Revers: ")[0] if pd.notna(x) else pd.NA)

    dataframe["Ob__rdfs:comment"] = dataframe["Ob__rdfs:comment"].apply(lambda x: pd.NA if "Rs." in str(x) or pd.isna(x) else str(x))
    dataframe["Ob__rdfs:comment"] = dataframe["Ob__rdfs:comment"].apply(lambda x: pd.NA if "Res." in str(x) or pd.isna(x) else str(x))

    # dataframe["Ob__rdfs:comment"] = dataframe["Ob__rdfs:comment"].apply(lambda x: "".join(str(x).splitlines()) if pd.notna(x) else pd.NA)
    dataframe["Ob__rdfs:comment"] = dataframe["Ob__rdfs:comment"].apply(lambda x: str(x).replace(";", "|") if pd.notna(x) else pd.NA)
    return dataframe


def remove_wrong_context_from_reverse(dataframe : pd.DataFrame) -> pd.DataFrame:
    """
        Removes obverse context from reverse.
    
        Parameters:
        -----------
        dataframe : pd.DataFrame
            Dataframe which should be updated
    """
    dataframe["Re__rdfs:comment"] = dataframe["Re__rdfs:comment"].apply(lambda x: str(x).split("Rev.: ")[-1] if pd.notna(x) else pd.NA)
    dataframe["Re__rdfs:comment"] = dataframe["Re__rdfs:comment"].apply(lambda x: str(x).split("Rs.: ")[-1] if pd.notna(x) else pd.NA)
    dataframe["Re__rdfs:comment"] = dataframe["Re__rdfs:comment"].apply(lambda x: str(x).split("Rev: ")[-1] if pd.notna(x) else pd.NA)
    dataframe["Re__rdfs:comment"] = dataframe["Re__rdfs:comment"].apply(lambda x: str(x).split("Revers: ")[-1] if pd.notna(x) else pd.NA)

    dataframe["Re__rdfs:comment"] = dataframe["Re__rdfs:comment"].apply(lambda x: str(x).split("Vs.: ")[0] if pd.notna(x) else pd.NA)
    dataframe["Re__rdfs:comment"] = dataframe["Re__rdfs:comment"].apply(lambda x: str(x).split("Obv.: ")[0] if pd.notna(x) else pd.NA)
    dataframe["Re__rdfs:comment"] = dataframe["Re__rdfs:comment"].apply(lambda x: str(x).split("Av.: ")[0] if pd.notna(x) else pd.NA)
    dataframe["Re__rdfs:comment"] = dataframe["Re__rdfs:comment"].apply(lambda x: str(x).split("Obv: ")[0] if pd.notna(x) else pd.NA)
    dataframe["Re__rdfs:comment"] = dataframe["Re__rdfs:comment"].apply(lambda x: str(x).split("Ob: ")[0] if pd.notna(x) else pd.NA)

    dataframe["Re__rdfs:comment"] = dataframe["Re__rdfs:comment"].apply(lambda x: pd.NA if "Ob." in str(x) or pd.isna(x) else str(x))
    dataframe["Re__rdfs:comment"] = dataframe["Re__rdfs:comment"].apply(lambda x: pd.NA if "Obv." in str(x) or pd.isna(x) else str(x))

    # dataframe["Re__rdfs:comment"] = dataframe["Re__rdfs:comment"].apply(lambda x: "".join(str(x).splitlines()) if pd.notna(x) else pd.NA)
    dataframe["Re__rdfs:comment"] = dataframe["Re__rdfs:comment"].apply(lambda x: str(x).replace(";", "|") if pd.notna(x) else pd.NA)
    return dataframe


def change_gYear_format(dataframe : pd.DataFrame) -> pd.DataFrame:
    """
        Takes float entries of gyear columns and change them to int.
    
        Parameters:
        -----------
        dataframe : pd.DataFrame
            Dataframe which should be updated
    """
    col_list = [col for col in dataframe.columns if "^^xsd:gYear" in str(col)]
    for column in col_list:
        dataframe[column] = dataframe[column].apply(lambda x: int(x) if pd.notna(x) else pd.NA)

    return dataframe


def replace_uncertainties_with_random_certainties(dataframe : pd.DataFrame) -> pd.DataFrame:
    """
        Replaces all not-null-entries in the columns with "^^certainty" with pseudo random values between 0 and 1.
    
        Parameters:
        -----------
        dataframe : pd.DataFrame
            Dataframe which should be updated
    """
    for column in dataframe.columns:
        if "^^certainty" in column:
            reference = str(column).split("__")[0]
            for reference_column in dataframe.columns:
                if ("**" + reference) in reference_column:
                    dataframe[column] = dataframe[[column,reference_column]].apply(lambda x: ";".join(["%.2f" % random() for _ in str(x[1]).split(";")]) if pd.notna(x[0]) else pd.NA, axis=1)
                    dataframe[column] = dataframe[column].apply(lambda x: "; ".join([str("%.2f" % (float(e) / sum([float(i) + 0.001 for i in str(x).split(";")]))) for e in str(x).split(";")]) if pd.notna(x) and len(str(x).split(";")) > 1 else x)
                    break
    return dataframe


def remove_datetimes(dataframe : pd.DataFrame) -> pd.DataFrame:
    """
        Remove all columns with "^^xsd:gYear".
    
        Parameters:
        -----------
        dataframe : pd.DataFrame
            Dataframe which should be updated
    """
    dataframe = dataframe.drop([column for column in dataframe.columns if "^^xsd:gYear" in column], axis=1)
    dataframe = dataframe.drop([column for column in dataframe.columns if ("DF__" in column) or ("DT__" in column)], axis=1)
    
    return dataframe


def remove_uncertainties(dataframe : pd.DataFrame) -> pd.DataFrame:
    """
        Remove all columns with "^^certainty".
    
        Parameters:
        -----------
        dataframe : pd.DataFrame
            Dataframe which should be updated
    """
    dataframe = dataframe.drop([column for column in dataframe.columns if "^^certainty" in column], axis=1)
    
    return dataframe

def remove_corrosion_legend_without_obreverse(dataframe : pd.DataFrame) -> pd.DataFrame:
    """
        Remove all corrosions and legends, without a ob- or reverse.
    
        Parameters:
        -----------
        dataframe : pd.DataFrame
            Dataframe which should be updated
    """
    old_dataframe = dataframe
    plans = {str(subject).split("**")[1] : subject for subject in dataframe.columns if len(str(subject).split("**")) > 1}
    print(plans)
    for key, subject in plans.items():
        for column in (col for col in dataframe.columns if f"{key}__" in col):
            dataframe[column] = dataframe[[subject,column]].apply(lambda x: x[1] if pd.notna(x[0]) else pd.NA, axis=1)
    
    if not old_dataframe.equals(dataframe):
        return remove_corrosion_legend_without_obreverse(dataframe)

    return dataframe


def run_pipeline_on_dataframe(dataframe : pd.DataFrame) -> pd.DataFrame:
    """
        Takes float entries of gyear columns and change them to int.
    
        Parameters:
        -----------
        dataframe : pd.DataFrame
            Dataframe which should be updated
    """
    dataframe = change_afe_coin_id(dataframe)
    dataframe = change_findspot(dataframe)
    dataframe = turn_nomisma_values_to_uris(dataframe)
    dataframe = combine_mint_and_denomination(dataframe)
    dataframe = remove_wrong_context_from_obverse(dataframe)
    dataframe = remove_wrong_context_from_reverse(dataframe)
    dataframe = simplify_all_id_columns(dataframe)
    dataframe = change_gYear_format(dataframe)
    dataframe = remove_corrosion_legend_without_obreverse(dataframe)
    dataframe = replace_uncertainties_with_random_certainties(dataframe)
    dataframe = remove_datetimes(dataframe)


    dataframe.to_csv(Path(UNCO_PATH,"tests/testdata/afe/afe_ready.csv"),index=False)
    remove_uncertainties(dataframe).sample(n=100).to_csv(Path(UNCO_PATH,"tests/testdata/afe/afemapping_changed_100rows.csv"),index=False)

    remove_uncertainties(dataframe).to_csv(Path(UNCO_PATH,"tests/testdata/afe/afe_noUn_ready.csv"),index=False)

    return dataframe


if __name__ == "__main__":
    from unco import UNCO_PATH
    from unco.data.rdf_data import RDFData
    from unco.features.graph_generator import GraphGenerator

    dataframe = pd.read_csv(Path(UNCO_PATH,"tests/testdata/afe/afe.csv"))

    dataframe = run_pipeline_on_dataframe(dataframe)

    print(dataframe)

    rdf_data = RDFData(dataframe)

    gg = GraphGenerator(rdf_data)

    gg.load_prefixes(str(Path(UNCO_PATH,"tests/testdata/afe/namespaces.csv")))

    gg.generate_solution(xml_format=False,solution_id=9)