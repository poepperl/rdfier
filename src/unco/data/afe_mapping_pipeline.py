import pandas as pd
from pathlib import Path

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
    dataframe["nmo:hasMaterial^^uri"] = dataframe["nmo:hasMaterial^^uri"].apply(lambda x: "nm:"+str(x) if pd.notna(x) else pd.NA)
    dataframe["nmo:hasMint^^uri"] = dataframe["nmo:hasMint^^uri"].apply(lambda x: "nm:"+str(x) if pd.notna(x) else pd.NA)
    dataframe["nmo:hasMint2^^uri"] = dataframe["nmo:hasMint2^^uri"].apply(lambda x: "nm:"+str(x) if pd.notna(x) else pd.NA)
    dataframe["nmo:hasDenomination^^uri"] = dataframe["nmo:hasDenomination^^uri"].apply(lambda x: "nm:"+str(x) if pd.notna(x) else pd.NA)
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
    dataframe["nmo:hasMint^^uri"] = dataframe[["nmo:hasMint^^uri","nmo:hasMint2^^uri"]].apply(lambda x: "; ".join(x) if pd.notna(x[1]) and pd.notna(x[0]) else x[0], axis =1)
    dataframe["nmo:hasDenomination^^uri"] = dataframe[["nmo:hasDenomination^^uri","nmo:hasDenomination2^^uri"]].apply(lambda x: "; ".join(x) if pd.notna(x[1]) and pd.notna(x[0]) else x[0], axis =1)

    return dataframe.drop(["nmo:hasMint2^^uri","nmo:hasDenomination2^^uri"],axis=1)

def simplify_all_id_columns(dataframe : pd.DataFrame) -> pd.DataFrame:
    """
        All id values will be replaced with "1".
    
        Parameters:
        -----------
        dataframe : pd.DataFrame
            Dataframe which should be updated
    """
    dataframe["nmo:hasDie^^id**1"] = dataframe["nmo:hasDie^^id**1"].apply(lambda x: str(1) if pd.notna(x) else x)
    dataframe["nmo:hasObverse^^id**2"] = dataframe["nmo:hasObverse^^id**2"].apply(lambda x: str(1) if pd.notna(x) else x)
    dataframe["nmo:hasReverse^^id**3"] = dataframe["nmo:hasReverse^^id**3"].apply(lambda x: str(1) if pd.notna(x) else x)

    return dataframe

def remove_wrong_context_from_obverse(dataframe : pd.DataFrame) -> pd.DataFrame:
    """
        Removes reverse context from obverse.
    
        Parameters:
        -----------
        dataframe : pd.DataFrame
            Dataframe which should be updated
    """
    dataframe["2__nmo:hasContext"] = dataframe["2__nmo:hasContext"].apply(lambda x: str(x).split("Vs.: ")[-1] if pd.notna(x) else pd.NA)
    dataframe["2__nmo:hasContext"] = dataframe["2__nmo:hasContext"].apply(lambda x: str(x).split("Obv.: ")[-1] if pd.notna(x) else pd.NA)
    dataframe["2__nmo:hasContext"] = dataframe["2__nmo:hasContext"].apply(lambda x: str(x).split("Av.: ")[-1] if pd.notna(x) else pd.NA)
    dataframe["2__nmo:hasContext"] = dataframe["2__nmo:hasContext"].apply(lambda x: str(x).split("Obv: ")[-1] if pd.notna(x) else pd.NA)
    dataframe["2__nmo:hasContext"] = dataframe["2__nmo:hasContext"].apply(lambda x: str(x).split("Ob: ")[-1] if pd.notna(x) else pd.NA)

    dataframe["2__nmo:hasContext"] = dataframe["2__nmo:hasContext"].apply(lambda x: str(x).split("Rev.: ")[0] if pd.notna(x) else pd.NA)
    dataframe["2__nmo:hasContext"] = dataframe["2__nmo:hasContext"].apply(lambda x: str(x).split("Rs.: ")[0] if pd.notna(x) else pd.NA)
    dataframe["2__nmo:hasContext"] = dataframe["2__nmo:hasContext"].apply(lambda x: str(x).split("Rev: ")[0] if pd.notna(x) else pd.NA)
    dataframe["2__nmo:hasContext"] = dataframe["2__nmo:hasContext"].apply(lambda x: str(x).split("Revers: ")[0] if pd.notna(x) else pd.NA)

    dataframe["2__nmo:hasContext"] = dataframe["2__nmo:hasContext"].apply(lambda x: pd.NA if "Rs." in str(x) or pd.isna(x) else str(x))
    dataframe["2__nmo:hasContext"] = dataframe["2__nmo:hasContext"].apply(lambda x: pd.NA if "Res." in str(x) or pd.isna(x) else str(x))

    # dataframe["2__nmo:hasContext"] = dataframe["2__nmo:hasContext"].apply(lambda x: "".join(str(x).splitlines()) if pd.notna(x) else pd.NA)
    dataframe["2__nmo:hasContext"] = dataframe["2__nmo:hasContext"].apply(lambda x: str(x).replace(";", "|") if pd.notna(x) else pd.NA)
    return dataframe


def remove_wrong_context_from_reverse(dataframe : pd.DataFrame) -> pd.DataFrame:
    """
        Removes obverse context from reverse.
    
        Parameters:
        -----------
        dataframe : pd.DataFrame
            Dataframe which should be updated
    """
    dataframe["3__nmo:hasContext"] = dataframe["3__nmo:hasContext"].apply(lambda x: str(x).split("Rev.: ")[-1] if pd.notna(x) else pd.NA)
    dataframe["3__nmo:hasContext"] = dataframe["3__nmo:hasContext"].apply(lambda x: str(x).split("Rs.: ")[-1] if pd.notna(x) else pd.NA)
    dataframe["3__nmo:hasContext"] = dataframe["3__nmo:hasContext"].apply(lambda x: str(x).split("Rev: ")[-1] if pd.notna(x) else pd.NA)
    dataframe["3__nmo:hasContext"] = dataframe["3__nmo:hasContext"].apply(lambda x: str(x).split("Revers: ")[-1] if pd.notna(x) else pd.NA)

    dataframe["3__nmo:hasContext"] = dataframe["3__nmo:hasContext"].apply(lambda x: str(x).split("Vs.: ")[0] if pd.notna(x) else pd.NA)
    dataframe["3__nmo:hasContext"] = dataframe["3__nmo:hasContext"].apply(lambda x: str(x).split("Obv.: ")[0] if pd.notna(x) else pd.NA)
    dataframe["3__nmo:hasContext"] = dataframe["3__nmo:hasContext"].apply(lambda x: str(x).split("Av.: ")[0] if pd.notna(x) else pd.NA)
    dataframe["3__nmo:hasContext"] = dataframe["3__nmo:hasContext"].apply(lambda x: str(x).split("Obv: ")[0] if pd.notna(x) else pd.NA)
    dataframe["3__nmo:hasContext"] = dataframe["3__nmo:hasContext"].apply(lambda x: str(x).split("Ob: ")[0] if pd.notna(x) else pd.NA)

    dataframe["3__nmo:hasContext"] = dataframe["3__nmo:hasContext"].apply(lambda x: pd.NA if "Ob." in str(x) or pd.isna(x) else str(x))
    dataframe["3__nmo:hasContext"] = dataframe["3__nmo:hasContext"].apply(lambda x: pd.NA if "Obv." in str(x) or pd.isna(x) else str(x))

    # dataframe["3__nmo:hasContext"] = dataframe["3__nmo:hasContext"].apply(lambda x: "".join(str(x).splitlines()) if pd.notna(x) else pd.NA)
    dataframe["3__nmo:hasContext"] = dataframe["3__nmo:hasContext"].apply(lambda x: str(x).replace(";", "|") if pd.notna(x) else pd.NA)
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

if __name__ == "__main__":
    from unco import UNCO_PATH
    from unco.data.rdf_data import RDFData
    from unco.features.graph_generator import GraphGenerator

    dataframe = pd.read_csv(Path(UNCO_PATH,r"tests\testdata\afe\afemapping_1_public_withoutUncertainties.csv"))
    # dataframe = dataframe.drop([f"Unnamed: {numb}" for numb in range(39,54)],axis=1)

    dataframe = change_afe_coin_id(dataframe)
    dataframe = change_findspot(dataframe)
    dataframe = turn_nomisma_values_to_uris(dataframe)
    dataframe = combine_mint_and_denomination(dataframe)
    dataframe = remove_wrong_context_from_obverse(dataframe)
    dataframe = remove_wrong_context_from_reverse(dataframe)
    dataframe = simplify_all_id_columns(dataframe)
    dataframe = change_gYear_format(dataframe)

    print(dataframe)
    dataframe.to_csv(Path(UNCO_PATH,r"tests\testdata\afe\afemapping_1_public_changed.csv"))

    rdf_data = RDFData(dataframe)

    gg = GraphGenerator(rdf_data)

    gg.load_prefixes(str(Path(UNCO_PATH,r"tests\testdata\afe\namespaces.csv")))

    gg.generate_solution()
