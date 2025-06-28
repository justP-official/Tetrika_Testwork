import csv, os

import pytest

from solution import parser, parse_markup, update_dict, write_to_csv


def test_parse_markup_with_good_html():
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test</title>
</head>
<body>
    <div id="mw-pages">
        <div class="mw-category">
            <div class="mw-category-group">
                <h3>А</h3>
                <ul>
                    <li>Lorem ipsum dolor sit amet consectetur adipisicing elit. Debitis laborum deserunt deleniti veniam maxime esse! Eveniet hic ipsum natus laborum voluptatem debitis est possimus ea non, nam aspernatur modi placeat!</li>
                    <li>Lorem ipsum dolor sit amet consectetur adipisicing elit. Ratione atque quasi repellat! Aliquam veritatis fugiat voluptatem dolor. Ducimus aliquam, doloremque inventore dolore reiciendis ut architecto, sapiente sunt eaque non consectetur?</li>
                    <li>Lorem ipsum dolor sit amet consectetur adipisicing elit. Fuga ducimus, architecto unde nostrum officiis, sint molestias iste culpa nam ut laborum incidunt ullam harum delectus inventore commodi qui fugiat eos.</li>
                </ul>
            </div>
            <div class="mw-category-group">
                <h3>Б</h3>
                <ul>
                    <li>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Vitae modi doloremque cupiditate soluta, qui accusamus laudantium voluptatibus illum expedita illo ad eaque quae nam numquam tempora, consequatur praesentium quasi non!</li>
                    <li>Lorem ipsum dolor sit amet consectetur adipisicing elit. Facilis adipisci, vitae officia sapiente doloremque consectetur sunt. Doloribus voluptatem rerum cumque quo commodi possimus quisquam perspiciatis minus, saepe tempore accusantium sed?</li>
                    <li>Lorem ipsum dolor sit amet consectetur adipisicing elit. Placeat ea iusto veritatis! Magni dicta asperiores quia placeat facere exercitationem, soluta officia aperiam. Culpa nostrum quo ducimus impedit eius? Minima, commodi.</li>
                    <li>Lorem ipsum dolor sit amet consectetur adipisicing elit. Autem mollitia nihil, a alias repellendus ducimus illum iure sequi eaque quo fugit, quos quod, consectetur culpa dicta voluptatum eum enim architecto!</li>
                </ul>
            </div>
            <div class="mw-category-group">
                <h3>Z</h3>
                <ul>
                    <li>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Vitae modi doloremque cupiditate soluta, qui accusamus laudantium voluptatibus illum expedita illo ad eaque quae nam numquam tempora, consequatur praesentium quasi non!</li>
                    <li>Lorem ipsum dolor sit amet consectetur adipisicing elit. Facilis adipisci, vitae officia sapiente doloremque consectetur sunt. Doloribus voluptatem rerum cumque quo commodi possimus quisquam perspiciatis minus, saepe tempore accusantium sed?</li>
                    <li>Lorem ipsum dolor sit amet consectetur adipisicing elit. Placeat ea iusto veritatis! Magni dicta asperiores quia placeat facere exercitationem, soluta officia aperiam. Culpa nostrum quo ducimus impedit eius? Minima, commodi.</li>
                    <li>Lorem ipsum dolor sit amet consectetur adipisicing elit. Autem mollitia nihil, a alias repellendus ducimus illum iure sequi eaque quo fugit, quos quod, consectetur culpa dicta voluptatum eum enim architecto!</li>
                </ul>
            </div>
        </div>
    </div>
    <a href="test-href">Следующая страница</a>
</body>
</html>
"""

    next_url, data = parse_markup(html)

    assert next_url is not None
    assert next_url == "test-href"

    assert "А" in data
    assert data["А"] == 3

    assert "Б" in data
    assert data["Б"] == 4

    assert "Z" not in data


def test_parse_markup_with_bad_html():
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test</title>
</head>
<body>
    <p>Empty!</p>
</body>
</html>
"""

    next_url, data = parse_markup(html)

    assert next_url is None

    assert len(data) == 0


def test_update_dict():
    tested_dict = {"A": 1, "B": 2}

    new_key = "X"
    new_value = 3
    old_key = "A"

    update_dict(tested_dict, new_key, new_value)
    assert new_key in tested_dict
    assert tested_dict[new_key] == new_value

    old_value = tested_dict[old_key]
    update_dict(tested_dict, old_key, new_value)
    assert old_key in tested_dict
    assert tested_dict[old_key] == old_value + new_value


def test_parser():
    start_url = '/wiki/Категория:Животные_по_алфавиту'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    result = parser(start_url, headers)

    assert len(result) == 29  # В результирующем словаре отсутствуют ключи Ё, Ъ, Ы, Ь


def test_write_to_csv_with_bad_filename(capsys):
    data = {"А": 1}
    filename = "test"

    write_to_csv(data, filename)

    captured = capsys.readouterr()
    assert captured.out.strip() == "Неверное имя файла!"


def test_write_to_csv_with_non_empty_dict(tmp_path, capsys):
    data = {"А": 1, "Б": 2, "В": 3}
    filename = tmp_path / "test.csv"
    
    write_to_csv(data, str(filename))
    
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    assert rows == [["А", "1"], ["Б", "2"], ["В", "3"]]
    
    captured = capsys.readouterr()
    assert captured.out.strip() == "Данные записаны"


def test_write_to_csv_with_empty_dict(tmp_path, capsys):
    filename = tmp_path / "empty.csv"
    
    write_to_csv({}, str(filename))
    
    captured = capsys.readouterr()
    assert captured.out.strip() == "Нет данных для записи!"
