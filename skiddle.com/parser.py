import requests
from bs4 import BeautifulSoup
import json

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}

# Все ссылки
fests_url = []
# for o in range(0, 288, 24):
for o in range(0, 192, 24):
    url = f'https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=5%20May%202023&to_date=&maxprice=500&o={o}&bannertitle=May'
    q = requests.get(url=url, headers=headers)
    json_data = json.loads(q.text)
    html_response = json_data['html']

    with open(f'index_{o}.html', 'w') as file:
        file.write(html_response)

    with open(f'index_{o}.html') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    cards = soup.find_all('a', class_='card-details-link')

    for item in cards:
        fest_url = 'https://www.skiddle.com/' + item.get('href')
        fests_url.append(fest_url)


#Собираем информацию о фестивале
fest_list_result = []
count = 0
for url in fests_url:
    count += 1
    print('#', count, url)
    req = requests.get(url=url, headers=headers).text
    try:
        soup = BeautifulSoup(req, 'lxml')
        fest_info_block = soup.find('div',class_='top-info-cont')

        fest_name = fest_info_block.find('h1').text.strip()
        fest_date = fest_info_block.find('h3').text.strip()
        fest_location_url = 'https://www.skiddle.com/' + fest_info_block.find('a', class_='tc-white').get('href')

        # Собираем контактные данные
        req = requests.get(url=fest_location_url, headers=headers).text
        soup = BeautifulSoup(req, 'lxml')

        contact_details = soup.find('h2', string='Venue contact details and info').find_next()
        items = [item.text for item in contact_details.find_all('p')]

        contact_details_dict = {}
        for contact_details in items:
            contact_details_list = contact_details.split(':')

            if len(contact_details_list) == 3:
                contact_details_dict[contact_details_list[0].strip()] = contact_details_list[1].strip() + ':' + contact_details_list[2].strip()

            else:
                contact_details_dict[contact_details_list[0].strip()] = contact_details_list[1].strip()

        fest_list_result.append(
            {
                'Fest name': fest_name,
                'Fest date': fest_date,
                'Contacts data': contact_details_dict
            }
        )

    except Exception as ex:
        print(ex)
        print('Ошибка')

with open('fest_list_result', 'w') as file:
    json.dump(fest_list_result, file, indent=4, ensure_ascii=False)


