import re
import pandas as pd
from os import environ
from sqlalchemy import create_engine, Engine
from sqlalchemy import URL
from rapidfuzz import fuzz
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

screening_app = FastAPI()

""" Define helper functions
"""

def get_engine() -> Engine:
    # Get environment variables
    HOST = environ["PG_HOST"]
    PORT = environ["PG_PORT"]
    DB_NAME = environ["PG_DB_NAME"]
    USER = environ["PG_USER"]
    PASS = environ["PG_PASS"]

    # Define connection string to PostgreSQL database
    connection_string = URL.create(
        drivername="postgresql+psycopg2",
        database=DB_NAME,
        host=HOST,
        port=PORT,
        username=USER,
        password=PASS
    )

    # Create engine object 
    engine = create_engine(url=connection_string)

    return engine

def clean_name(raw_name: str) -> str:
    clean_name = re.sub("[/-]", " ", raw_name).upper() # replace /- with spaces; convert to upper case
    clean_name = re.sub("[^A-Z0-9\\s]", "", clean_name) # get only alphanumeric and spaces
    clean_name = re.sub("\\s+", " ", clean_name).strip() # remove multiple consecutive spaces 
    return clean_name

def get_ratio(s1: str, s2: str, sort_names: bool = False) -> float | None:
    # Sort names if specified
    if sort_names:
        s1 = " ".join(sorted(s1.split(" ")))
        s2 = " ".join(sorted(s2.split(" ")))

    # Return None on error 
    try:
        return round(fuzz.ratio(s1, s2) / 100, 4)
    except:
        return None

def get_sanctions() -> pd.DataFrame:
    engine = get_engine()
    return pd.read_sql("SELECT * FROM ofac_consolidated", engine)

def screen(name: str, threshold: float = 0.7) -> list:
    cleaned_name = clean_name(name)
    sanctions = get_sanctions()
    sanctions["score"] = sanctions["cleaned_names"].apply(get_ratio, args=(cleaned_name,))
    sanctions_filtered = sanctions[sanctions["score"]>=threshold]
    sanctions_filtered["input_name"] = name
    results = sanctions_filtered.fillna(value="-").to_dict(orient="records")
    return results

def get_base_response(status: str, data: list, error_message: str = None) -> dict:
    base_response = {"status": status}
    if error_message:
        base_response["error_message"] = error_message
        return base_response
    
    base_response["results"] = data
    return base_response

""" Define routes
"""

@screening_app.get("/")
def home():
    return get_base_response(
        "success",
        {
            "App Title": "Simple Screening API",
            "Version": "0.0.1"
        }
    )


@screening_app.get("/screen")
def screen_name(name: str, threshold: float = 0.7):
    results = []
    _names = name.split(",")

    for _name in _names:
        results.extend(screen(_name, threshold))

    return get_base_response("success", results)