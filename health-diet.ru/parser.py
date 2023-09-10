import requests
from bs4 import BeautifulSoup
import json
import csv

# url = 'https://health-diet.ru/table_calorie/'
headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}

# req = requests.get(url, headers=headers)
# src = req.text
#
# with open('index.html', 'w', encoding='utf-8') as f:
#     f.write(src)

# with open('index.html', 'r', encoding='utf-8') as f:
#     src = f.read()
#
# soup = BeautifulSoup(src, 'lxml')
# all_product = soup.find_all(class_='mzr-tc-group-item-href')
#
# all_categories_dict = {}
# for item in all_product:
#     product_text = item.text
#     product_href = 'https://health-diet.ru' + item.get('href')
#     all_categories_dict[product_text] = product_href
#
# with open('categories.json', 'w', encoding='utf-8') as f:
#     json.dump(all_categories_dict, f, indent=4, ensure_ascii=False)

with open('categories.json', 'r', encoding='utf-8') as f:
    all_categories = json.load(f)

iteration_count = int(len(all_categories)) - 1
count = 0
print(f'Всего итераций: {iteration_count}')
for name, href in all_categories.items():

    rep = [',', ' ', '-', "'"]
    for item in rep:
        if item in name:
            name = name.replace(item, '_')

    req = requests.get(url=href, headers=headers)
    src = req.text

    with open(f'data/{count}_{name}.html', 'w', encoding='utf-8') as f:
        f.write(src)

    with open(f'data/{count}_{name}.html', encoding='utf-8') as f:
        src = f.read()

    soup = BeautifulSoup(src, 'lxml')

    #проверка страницы на наличие таблицы
    alert_block = soup.find(class_='uk-alert-danger')
    if alert_block is not None:
        continue

    #собираем заголовки таблицы
    table_head = soup.find(class_='mzr-tc-group-table').find('tr').find_all('th')
    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text

    with open(f'data/{count}_{name}.csv', 'w', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(
            (
                product,
                calories,
                proteins,
                fats,
                carbohydrates
            )
        )

    #собираем данные продуктов
    products_data = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')
    for item in products_data:
        product_tds = item.find_all('td')

        title = product_tds[0].find('a').text
        calories = product_tds[1].text
        proteins = product_tds[2].text
        fats = product_tds[3].text
        carbohydrates = product_tds[4].text

        with open(f'data/{count}_{name}.csv', 'a', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(
                (
                    title,
                    calories,
                    proteins,
                    fats,
                    carbohydrates
                )
            )


    count += 1
    print(f'#Итерация {count}. {name} записана...')
    iteration_count -= 1
    if iteration_count == 0:
        print("Работа завершена")
        break

    print(f'Осталось итераций: {iteration_count}')
