import csv, random, time

import requests
from bs4 import BeautifulSoup


def update_dict(data: dict, key: str, value: int) -> None:
    """
    Функция для обновления словарей. 
    Не перезаписывает данные словаря, в отличии от метода updata, а аккумулирует значение.

    :param data: исходный словарь.

    :param key: ключ, который нужно обновить.

    :param value: новые данные.
    """
    if key in data:
        data[key] += value
    else:
        data[key] = value


def parse_markup(html: str) -> tuple[str, dict]:
    """
    Функция для сбора данных из разметки.

    :param html: разметка.

    :return: кортеж, содержащий ссылку на следующую страницу и собранные данные
    :rtype: tuple
    """
    RUSSIAN_LETTERS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    
    collected_data = {}

    soup = BeautifulSoup(html, "lxml")

    groups = soup.select("#mw-pages .mw-category-group")

    for group in groups:
        title = group.find("h3").text
        if title and title in RUSSIAN_LETTERS:
            count = len(group.find_all("li"))

            update_dict(collected_data, title, count)

    next_link = soup.find('a', string='Следующая страница')
    next_url = next_link['href'] if next_link else None

    return next_url, collected_data


def parser(url: str, headers: dict) -> dict[str: int]:
    """
    Функция для получения данных с Википедии.

    Выполняется, пока существует следующая страница.

    :param url: Адрес страницы, с которой начинается сбор

    :param headers: Зоголовки для запроса

    :return data: Собранные данные

    :rtype: dict[str: int]
    """
    data = {}
    base_url = 'https://ru.wikipedia.org'

    current_url = f'{base_url}{url}'
    
    page_counter = 1

    while current_url:
        print(f"Страница: {page_counter}")
        try:
            response = requests.get(current_url, headers)

            response.raise_for_status()

            next_url, page_data = parse_markup(response.text)

            current_url = f'{base_url}{next_url}' if next_url else None

            for key, value in page_data.items():
                update_dict(data, key, value)

            time.sleep(random.randrange(0, 10))
        except requests.HTTPError:
            print("Ошибка подключения")
            break

        page_counter += 1
    else:
        print("Данные собраны")

    return data


def write_to_csv(data: dict, filename: str) -> None:
    """
    Функция для записи данных в csv файл.

    :param data: Словарь с данными.
    
    :param filename: Имя файла формата "*.csv".
    """
    if not filename.endswith(".csv"):
        print("Неверное имя файла!")
        return

    if data:
        with open(filename, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)

            for row in data.items():
                writer.writerow(row)
            else:
                print("Данные записаны")
    else:
        print("Нет данных для записи!")


if __name__ == "__main__":
    start_url = '/wiki/Категория:Животные_по_алфавиту'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    collected_animals = parser(start_url, headers)
    write_to_csv(collected_animals, "beasts.csv")