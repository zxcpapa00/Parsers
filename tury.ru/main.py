import requests
from bs4 import BeautifulSoup
import lxml
import json

def get_data(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
    }

    req = requests.get(url=url, headers=headers).text

    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(req)

    with open('index.html', 'r', encoding='utf-8') as file:
        src = file.read()

    hotel_info = []
    for i in range(0, 40, 20):
        url = f'https://tury.ru/hotel/?cn=0&ct=0&cat=1317&txt_geo=&srch=&s={i}'
        src = requests.get(url=url, headers=headers).text

        soup = BeautifulSoup(src, 'lxml')
        hotel_block = soup.find('div', class_='reviews-travel__column')

        hotel_names = hotel_block.find_all('div', class_='h4')
        names = []
        for name in hotel_names:
            hotel_name = name.text
            names.append(hotel_name)


        hotel_locations = hotel_block.find_all('div', class_='reviews-travel__tag tag flex')
        locations = []
        for location in hotel_locations:
            hotel_location = location.text.strip()
            locations.append(hotel_location)

        urls = []
        hotel_urls = hotel_block.find_all('a', class_='reviews-travel__title')
        for url in hotel_urls:
            urls.append(url.get('href'))

        for i in range(len(names)):
            info = {
                'Name': names[i][:-2].strip(),
                'Location': locations[i],
                'Stars': int(names[i][-3:-1].strip()) * '*',
                'URL': urls[i]
            }
            hotel_info.append(info)


    with open('result.json', 'a', encoding='utf-8') as file:
        json.dump(hotel_info, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    get_data('https://tury.ru/hotel/?cat=1317')