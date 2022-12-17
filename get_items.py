from bs4 import BeautifulSoup as bs
import requests
import json

URL = 'https://terraria.fandom.com/wiki/Item_IDs_{}-{}'


list=[]
for i in range(1, 5402, 200):
    url = URL.format(i, i+199)
    webpage = requests.get(url)
    soup = bs(webpage.content, "html.parser")
    try: 
        f = soup.find('table')
        s=f.find_all('tr')
        for item in s:
            aux = item.find_all('td')
            for j in aux:
                list.append(j.text)
    except: 
        print('error in %s'%url)
        try: 
            url='https://terraria.fandom.com/wiki/IDs_601-800'
            webpage = requests.get(url)
            soup = bs(webpage.content, "html.parser")
            f = soup.find('table')
            s=f.find_all('tr')
            for item in s:
                aux = item.find_all('td')
                for j in aux:
                    list.append(j.text)
        except: print('another error')

terraria_dict ={}
for i in range(0, len(list), 3):
    terraria_dict.update({list[i]:[list[i+1], list[i+2]]})

print(terraria_dict)


with open('terrariaID.json', 'w') as out:
    json.dump(terraria_dict, out)