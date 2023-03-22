# db lib
from pymongo import MongoClient

# local lib
from bazaar import api as api_bazaar
from otx import crawl_module as api_otx
from virustotal import api as api_vt

# app lib
from sanic import Sanic
from sanic_cors import CORS
from sanic import json as sanic_json

# env lib
import os
from dotenv import load_dotenv

app = Sanic(__name__)
CORS(app)

load_dotenv()
con_str = os.environ.get("CONNECTION_STRING")
db_name = os.environ.get("DB_NAME")
col_1 = os.environ.get("BAZAAR_COL")
col_2 = os.environ.get("OTX_COL")
col_3 = os.environ.get("VT_COL")

# khai bao mongodb ,database, collection
client = MongoClient(con_str)
db = client.get_database(db_name)


@app.post("/bazaar_api/v1")  # run api of bazaar folder, post data to db
def bazaar_api(request):
    api_bazaar.insert_to_collection()
    return sanic_json("inserted successful!")


@app.post("/otx_api/v1")  # run api of otx folder, post data to db
def otx_api(request):
    api_otx.insert_to_collection()
    return sanic_json("inserted successful!")


@app.post("/vt_api/v1")  # run api of virustotal folder, post data to api
def otx_api(request):
    api_vt.insert_to_collection()
    return sanic_json("inserted successful!")


@app.get("/bazaar_data")  # get all data from bazaar col and show
def bazaar_data(request):
    col = db.get_collection(col_1)
    data = col.find()
    return sanic_json(
        [
            {"timestamp": item["timestamp"], "type": item["type"], "data": item["data"]}
            for item in data
        ]
    )


@app.get("/otx_data")  # get all data from otx col and show
def otx_data(request):
    col = db.get_collection(col_2)
    data = col.find()
    return sanic_json(
        [
            {"timestamp": item["timestamp"], "type": item["type"], "data": item["data"]}
            for item in data
        ]
    )


@app.get("/vt_data")  # get all data from vt col and show
def otx_data(request):
    col = db.get_collection(col_3)
    data = col.find()
    return sanic_json(
        [{"timestamp": item["timestamp"], "data": item["data"]} for item in data]
    )


@app.post("/bazaar_data/type")  # get all data by type from bazaar col
def bazaar_data_type(request):
    ftype = request.json.get("type")
    ftype = ftype.upper()
    col = db.get_collection(col_1)
    data = col.find({"type": ftype})
    return sanic_json(
        [
            {"timestamp": item["timestamp"], "type": item["type"], "data": item["data"]}
            for item in data
        ]
    )


@app.post("/otx_data/type")  # get all data by type from otx col
def otx_data_type(request):
    ftype = request.json.get("type")
    ftype = ftype.upper()
    col = db.get_collection(col_2)
    data = col.find({"type": ftype})
    return sanic_json(
        [
            {"timestamp": item["timestamp"], "type": item["type"], "data": item["data"]}
            for item in data
        ]
    )


@app.post("/vt_data/type")  # get all data by type_description from vt col
def vt_data_type(request):
    ftype = request.json.get("type")
    # ftype = ftype.upper()
    # print(ftype)
    col = db.get_collection(col_3)
    data = col.find({"data.attributes.type_description": ftype})
    return sanic_json(
        [{"timestamp": item["timestamp"], "data": item["data"]} for item in data]
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5505, debug=True, auto_reload=True)
