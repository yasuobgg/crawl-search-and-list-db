import requests
from datetime import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import time

# get information from .env file
load_dotenv()
con_str = os.environ.get("CONNECTION_STRING")
api_key = os.environ.get("VT_API_KEY")
db_name = os.environ.get("DB_NAME")
col_name = os.environ.get("VT_COL")
col_get_data = os.environ.get("BAZAAR_COL")

# Mongodb
client = MongoClient(con_str)
db = client.get_database(db_name)
col = db.get_collection(col_name)
col_db = db.get_collection(col_get_data)

a = datetime.now()


def find_virustotal(sha256):
    url = f"https://www.virustotal.com/api/v3/files/{sha256}"
    data_headers = {"x-apikey": api_key}
    response = requests.get(url, headers=data_headers)
    response_json = response.json()
    try:
        response_json = response_json["data"]
        col.insert_one(
        {
            "timestamp": int(round(a.timestamp())),
            "data": response_json,
        }
    )
    except KeyError:
        pass  # if not found file hashed SHA256 in virustotal,response will not have field `data`
    
    time.sleep(5)


def insert_to_collection():
    cursor = col_db.find({"type": "SHA256"})
    for doc in cursor:
        for data in doc["data"]:
            dt = col.find_one({"data.id": data})
            if dt is None:
                find_virustotal(data)
            else:
                pass
