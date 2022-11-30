from pathlib import Path

def write_df_as_paquet(df, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path)
