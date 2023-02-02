import requests
import json
import re
import hashlib
from src.log_setup import logger
import traceback


# logger.debug("Running fetch_items.py...")


# API = "https://terraria.wiki.gg//api.php"

# PARAMS = {
#     "action": "cargoquery",
#     "format": "json",
#     "tables": "Items",
#     "fields": "itemid, name, internalname, imagefile, consumable, hardmode, type, tag, rare, tooltip, research",
#     "offset": 0,
# }


# session = requests.Session()
# request = session.get(url=API, params=PARAMS)
# DATA = request.json()
# final = []

# while DATA["cargoquery"] != []:
#     try:
#         for item in DATA["cargoquery"]:
#             item_dict = item["title"]
#             image_file = item_dict["imagefile"].replace(" ", "_")
#             hash = hashlib.md5(image_file.encode()).hexdigest()
#             item_url = f"https://terraria.wiki.gg/images/{hash[0]}/{hash[0]}{hash[1]}/{image_file}"
#             item_dict["imageUrl"] = item_url
#             final.append(item_dict)
#             print(f"o item url é {item_url}")

#         PARAMS["offset"] += 50
#         request = session.get(url=API, params=PARAMS)
#         DATA = request.json()

#     except Exception as e:
#         print(e)
#         traceback.print_stack
#         break


# with open("data/raw_item.json", "w") as f:
#     json.dump(final, f, indent=4)

with open("data/raw_item.json", "r") as f:
    raw_items = json.load(f)


def switch_to_boolean(obj):
    return obj != None


def type_to_list(types):
    if types == None or len(types) == 0:
        return []
    pieces = [x.lower() for x in types.split("^")]
    return pieces


def merge_dicts(dict_list):
    merged: dict = {}
    for dictionary in dict_list:
        for key in dictionary:
            if key not in merged:
                merged[key] = [dictionary[key]]
            else:
                merged[key].append(dictionary[key])

    return merged


def transform_composite_labels(lst):
    new_props = [x for x in lst if ":" in x]
    tags = [y for y in lst if ":" not in y and y not in ["plunder", "vendor", "during"]]

    def map_composite_to_dict(s):
        parts = re.split(":", s)
        nprops: dict = {}
        nprops[parts[0]] = parts[1]
        return nprops

    prop_list = list(map(map_composite_to_dict, new_props))
    return tags, merge_dicts(prop_list)


def clean_tooltip(tooltip):
    if tooltip == None:
        return
    fclean = (
        tooltip.replace("&lt;span class=&quot;gameText&quot;&gt;", "")
        .replace("&lt;/span&gt;", "")
        .replace("&lt;br/&gt;", ". ")
    )

    return fclean


all_tags = []
final: list = []
for item in raw_items:
    if item["itemid"] == None:
        continue
    item["id"] = item["itemid"]
    item["internalName"] = item["internalname"]

    item["hardmode"] = switch_to_boolean(item["consumable"])
    item["consumable"] = switch_to_boolean(item["consumable"])
    item["type"] = type_to_list(item["type"])
    item["tags"], prop_dict = transform_composite_labels(type_to_list(item["tag"]))
    item["tooltip"] = clean_tooltip(item["tooltip"])
    item.update(prop_dict)
    all_tags.extend(type_to_list(item["tag"]))
    item["category"] = item["type"]

    del item["tag"]
    del item["itemid"]
    del item["type"]
    del item["internalname"]
    final.append(item)


with open("data/items.json", "w") as g:
    json.dump(final, g, indent=4)

logger.debug("Done! Items saved in data folder as items.json and raw_items.json")
