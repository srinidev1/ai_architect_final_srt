from functools import lru_cache
import pandas as pd
from pathlib import Path
import json
import re

@lru_cache(maxsize=1)
def get_dataframe():
    current_file = Path(__file__).resolve()
    dataset_folder = current_file.parent.parent.parent / "data" / "natural_disasters"
    dataset_file =  dataset_folder / "1900_2021_DISASTERS.xlsx - emdat data.csv"
    df = pd.read_csv(dataset_file)
    #spaces in column names making query to fail
    df.columns = [
        re.sub(r'[^A-Za-z0-9_]', '', col.replace(" ", "_"))
        for col in df.columns
    ]

    return df


def query_events(query: str) -> str:
    """
    Query natural disaster events using a pandas query string.
    
    Args:
        query: A pandas query string e.g. "Year == 2010 and Disaster Type == 'Earthquake'"
    
    Returns:
        JSON string of matching disaster records 
    """
    df = get_dataframe()
    #results = df.query(query).head(25).to_dict(orient="records")
    results = df.query(query).to_dict(orient="records")

    if not results:
        return json.dumps({"message": "No records found for the given query", "data": []})
    
    return json.dumps({
        "count": len(results),
        "data": results
    })