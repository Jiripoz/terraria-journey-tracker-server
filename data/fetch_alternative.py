import requests
from bs4 import BeautifulSoup
import json


url = "https://terraria.wiki.gg/wiki/Alternative_crafting_ingredients"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

a = soup.find_all(class_="terraria")

alternative = {}

for item in a:
    elements = item.find_all("li")
    key = str(item.previous_element.previous_element)
    loi = []  # list of itens
    for e in elements:
        try:
            f = e.find_all(class_="i")

            for i in f:
                string = i.find(class_="id").text.replace("Internal Item ID:", "")
                print(string)
                loi.append(string)
        except:
            continue
    alternative[key] = loi

print(alternative)

with open("alternative_db.json", "w") as f:
    json.dump(alternative, f, indent=4)
