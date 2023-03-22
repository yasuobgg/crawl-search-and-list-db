from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
con_str = os.environ.get('CONNECTION_STRING')
api_key = os.environ.get('BAZAAR_API_KEY')
db_name = os.environ.get('DB_NAME')
col_name = os.environ.get('OTX_COL')
col_name_2 = os.environ.get('OTX_ID_COL')

# MongoDB
client = MongoClient(con_str)
db = client.get_database(db_name)
col = db.get_collection(col_name)
col2 = db.get_collection(col_name_2)

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
