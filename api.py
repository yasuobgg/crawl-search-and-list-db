# mongodb lib
from pymongo import MongoClient

# basic lib
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# OTX lib
from OTXv2 import OTXv2

# load information from .env file
load_dotenv()
con_str = os.environ.get("CONNECTION_STRING")
api_key = os.environ.get("OTX_API_KEY")
db_name = os.environ.get("DB_NAME")
col_name = os.environ.get("OTX_COL")
col_name_2 = os.environ.get("OTX_ID_COL")

# Define MongoDB
client = MongoClient(con_str)
db = client.get_database(db_name)
col = db.get_collection(col_name)
col2 = db.get_collection(col_name_2)

# Define OTX api
otx_api_key = os.environ.get("OTX_API_KEY")
otx = OTXv2(api_key=otx_api_key)


# save indicators to mongo, col
def save_iocs(iocs):
    for ioc in iocs:
        col.insert_one(
            {
                "timestamp": int(round(datetime.datetime.now().timestamp())),
                "type": ioc["type"],
                "data": ioc["data"],
            }
        )


# save pulse_id to mongo, col2
def save_pulses_id(pulse):
    f = col2.find_one({"pulse_id": pulse})
    if f is None:  # neu khong tim thay f
        col2.insert_one(
            {
                "pulse_id": pulse,
            }
        )
        return True
    else:
        return False


def group_data(iocs):
    grouped_dict = {}

    for item in iocs:
        type = item["type"]
        if type in grouped_dict:
            # if type is already a key in dict, append the 'indicator' filed to this key
            grouped_dict[type].append(item["indicator"])
        else:
            # if type is not a key in dict, create a new key with this type and sets its value to a new list containing the indicator value
            grouped_dict[type] = [item["indicator"]]

    grouped_list = []

    # using the `items()` method to store data in a more user-firendly format
    for type, items in grouped_dict.items():
        grouped_list.append({"type": type.replace("FileHash-", ""), "data": items})

    return grouped_list


def find_iocs():
    timer = (datetime.now() - timedelta(days=1)).isoformat()  
    # timer = now - 1 day (query from previous day -> now)
    
    mydata = otx.getsince(timer, max_page=100)

    iocs = []

    for data in mydata:
        not_exis = save_pulses_id(data["id"])
        if not_exis:
            indicators = otx.get_pulse_indicators(data["id"])
            for indicator in indicators:
                iocs.append(indicator)
        else:
            pass

    group_data(iocs)


def insert_to_collection():
    data = find_iocs()
    save_iocs(data)


insert_to_collection()
