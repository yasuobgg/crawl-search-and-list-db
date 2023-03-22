from OTXv2 import OTXv2
from otx import mongo_module as mongo
import os
from dotenv import load_dotenv

load_dotenv()

otx_api_key = os.environ.get('OTX_API_KEY')
otx = OTXv2(api_key=otx_api_key)


def find_all_indicators_and_save_to_mongo():
    # All types of searching for IOCs
    types = [
        "IOCs",
        "malware",
        "IP addresses",
        "Domains",
        "URLs",
        "File hashes",
        "Email addresses",
    ]
    iocs = []
    # Get all iocs of pulses found
    for type in types:  # browse each type in types[]
        results = otx.search_pulses(type, max_results=25)  # search for it pulses
        for result in results["results"]:  # browse each result in results field of the above pulses
            r = mongo.find_and_put_pulses_to_collection(result["id"])  # if pulse_id not exis in db, put to db and return pulse_id
                                                                        # if it already exis in db, not put and return None
            if r is not None:
                indicators = otx.get_pulse_indicators(result["id"])  # search for its indicators
                for (indicator) in indicators:  # browse each indicator and save it to list iocs
                    iocs.append(indicator)

    # browse each item in iocs above, set the item['type'] be the key
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
        grouped_list.append(
            {"type": type.replace("FileHash-", ""), "data": items}
        )  # the type key is set to the type of the IOC
        # the data is set to the list of indicator values

    # For loop to save all items to mongodb
    # for item in grouped_list:
    return grouped_list


def insert_to_collection():
    data = find_all_indicators_and_save_to_mongo()
    mongo.put_iocs_to_collection(data)

# insert_to_collection()