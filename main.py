import json
import requests
from bs4 import BeautifulSoup
from tenacity import retry


headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"
}

urls = ['https://funpay.com/lots/436/', 'https://funpay.com/lots/437/', 'https://funpay.com/lots/967/', 'https://funpay.com/lots/908/']

def get_lots():
    data_dict = {}

    for url in urls:
        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        cards = soup.find_all('a', class_='tc-item')

        for i in cards:
            try:
                link = i.get('href').strip()
            except:
                link = None
            try:
                description = i.find('div', class_='tc-desc-text').text.strip()
            except:
                description = None
            try:
                price = i.find('div', class_='tc-price').text.strip()
            except:
                price = None

            lot_id = link.split('?id=')[-1]

            data_dict[lot_id] = {
                "link": link,
                "description": description,
                "price": price,

            }

    with open("all_data.json", "w", encoding="utf-8") as file:
        json.dump(data_dict, file, ensure_ascii=False, indent=4)


@retry()
def check_update():
    with open("all_data.json", encoding="utf-8") as file:
        all_data_dict = json.load(file)

    new_data_dict = {}

    for url in urls:
        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        cards = soup.find_all('a', class_='tc-item')

        for i in cards:
            link = i.get('href').strip()
            id = link.split('?id=')[-1]

            if id in all_data_dict:
                continue
            else:
                try:
                    link = i.get('href').strip()
                except:
                    link = None
                try:
                    description = i.find('div', class_='tc-desc-text').text.strip()
                except:
                    description = None
                try:
                    price = i.find('div', class_='tc-price').text.strip()
                except:
                    price = None

                all_data_dict[id] = {
                    "link": link,
                    "description": description,
                    "price": price,
                }

                new_data_dict[id] = {
                    "link": link,
                    "description": description,
                    "price": price,
                }

    with open("all_data.json", "w", encoding="utf-8") as file:
        json.dump(all_data_dict, file, ensure_ascii=False, indent=4)

    with open("new_data.json", "w", encoding="utf-8") as file:
        json.dump(new_data_dict, file, ensure_ascii=False, indent=4)

    return new_data_dict
