#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# db lib
from pymongo import MongoClient

# local lib
from bazaar import api as api_bazaar
from otx import crawl_module as api_otx
from virustotal import api as api_vt
from virusshare import api as api_vs

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

# khai bao mongodb ,database, collection
client = MongoClient(con_str)
db = client.get_database(db_name)


#  func to post data to mongodb
def post_data(api_name):
    if api_name == "bazaar":
        api_bazaar.insert_to_collection()
    elif api_name == "otx":
        api_otx.insert_to_collection()
    elif api_name == "virustotal":
        api_vt.insert_to_collection()
    elif api_name == "virusshare":
        api_vs.vs_file_info()
    else:
        return sanic_json("wrong api name")
    return sanic_json("inserted successful!")


# func to get all data from db
def db_data(col_name):
    col = db.get_collection(col_name)
    data = col.find()
    if col_name == "bazaar" or col_name == "otx":
        return sanic_json(
            [
                {
                    "timestamp": item["timestamp"],
                    "type": item["type"],
                    "data": item["data"],
                }
                for item in data
            ]
        )
    elif col_name == "virustotal" or col_name == "virusshare":
        return sanic_json(
            [{"timestamp": item["timestamp"], "data": item["data"]} for item in data]
        )
    else:
        return sanic_json("wrong collection name")


# func to get data by type from db
def find_type_data(type, col_name):
    if col_name == "bazaar" or col_name == "otx":
        col = db.get_collection(col_name)
        if col_name == "bazaar":
            type = type.upper()
        else:
            type = type
        data = col.find({"type": type})
        return sanic_json(
            [
                {
                    "timestamp": item["timestamp"],
                    "type": item["type"],
                    "data": item["data"],
                }
                for item in data
            ]
        )
    elif col_name == "virustotal" or col_name == "virusshare":
        col = db.get_collection(col_name)
        if col_name == "virustotal":
            data = col.find({"data.attributes.type_description": type})
        else:
            data = data = col.find({"data.extension": type})
        return sanic_json(
            [{"timestamp": item["timestamp"], "data": item["data"]} for item in data]
        )
    else:
        return sanic_json("wrong type or collection name")


# create app route to post data
@app.post("/api/v1")
def api_v1(request):
    api_name = request.json.get("source")
    return post_data(api_name)


# run api of virusshare, find md5 ( from 001 to 463) and post to db
@app.post("/vs_api/v2")
def vs_api_md5(request):
    ftype = request.json.get("id")
    api_vs.find_md5_and_insert(ftype)
    return sanic_json("inserted successful!")


# create app route to get all data of a collection
@app.post("/all_data")
def all_data(request):
    col_name = request.json.get("source")
    return db_data(col_name)


# create app route to get all data by type of a collection
@app.post("/query_by_type")
def query_by_type(request):
    type = request.json.get("type")
    col_name = request.json.get("source")
    return find_type_data(type, col_name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5505, debug=True, auto_reload=True)
