import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
import json


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}


def get_page(url):

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service(executable_path='D:\\Python\\Projects\\parser\\project7\\driver')
    browser = Chrome(service=service, options=options)

    browser.get(url)
    time.sleep(6)

    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(browser.page_source)


def get_data(file_path):

    with open(file_path, encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    result_info = []
    # Поиск 30-ти первых карточек
    blocks_20 = soup.find_all('div', class_='product-card__wrapper')[:20]

    for item in blocks_20:
        try:
            # Собираем названия
            item_name = item.find('span', class_='product-card__name').text.strip()[2:]
        except Exception as ex:
            print(ex)
            item_name = 'Отсутствует'

        try:
            # Собираем бренд
            item_brand = item.find('span', class_='product-card__brand').text.strip()
        except Exception as ex:
            print(ex)
            item_brand = 'Отсутствует'

        try:
            # Собираем цену со скидкой
            item_price_sale = item.find('ins', class_='price__lower-price').text.strip().replace(' ', '')
        except Exception as ex:
            print(ex)
            item_price_sale = item.find('span', class_='price__lower-price').text.strip().replace(' ', '')

        try:
            # Собираем цену без скидки
            item_price = item.find('span', class_='price__wrap').find('del').text.strip().replace(' ', '')
        except Exception as ex:
            print(ex)
            item_price = 'Отсутствует'

        try:
            # Процент скидки
            item_discount = item.find('p', class_='product-card__tip--sale').text.strip()
        except Exception as ex:
            print(ex)
            item_discount = 'Отсутствует'

        # Получаем кол-во звёзд
        if item.find('span', class_='star5'):
            item_stars = '5*'
        elif item.find('span', class_='star4'):
            item_stars = '4*'
        elif item.find('span', class_='star3'):
            item_stars = '3*'
        elif item.find('span', class_='star2'):
            item_stars = '2*'
        elif item.find('span', class_='star1'):
            item_stars = '1*'
        else:
            item_stars = '0*'

        # Получаем кол-во отзывов
        item_comments = item.find('span', class_='product-card__count').text.strip().replace(' ', '')

        # Ссылка на товар
        item_url = item.find('a', class_='product-card__link').get('href')

        # Ссылка на изображение
        if 'https' in item.find('div', class_='product-card__img-wrap').find('img').get('src'):
            item_img = item.find('div', class_='product-card__img-wrap').find('img').get('src')
        else:
            item_img = 'https:' + item.find('div', class_='product-card__img-wrap').find('img').get('src')

        result_info.append(
            {
                'Название модели': item_name,
                "Бренд": item_brand,
                "Цена со скидкой": item_price_sale,
                "Цена без скидки": item_price,
                "Размер скидки": item_discount,
                "Количество звёзд": item_stars,
                "Количество отзывов": item_comments,
                'Ссылка на товар': item_url,
                'img': item_img
            }
        )

    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(result_info, file, indent=4, ensure_ascii=False)


def main(text):
    search_input = text.split()
    if '-' not in search_input:
        get_page(url=f'https://www.wildberries.ru/catalog/0/search.aspx?page=1&sort=rate&search={" ".join(search_input[:-1])}')
        get_data('index.html')
    else:
        price = search_input[-1].split('-')
        get_page(url=f'https://www.wildberries.ru/catalog/0/search.aspx?page=1&sort=rate&search={search_input[0]}&priceU={int(price[0])*100}%3B{int(price[1])*100}')
        get_data('index.html')

