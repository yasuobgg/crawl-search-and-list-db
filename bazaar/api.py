import requests
from datetime import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
con_str = os.environ.get("CONNECTION_STRING")
api_key = os.environ.get("BAZAAR_API_KEY")
db_name = os.environ.get("DB_NAME")
col_name = os.environ.get("BAZAAR_COL")

# MongoDB
client = MongoClient(con_str)
db = client.get_database(db_name)
col = db.get_collection(col_name)

a = datetime.now()


def getDataBazaar():
    file_types = ["exe", "zip", "ace", "7z", "elf", "js", "rar"]
    list1 = [
        {"type": "SHA256", "data": []},
        {"type": "SHA1", "data": []},
        {"type": "MD5", "data": []},
    ]
    for file_type in file_types:
        url = "https://mb-api.abuse.ch/api/v1/"
        data_query = {"query": "get_file_type", "file_type": file_type, "limit": 25}

        data_headers = {"API-KEY": api_key}

        response = requests.post(url, headers=data_headers, data=data_query)

        response_json = response.json()

        for data in response_json["data"]:
            r = col.find_one({"data": data["sha256_hash"]})
            if r is None:
                list1[0]["data"].append(data["sha256_hash"])
                list1[1]["data"].append(data["sha1_hash"])
                list1[2]["data"].append(data["md5_hash"])
            else:
                pass

    return list1


def insert_to_collection():
    my_data = getDataBazaar()

    for data in my_data:
        col.insert_one(
            {
                "timestamp": int(round(a.timestamp())),
                "type": data["type"],
                "data": data["data"],
            }
        )


# print("done!")
