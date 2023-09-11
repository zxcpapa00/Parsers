from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup
import lxml
import json


for i in range(1,2):
    url = f'https://www.avito.ru/kaliningrad/kvartiry/sdam/na_dlitelnyy_srok/2-komnatnye-ASgBAQICAkSSA8gQ8AeQUgFAzAgUkFk?p={i}&s=1'
    options = webdriver.ChromeOptions()
    service = Service('D:\\Python\\Projects\\parser\\project7\\driver')

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(1)

        with open('index.html', 'w', encoding='utf-8') as file:
            file.write(driver.page_source)

        with open('index.html', encoding='utf-8') as file:
            src = file.read()

        list_info = []

        soup = BeautifulSoup(src, 'lxml')

        with open('index.html', encoding='utf-8') as file:
            src = file.read()

        list_info = []

        soup = BeautifulSoup(src, 'lxml')

        names = soup.find_all('h3', class_='title-root-zZCwT')
        # for name in names:
        #     print(name.text)

        prices = soup.find_all('span', class_='price-text-_YGDY')
        # for price in prices:
        #     print(price.text)

        adresses = soup.find_all('div', class_='geo-address-fhHd0')
        # for adress in adresses:
        #     print(adress.text)

        urls = soup.find('div', class_='items-items-kAJAg').find_all('a', class_='link-link-MbQDP')
        # for url in urls:
        #     print(url.get('href'))

        descriptions = soup.find_all('div', class_='iva-item-text-Ge6dR iva-item-description-FDgK4 text-text-LurtD text-size-s-BxGpL')
        # for desc in descriptions:
        #     print(desc.text)

        dates = soup.find_all('div', class_='date-text-KmWDf text-text-LurtD text-size-s-BxGpL text-color-noaccent-P1Rfs')
        # for data in dates:
        #     print(data.text)

        for i in range(len(names)):

            info = {
                'Size': names[i].text.replace(' ', ''),
                'Adress': adresses[i].text.replace(' ', ''),
                'Price': prices[i].text.replace(' ', ''),
                'Date': dates[i].text.replace(' ', ''),
                'Descripton': descriptions[i].text.replace(' ', ''),
                'URL': 'https://www.avito.ru' + urls[i].get('href')

            }
            list_info.append(info)

        with open('info.json', 'a', encoding='utf_8_sig') as file:
            json.dump(list_info, file, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

