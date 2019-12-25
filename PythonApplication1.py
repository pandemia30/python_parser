
from bs4 import BeautifulSoup
import requests
import json
import re

url = 'https://www.dme.ru/shopping/shop/'
connect_string = "".join(re.findall('(https?://)?(www\.)?([-\w.]+)', url)[0])

def write(data: dict):
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def get_page(url: str):
    
    page = requests.get(url).text
    return BeautifulSoup(page, 'lxml')


def parse(page: BeautifulSoup):
    shops = {}

    
    received_data = (page.find('div', class_='shadows_left')
            .find('div', class_='shadows_right')
            .find('div', class_='layout')
            .find('div', class_='main')
            .find('div', class_='right_column')
            .find('div', class_='content')
            .find('div', class_='simple')
            .find('div', class_='simple')
            .find('div')
            .find('div'))

    received_data = received_data.findAll(['a', 'h2', 'p'])

    key_string = ''
    for item in received_data:
        if item.name == 'h2':
            shops.update({item.text: {'name': item.text, 'location': 'unknown', 'shops': []}})
            key_string = item.text

        elif key_string and item.name == 'p' and 'располож' in item.text:    
            pattern = re.compile('расположен[\w]?\s', re.IGNORECASE)
            shops[key_string]['location'] = re.split(pattern, item.text)[1]
        
        elif key_string and item.name == 'a' and item.text:
            shop_url = connect_string + (item.attrs["href"] if item.attrs['href'][0] == '/' else f'/{item.attrs["href"]}')
            shops[key_string]['shops'].append({'name': item.text, 'url': shop_url})

    return shops

page = get_page(url)
received_data = parse(page)
write(received_data)


