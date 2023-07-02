import pandas as pd
from unco import UNCO_PATH
from pathlib import Path


afe = pd.read_csv(Path(UNCO_PATH,"tests/testdata/afe/afe_ready.csv"))

afe.describe(include=["object","float"]).to_csv(Path(UNCO_PATH,"tests/testdata/afe/afe_overview.csv"))
