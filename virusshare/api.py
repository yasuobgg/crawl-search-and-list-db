import requests
from datetime import datetime
import time
from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()
con_str = os.environ.get("CONNECTION_STRING")
api_key = os.environ.get("VS_API_KEY")
db_name = os.environ.get("DB_NAME")
col_name = os.environ.get("VS_COL")
col_id_name = os.environ.get("VS_ID_COL")

# MongoDB
client = MongoClient(con_str)
db = client.get_database(db_name)
col_id_name = db.get_collection(col_id_name)
col_name = db.get_collection(col_name)


def find_md5_and_insert(id):
    a = datetime.now()

    # co 1 list cac file chua md5, thay '.../VirusShare_00463.md5' bang '.../VirusShare_00{i}.md5' voi i = 000,001,...00463

    url = f"https://virusshare.com/hashfiles/VirusShare_00{id}.md5"

    response = requests.get(url)
    response = response.text
    data = response.splitlines()
    temp = []

    for line in data[6:1006]:
        f = col_id_name.find_one({"MD5":line})
        if f is None:
            temp.append(line)
        else:
            pass

    col_id_name.insert_one({"timestamp": int(round(a.timestamp())), "MD5": temp})


def vs_file_info():
    a = datetime.now()
    tp = []
    for f in col_id_name.find():
        for i in range(len(f["MD5"])):
            tp.append(f["MD5"][i])
    while True:
        for md5 in tp[:100]:
            # print(md5)
            f = col_name.find_one({"data.md5": md5})
            if f is None:
                url = f"https://virusshare.com/apiv2/file?apikey={api_key}&hash={md5}"
                response = requests.get(url)
                try:
                    response_json = response.json()
                except requests.exceptions.JSONDecodeError:
                    response_json = ""

                col_name.insert_one(
                    {"timestamp": int(round(a.timestamp())), "data": response_json}
                )
                time.sleep(15)  # each minute can query 4 times :<
            else:
                pass
        break


# vs_file_info()
# col_name.delete_many({"timestamp":1679546283})
# print("done")
