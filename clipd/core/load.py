from pathlib import Path
import pandas as pd

def load(file_path: str) -> pd.DataFrame:
    suffix = Path(file_path).suffix.lower()

    if suffix == '.csv':
        df = pd.read_csv(file_path)
    elif suffix in ['.xls', '.xlsx']:
        df = pd.read_excel(file_path)
    elif suffix == '.json':
        df = pd.read_json(file_path)
    elif suffix == '.parquet':
        df = pd.read_parquet(file_path)
    elif suffix in ['.h5', '.hdf5']:
        df = pd.read_hdf(file_path)
    elif suffix == '.feather':
        df = pd.read_feather(file_path)
    elif suffix == '.dta':
        df = pd.read_stata(file_path)
    elif suffix == '.sas7bdat':
        df = pd.read_sas(file_path)
    else:
        raise ValueError(f"Unsupported file type: {suffix}")
    return df
