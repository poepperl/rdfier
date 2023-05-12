import pandas as pd
from pathlib import Path
from unco import UNCO_PATH

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
    dataframe["nmo:hasMint^^uri"] = dataframe["nmo:hasMint^^uri"] + dataframe["nmo:hasMint2^^uri"]
    dataframe["nmo:hasDenomination^^uri"] = dataframe["nmo:hasDenomination^^uri"].astype(str) + dataframe["nmo:hasDenomination2^^uri"]

    return dataframe


if __name__ == "__main__":
    dataframe = pd.read_csv(Path(UNCO_PATH,r"tests\testdata\afe\afemapping_1_public.csv"))

    dataframe = change_afe_coin_id(dataframe)
    dataframe = change_findspot(dataframe)
    dataframe = turn_nomisma_values_to_uris(dataframe)
    dataframe = combine_mint_and_denomination(dataframe)

    print(dataframe)
    dataframe.to_csv(Path(UNCO_PATH,r"tests\testdata\afe\afemapping_1_public_changed.csv"))