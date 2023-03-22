from pymongo import MongoClient
from datetime import datetime

# MongoDB
client = MongoClient("mongodb://admin:admin@localhost:27017/")
db = client["crawl_data"]
col = db["otx"]
col2 = db["otx_id"]

a = datetime.now()


# save indicators to mongo, ioc2
def put_iocs_to_collection(iocs):
    for ioc in iocs:
        col.insert_one(
            {
                "timestamp": int(round(a.timestamp())),
                "type": ioc["type"],
                "data": ioc["data"],
            }
        )


# save pulse_id to mongo, ioc1
def find_and_put_pulses_to_collection(pulse):
    f = col.find_one({"pulse_id": pulse})
    if f is None:  # neu khong tim thay f
        col2.insert_one(
            {
                "pulse_id": pulse,
            }
        )
        return pulse
    else:
        return None
