import sys
import json
import time
import concurrent.futures
import schedule
import pandas as pd
from os import environ, remove
from pathlib import Path
from ftplib import FTP_TLS

def get_ftp() -> FTP_TLS:
    # Get FTP details
    FTPHOST = environ["FTPHOST"]
    FTPUSER = environ["FTPUSER"]
    FTPPASS = environ["FTPPASS"]

    # Return authenticated FTP
    ftp = FTP_TLS(FTPHOST, FTPUSER, FTPPASS)
    ftp.prot_p()
    return ftp

def upload_to_ftp(ftp: FTP_TLS, file_to_upload: str):
    file_path = Path(file_to_upload)
    file_name = file_path.name

    # Upload file
    with open(file_path, "rb") as fp:
        ftp.storbinary(f"STOR ftp/new/{file_name}", fp)

def read_csv(config: dict) -> pd.DataFrame:
    url = config["URL"]
    params = config["PARAMS"]
    return pd.read_csv(url, **params)

def pipeline(source_config: dict):
    ftp = get_ftp()
    name = list(source_config.keys())[0]
    config = source_config[name]

    # Download the file and save as CSV
    file_name = f"{name}.csv"
    print(f"Downloading {file_name}.")
    df = read_csv(config)
    df.to_csv(file_name,index=False)

    # Upload to FTP
    upload_to_ftp(ftp, file_name)

    # Delete file
    remove(file_name)

    print(f"{file_name} has been uploaded to FTP.")

def parallel_execution():
    
    with open("config.json", "rb") as fp:
        config = json.load(fp)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(pipeline, config)

if __name__=="__main__":

    if sys.argv[1]=="manual":
        parallel_execution()

    elif sys.argv[1]=="schedule":
        schedule.every().day.at("22:23").do(parallel_execution)

        while True:
            schedule.run_pending()
            time.sleep(1)