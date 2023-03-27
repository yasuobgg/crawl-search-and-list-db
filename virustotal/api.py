import requests
from datetime import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv

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


def insert_to_collection():
    inf = col_db.find({"type": "SHA256"})

    my_sha256 = []
    for doc in inf:
        for data in doc["data"]:
            my_sha256.append(data)

    print(my_sha256)
    a = datetime.now()

    #  this script only query for filetypes that is hash sha256 in virustotal
    for file_type in my_sha256:
        # print(file_type)
        # file_type = '108086be0db84ea3c1be952a8b2dc9828b65efb21805f26f37c9c94825f8523ba'
        f = col.find_one({"data.id": file_type})
        if f is None:  # khong tim thay f
            url = f"https://www.virustotal.com/api/v3/files/{file_type}"
            data_headers = {"x-apikey": api_key}
            # print(url)
            # print(type(url))
            response = requests.get(url, headers=data_headers)
            response_json = response.json()
            try:
                response_json = response_json["data"]
            except KeyError:
                response_json = response_json
            col.insert_one(
                {
                    "timestamp": int(round(a.timestamp())),
                    # "type": response_json['data']['attributes']['type_description'],
                    "data": response_json,
                }
            )
        else:
            pass


# print("done!")
