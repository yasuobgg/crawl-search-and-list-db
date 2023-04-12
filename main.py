#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# db lib
from pymongo import MongoClient

# local lib
from bazaar import api as api_bazaar
from otx import api as api_otx
from virustotal import api as api_vt
from virusshare import api as api_vs

# app lib
from sanic import Sanic
from sanic_cors import CORS
from sanic import json as sanic_json

# env lib
import os
from dotenv import load_dotenv

# Scheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

app = Sanic(__name__)
CORS(app)

load_dotenv()
con_str = os.environ.get("CONNECTION_STRING")
db_name = os.environ.get("DB_NAME")

# khai bao mongodb ,database, collection
client = MongoClient(con_str)
db = client.get_database(db_name)


def daily_crawl_and_post():
    api_bazaar.insert_to_collection()
    api_otx.insert_to_collection()
    api_vt.insert_to_collection()
    api_vs.vs_file_info()


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
            query = {f"data.attributes.{type}": {"$exists": True}}
            data = col.find(query)
        else:
            query = {f"data.{type}": {"$exists": True}}
            data = col.find(query)
        return sanic_json(
            [{"timestamp": item["timestamp"], "data": item["data"]} for item in data]
        )
    else:
        return sanic_json("wrong type or collection name")


# func to get data by type and timestamp from db
def find_type_timestamp_data(type, timestamp, col_name):
    if col_name == "bazaar" or col_name == "otx":
        col = db.get_collection(col_name)
        if col_name == "bazaar":
            type = type.upper()
        else:
            type = type
        data = col.find({"type": type, "timestamp": timestamp})
        # data = col.find({"timestamp": {"$gt": 20, "$lt": 30}})

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
            query = {
                f"data.attributes.{type}": {"$exists": True},
                "timestamp": timestamp,
            }
            data = col.find(query)
        else:
            query = {f"data.{type}": {"$exists": True}, "timestamp": timestamp}
            data = col.find(query)
        return sanic_json(
            [{"timestamp": item["timestamp"], "data": item["data"]} for item in data]
        )
    else:
        return sanic_json("wrong type or collection name")


# create app route to crawl data and post to db
@app.post("/api/v1")
def api_v1(request):
    my_query = request.json

    if len(my_query) == 1:
        api_name = my_query["source"]
        return post_data(api_name)

    elif len(my_query) == 2:
        api_name = my_query["source"]
        number = my_query["number"]
        api_vs.find_md5_and_insert(number)
        return sanic_json("inserted successful!")


# create app route to get data from db
@app.post("/api/v2")
def api_v2(request):
    my_query = request.json

    if len(my_query) == 1:  # get all data
        col_name = my_query["source"]
        return db_data(col_name)

    elif len(my_query) == 2:  # get data by type
        col_name = my_query["source"]
        type_query = my_query["type"]
        return find_type_data(type=type_query, col_name=col_name)

    elif len(my_query) == 3:
        col_name = my_query["source"]
        type_query = my_query["type"]
        timestamp = my_query["timestamp"]
        return find_type_timestamp_data(
            type=type_query, timestamp=timestamp, col_name=col_name
        )


# schedule everyday at 7 AM
scheduler = BackgroundScheduler()
trigger = CronTrigger(year="*", month="*", day="*", hour="7", minute="0", second="0")
scheduler.add_job(
    daily_crawl_and_post,  # takes ~40 min <<<
    trigger=trigger,
    name="daily pull",
)
scheduler.start()


if __name__ == "__main__":
    # daily_crawl_and_post() # it takes ~ 40 min to run this function <<<
    app.run(host="0.0.0.0", port=5505, debug=True, auto_reload=True)
