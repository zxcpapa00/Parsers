import requests
from bs4 import BeautifulSoup
import lxml
import fake_user_agent
import json
from random import randrange
from time import sleep

headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}

# persons_urls = []
#
# for i in range(0, 760, 20):
#     url = f'https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=20&noFilterSet=true&offset={i}'
#
#     q = requests.get(url)
#     result = q.content
#
#     soup = BeautifulSoup(result, 'lxml')
#     persons = soup.find_all(class_='bt-slide-content')
#
#     for item in persons:
#         person_url = item.find('a')
#         persons_urls.append(person_url.get('href'))
#
#
# with open('persons_urls.txt', 'a', encoding='utf-8') as file:
#     for line in persons_urls:
#         file.write(f'{line}\n')

with open('persons_urls.txt', encoding='utf-8') as file:
    lines = [line.strip() for line in file.readlines()]

    data_dict = []
    count = 0

    for line in lines:
        q = requests.get(url=line)
        result = q.content

        soup = BeautifulSoup(result, 'lxml')
        person = soup.find(class_='bt-biografie-name').find('h3').text
        person_name_company = person.strip().split(',')
        name = person_name_company[0]
        company = person_name_company[1].strip()

        social_network = soup.find_all(class_='bt-link-extern')

        social_network_urls = []

        for url in social_network:
            social_network_urls.append(url.get('href'))

        data = {
            'Person': name,
            'Company': company,
            'SocialNetworks': social_network_urls
        }

        count+=1
        sleep(random.randrange(2, 4))
        print(f'#Выполнено {count} итераций')
        data_dict.append(data)

        with open('data.json', 'w') as file:
            json.dump(data_dict, file, indent=4)