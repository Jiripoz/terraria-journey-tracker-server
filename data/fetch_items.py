import requests
import json
import re
import hashlib
from src.log_setup import logger
import traceback


# logger.debug("Running fetch_items.py...")


# API = "https://terraria.fandom.com//api.php"
# API2 = "https://terraria.wiki.gg/api.php"

# PARAMS = {
#     "action": "cargoquery",
#     "format": "json",
#     "tables": "Items",
#     "fields": "itemid, name, internalname, imagefile, consumable, hardmode, type, tag, rare, tooltip, research",
#     "offset": 0,
#     "limit": 1000000000,
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

#         PARAMS["offset"] += 49
#         request = session.get(url=API, params=PARAMS)
#         DATA = request.json()
#         print(PARAMS["offset"])
#     except Exception as e:
#         print(e)
#         traceback.print_stack
#         break

# session = requests.Session()
# PARAMS["offset"] = 0
# request = session.get(url=API2, params=PARAMS)
# DATA = request.json()


# while DATA["cargoquery"] != []:
#     try:
#         for item in DATA["cargoquery"]:
#             item_dict = item["title"]
#             image_file = item_dict["imagefile"].replace(" ", "_")
#             hash = hashlib.md5(image_file.encode()).hexdigest()
#             item_url = f"https://terraria.wiki.gg/images/{hash[0]}/{hash[0]}{hash[1]}/{image_file}"
#             item_dict["imageUrl"] = item_url
#             final.append(item_dict)

#         PARAMS["offset"] += 49
#         request = session.get(url=API2, params=PARAMS)
#         DATA = request.json()
#         print(PARAMS["offset"])
#     except Exception as e:
#         print(e)
#         traceback.print_stack
#         break


# with open("data/raw_item.json", "w") as f:
#     json.dump(final, f, indent=4)

with open("data/raw_item.json", "r") as f:
    raw_items = json.load(f)

with open("data/items2.json", "r") as g:
    raw_items2 = json.load(g)


def search_duplicate_id(sub):
    id_list = []
    for item in sub:
        id_list.append(item["id"])
    duplicates = set(i for i in id_list if id_list.count(i) > 1)
    return duplicates


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
        return ""
    fclean = (
        tooltip.replace("&lt;span class=&quot;gameText&quot;&gt;", "")
        .replace("&lt;/span&gt;", "")
        .replace("&lt;br/&gt;", ". ")
        .replace(
            "&lt;span class=&quot;eico s i0 i1 i4 i7 i9 i10&quot; title=&quot;PC, Console, Mobile, Old Chinese, tModLoader and tModLoader 1.3-Legacy versions&quot;&gt;&lt;b&gt;&lt;/b&gt;&lt;i&gt;&lt;/i&gt;. Shows depth &lt;span class=&quot;eico s i2 i5 i8&quot; title=&quot;Old-gen console, Windows Phone and 3DS versions&quot;&gt;&lt;b&gt;&lt;/b&gt;&lt;i&gt;&lt;/i&gt;",
            "",
        )
        .replace(
            "&lt;span class=&quot;eico s i0 i1 i4 i9&quot; title=&quot;PC, Console, Mobile and tModLoader versions&quot;&gt;&lt;b&gt;&lt;/b&gt;&lt;i&gt;&lt;/i&gt;",
            "",
        )
        .replace(
            "&lt;span class=&quot;eico s i2 i5 i7 i10&quot; title=&quot;Old-gen console, Windows Phone, Old Chinese and tModLoader 1.3-Legacy versions&quot;&gt;&lt;b&gt;&lt;/b&gt;&lt;i&gt;&lt;/i&gt;",
            "",
        )
        .replace(
            "&lt;span class=&quot;eico s i0 i1 i4 i7 i9 i10&quot; title=&quot;PC, Console, Mobile, Old Chinese, tModLoader and tModLoader 1.3-Legacy versions&quot;&gt;&lt;b&gt;&lt;/b&gt;&lt;i&gt;&lt;/i&gt; . Opens one Gold Chest &lt;span class=&quot;eico s i2 i5 i8&quot; title=&quot;Old-gen console, Windows Phone and 3DS versions&quot;&gt;&lt;b&gt;&lt;/b&gt;&lt;i&gt;&lt;/i&gt;",
            "",
        )
        .replace(
            "&lt;span class=&quot;eico s i0 i1 i2 i4 i7 i9 i10&quot; title=&quot;PC, Console, Old-gen console, Mobile, Old Chinese, tModLoader and tModLoader 1.3-Legacy versions&quot;&gt;&lt;b&gt;&lt;/b&gt;&lt;i&gt;&lt;/i&gt; Can mine Mythril and Orichalcum. &lt;span class=&quot;eico s i5 i8&quot; title=&quot;Windows Phone and 3DS versions&quot;&gt;&lt;b&gt;&lt;/b&gt;&lt;i&gt;&lt;/i&gt; Can mine Mythril, Orichalcum, Adamantite, and Titanium",
            "",
        )
    )

    return fclean


def has_research(research):
    try:
        int(item["research"])
    except:
        return False
    return research != None


def check_internalName(internalName):
    if internalName == "EldMelter":
        return "ElfMelter"
    return internalName


new_item_dict = {}

added_ids: dict = {}
all_tags: list = []
for item in raw_items:
    if item["itemid"] == None or not has_research(item["research"]) or item["itemid"] in added_ids:
        continue

    item["tags"], prop_dict = transform_composite_labels(type_to_list(item["tag"]))
    new_item_dict[int(item["itemid"])] = {
        "id": int(item["itemid"]),
        "name": item["name"],
        "imagefile": item["imagefile"],
        "consumable": switch_to_boolean(item["consumable"]),
        "hardmode": switch_to_boolean(item["hardmode"]),
        "rare": item["rare"],
        "tooltip": clean_tooltip(item["tooltip"]),
        "research": int(item["research"]),
        "imageUrl": item["imageUrl"],
        "internalName": check_internalName(item["internalname"]),
        "tags": item["tags"],
        "category": type_to_list(item["type"]),
        "itemUrl": item["name"].replace(" ", "_"),
    }
    new_item_dict[int(item["itemid"])].update(prop_dict)

    added_ids[item["itemid"]] = True

for item in raw_items2:
    if item["id"] in added_ids:
        continue

    new_item_dict[int(item["id"])] = {
        "id": int(item["id"]),
        "name": item["name"],
        "imagefile": item["itemUrl"],
        "consumable": False,
        "hardmode": False,
        "rare": 0,
        "tooltip": "",
        "research": int(item["research"]),
        "imageUrl": item["imageUrl"],
        "internalName": item["internalName"],
        "tags": [],
        "category": type_to_list(item["category"]),
        "itemUrl": item["itemUrl"],
    }
    added_ids[item["id"]] = True


with open("data/items.json", "w") as h:
    json.dump(new_item_dict, h, indent=4)

logger.debug("Done! Items saved in data folder as items.json and raw_items.json")
