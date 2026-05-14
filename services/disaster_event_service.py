import os
from os import path
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from functools import lru_cache
from openai import AzureOpenAI
from utils.models import response_generator_llm,get_response_generator_llm_model
from datasets import load_dataset
#import pandas as pd
import kagglehub
import shutil
import json
from mcp_client.tool_executor import call_tool_sync

load_dotenv(override=True)

DATASET_FILENAME = "1900_2021_DISASTERS.xlsx - emdat data.csv"

QUERY_GENERATOR_PROMPT = """
    You are a query generator for disaster event data.
    Your task is to convert user requests into valid pandas query expressions.

    Rules:
    - Return ONLY the pandas query string.
    - Do not explain anything.
    - Available Columns:
        Year,Seq,Glide,Disaster_Group,Disaster_Subgroup,Disaster_Type,Disaster_Subtype,Disaster_Subsubtype,Event_Name,
        Country,ISO,Region,Continent,Location,Origin,Associated_Dis,Associated_Dis2,OFDA_Response,Appeal,Declaration,
        Aid_Contribution,Dis_Mag_Value,Dis_Mag_Scale,Latitude,Longitude,Local_Time,River_Basin,Start_Year,Start_Month,Start_Day,
        End_Year,End_Month,End_Day,Total_Deaths,No_Injured,No_Affected,No_Homeless,Total_Affected,Insured_Damages_000_US),
        Total_Damages_000_US),CPI,Adm_Level,Admin1_Code,Admin2_Code,Geo_Locations

    Examples:
    User: show floods in India after 2020
    Output:
    Country == 'India' and Disaster_Type == 'Flood' and Year >= 2020
"""

RESPONSE_SYSTEM_PROMPT = """
    You are a disaster event analyst.

    Summarize disaster event records returned from a dataset query.

    Rules:
    - Explain results clearly in plain English.
    - Mention count of records found.
    - Highlight important trends such as countries, years, deaths, or disaster types.
    - If no records found, say no matching events were found.

    Keep response concise but informative.

"""
def search_events(question: str, history: list[dict]) -> str:
    download_disaster_events()
    #convert to query
    query = nl_to_pandas_query(question).strip()

    #return query
    #call tool
    results = call_tool_sync("query_events", {"query": query})

    messagetoLLM = results.content[0].text

    #return results
    messages = [{"role": "system", "content": RESPONSE_SYSTEM_PROMPT}]
    for m in history:
        if m["role"] in ("user", "assistant"):
            messages.append({"role": m["role"], "content": m["content"]})
    messages.append({"role": "user", "content": messagetoLLM})

    response = response_generator_llm.chat.completions.create(
            messages=messages,            
            model=get_response_generator_llm_model()
    )    

    return response.choices[0].message.content
    #return f"Searching for events related to: {question} and query is : {query}"


def nl_to_pandas_query(question:str) -> str:
    messages = [{"role": "system", "content": QUERY_GENERATOR_PROMPT}]
    messages.append({"role": "user", "content": question})

    response = response_generator_llm.chat.completions.create(
            messages=messages,            
            model=get_response_generator_llm_model()
    )

    return response.choices[0].message.content

def download_disaster_events():
    """
      download the events csv file from kaggle and copy into project data folder if does not exists.
    """
    current_file = Path(__file__).resolve()
    dataset_folder = current_file.parent.parent / "data" / "natural_disasters"
    dataset_file =  dataset_folder / DATASET_FILENAME

    if not os.path.exists(dataset_file):
        #dataset = load_dataset("https://www.kaggle.com/datasets/brsdincer/all-natural-disasters-19002021-eosdis", data_files="1900_2021_DISASTERS.csv", split="train")
        cached_path = kagglehub.dataset_download("brsdincer/all-natural-disasters-19002021-eosdis")
        #print(f"Dataset downloaded to: {cached_path}")            
        #returned path is missing folder name DISASTERS
        cached_file = Path(cached_path) / "DISASTERS" / DATASET_FILENAME
        #copy to project folder, optional , copied to easily view data during dev
        shutil.copy(cached_file, dataset_folder)
    
