from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
from OTXv2 import OTXv2


load_dotenv()
con_str = os.environ.get("CONNECTION_STRING")
api_key = os.environ.get("OTX_API_KEY")
db_name = os.environ.get("DB_NAME")
col_name = os.environ.get("OTX_COL")
col_name_2 = os.environ.get("OTX_ID_COL")

# MongoDB
client = MongoClient(con_str)
db = client.get_database(db_name)
col = db.get_collection(col_name)
col2 = db.get_collection(col_name_2)

a = datetime.now()


# save indicators to mongo, col
def save_iocs(iocs):
    for ioc in iocs:
        col.insert_one(
            {
                "timestamp": int(round(a.timestamp())),
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


otx_api_key = os.environ.get("OTX_API_KEY")
otx = OTXv2(api_key=otx_api_key)


def find_iocs():
    # All types of searching for IOCs
    types = [
        "iocs",
        "malware",
        "ip addresses",
        "domains",
        "urls",
        "file hashes",
        "email addresses",
    ]
    iocs = []
    # Get all iocs of pulses found
    for type in types:  # browse each type in types[]
        results = otx.search_pulses(type, max_results=25)
        # browse each result in results field of the above pulses
        for result in results["results"]:
            r = save_pulses_id(result["id"])
            # if pulse_id not exis in db, put to db and return True
            # if it already exis in db, not put and return False
            if r:
                # search for its indicators
                indicators = otx.get_pulse_indicators(result["id"])
                # browse each indicator and save it to list iocs
                for indicator in indicators:
                    iocs.append(indicator)

    # browse each item in iocs above, set the item['type'] be the key `type`
    grouped_dict = {}
    for item in iocs:
        type = item["type"]
        if (
            type in grouped_dict
        ):  # if type is already a key in dict, append the 'indicator' filed to this key
            grouped_dict[type].append(item["indicator"])
        else:  # if type is not a key in dict, create a new key with this type and sets its value to a new list containing the indicator value
            grouped_dict[type] = [item["indicator"]]

    # using the `items()` method to store data in a more user-firendly format
    grouped_list = []
    for type, items in grouped_dict.items():
        grouped_list.append({"type": type.replace("FileHash-", ""), "data": items})
        # the type key is set to the type of the IOC
        # the data is set to the list of indicator values

    return grouped_list


def insert_to_collection():
    data = find_iocs()
    save_iocs(data)


# insert_to_collection()
