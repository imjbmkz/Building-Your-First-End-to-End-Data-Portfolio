import json
import time
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
        ftp.storbinary(f"STOR {file_name}", fp)

def read_csv(config: dict) -> pd.DataFrame:
    url = config["URL"]
    params = config["PARAMS"]
    return pd.read_csv(url, **params)

def pipeline():
    # Load source configuration
    with open("config.json", "rb") as fp:
        config = json.load(fp)

    ftp = get_ftp()

    # Loop through each source config
    for name, source in config.items():
        # Download the file and save as CSV
        file_name = f"{name}.csv"
        df = read_csv(source)
        df.to_csv(file_name,index=False)

        # Upload to FTP
        upload_to_ftp(ftp, file_name)

        # Delete file
        remove(file_name)

        print(f"{file_name} has been uploaded to FTP.")

if __name__=="__main__":

    schedule.every().day.at("22:23").do(pipeline)

    while True:
        schedule.run_pending()
        time.sleep(1)