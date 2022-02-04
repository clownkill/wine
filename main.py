import datetime as dt
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape

WINERY_FOUNDATION_YEAR = 1920
WINES_TABLE_FILE = 'wine.xlsx'


def get_wine_by_categories(database):
    wines = pandas.read_excel(
        database,
        na_values=False,
        keep_default_na=False
    ).to_dict(orient='records')
    wine_by_categories = defaultdict(list)
    for wine in wines:
        wine_by_categories[wine['Категория']].append(wine)
    return wine_by_categories


def render_webpage(wines_by_category):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    render_page = template.render(
        wine_factory_age=dt.datetime.now().year - WINERY_FOUNDATION_YEAR,
        wines_by_category=wines_by_category,
    )

    with open('index.html', 'w', encoding='utf8') as file:
        file.write(render_page)


def main():
    wines_by_category = get_wine_by_categories(WINES_TABLE_FILE)
    render_webpage(wines_by_category)
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()