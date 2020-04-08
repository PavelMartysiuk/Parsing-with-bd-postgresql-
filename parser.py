import requests
from requests import HTTPError
from bs4 import BeautifulSoup
import datetime
import tables
from sqlalchemy.exc import IntegrityError
import json


class ParseRussiaData:
    """Parse russian statistic of coronavirus"""

    def __init__(self):
        self.url = 'https://стопкоронавирус.рф/'
        date = datetime.datetime.now()
        self.date = date.strftime('%Y-%m-%d %H:%M:%S')
        self.parse_site()

    def check_connect(self):
        try:
            response = requests.get(self.url)
        except HTTPError as http:
            print(f'Error{http}')
        except Exception as exc:
            print(f'Error{exc}')
        if response.status_code == 404:
            print('Page not found')
            return False
        return response.text

    def save_in_db(self, town, quantity_sick, quantity_recovered, quantity_deaths, coordinates):
        sess = tables.Session()
        new_row = tables.CoronavirusRussiaStatistic(town=town,
                                                    sick=quantity_sick, recover=quantity_recovered,
                                                    death=quantity_deaths, date=self.date, coordinates=coordinates)
        sess.add(new_row)
        sess.commit()

    def read_town_coordinates(self):
        COORDINATES_FILE = 'russian_towns.json'
        with open(COORDINATES_FILE, 'r') as file:
            self.coordinates = json.load(file)

    def parse_site(self):
        response = self.check_connect()
        self.read_town_coordinates()
        if response:
            soup = BeautifulSoup(response, 'html.parser')
            main_block = soup.find('div', class_='d-map__list')
            table = main_block.find('table')
            rows = table.find_all('tr')
            for row in rows:
                town = row.find('th').text
                quantity_sick = row.find('span', class_='d-map__indicator d-map__indicator_sick').parent.text
                quantity_recovered = row.find('span', class_='d-map__indicator d-map__indicator_healed').parent.text
                quantity_deaths = row.find('span', class_='d-map__indicator d-map__indicator_die').parent.text
                coordinates = self.coordinates.get(town, 'Координаты не найдены')
                self.save_in_db(town, quantity_sick, quantity_recovered, quantity_deaths, coordinates)


class ParseCoronavitrusNews:
    """Parse news coronavirus in Russia"""

    def __init__(self):
        self.url = 'https://стопкоронавирус.рф/news/'
        self.articles_links = []
        self.months = {'января': '01', 'февраля': '02', 'марта': '03',
                       'апреля': '04', 'мая': '05', 'июня': '06', 'июля': '07',
                       'августа': '08', 'сентября': '09', 'октября': '10',
                       'ноября': '11', 'декарбря': '12'}

    def check_connect(self, url):
        try:
            response = requests.get(url)
        except HTTPError as http:
            print(f'Error{http}')
            return False
        except Exception as exc:
            print(f'Error{exc}')
            return False
        if response.status_code == 404:
            print('Page not found')
            return False
        return response.text

    def save_in_bd(self, title, content, source, date):
        try:
            sess = tables.Session()
            new_row = tables.News(title=title, content=content,
                                  source=source, date=date)
            sess.add(new_row)
            sess.flush()
        except IntegrityError:
            print('I have this record in bd')
            return -1
        else:
            sess.commit()

    def conversion_date(self, date):
        QUANTITY_TIME_SYMBOLS = 7
        START_MONTH = 3
        END_YEAR = 4
        curr_year = str(datetime.datetime.now())[:END_YEAR]
        end_month = len(date) - QUANTITY_TIME_SYMBOLS
        month = date[START_MONTH:end_month]
        month_number = self.months[month]
        new_date = date.replace(month, month_number).strip()
        full_date = curr_year + new_date
        format_date = datetime.datetime.strptime(full_date, '%Y%d %m %H:%M')
        return format_date

    def get_quantity_pages(self):
        LAST_PAGE_INDEX = -1
        response = self.check_connect(self.url)
        if response:
            soup = BeautifulSoup(response, 'html.parser')
            last_page = soup.find_all('a', class_='cv-pager__item')[LAST_PAGE_INDEX].text
            return last_page

    def get_articles_links(self):
        START_PAGE = 1
        pages = self.get_quantity_pages()
        last_page = int(pages) + 1
        for page in range(START_PAGE, last_page):
            url = self.url + '?page=' + str(page)
            response = self.check_connect(url)
            if response:
                soup = BeautifulSoup(response, 'html.parser')
                links_block = soup.find_all('div', class_='cv-news-page__news-list-item')
                for item in links_block:
                    link = item.find('a').get('href')
                    full_link = self.url + link
                    self.articles_links.append(full_link)

    def get_articles_content(self):
        END_DATE_SYMBOL = '•'
        END_TITLE_SYMBOL = '|'
        DATE_INDEX = 0
        self.get_articles_links()
        for link in self.articles_links:
            response = self.check_connect(link)
            if response:
                soup = BeautifulSoup(response, 'html.parser')
                date_block = soup.find('div', class_='cv-full-news__date').text
                date = date_block.split(END_DATE_SYMBOL)[DATE_INDEX]
                format_date = self.conversion_date(date)
                title_block = soup.find('title').text
                title = title_block.split(END_TITLE_SYMBOL)[DATE_INDEX].strip()
                content_block = soup.find('div', class_='cv-full-news__text')
                content = content_block.find_all('p')
                content = list(map(lambda sentence: sentence.text, content))
                full_content = ''.join(content)
                source_block = soup.find('div', class_='cv-full-news__src')
                source_url = source_block.find('a').get('href')
                status_code = self.save_in_bd(title, full_content, source_url, format_date)
                if status_code == -1:
                    break


class ParseWorldData:
    """Parse world statistic of coronavirus"""

    def __init__(self):
        self.url = 'https://meduza.io/feature/2020/03/05/' \
                   'poslednie-dannye-po-koronavirusu-vo-vsem-mire-tablitsa'
        date = datetime.datetime.now()
        self.date = date.strftime('%Y-%m-%d %H:%M:%S')

    def check_connect(self):
        try:
            response = requests.get(self.url)
        except HTTPError as http:
            print(f'Error{http}')
            return False
        except Exception as exc:
            print(f'Error{exc}')
            return False
        if response.status_code == 404:
            print('Page not found')
            return False
        return response.text

    def read_coordinates(self):
        COUNTRIES_COORDINATES_FILE = 'countries.json'
        with open(COUNTRIES_COORDINATES_FILE, 'r') as file:
            self.coordinates = json.load(file)

    def save_in_bd(self, country, sick, recover, death, coordinates):
        sess = tables.Session()
        new_row = tables.CoronavirusWorldStatistic(
            country=country, sick=sick, recover=recover,
            death=death, date=self.date, coordinates=coordinates)
        sess.add(new_row)
        sess.commit()

    def parse_statictic(self):
        START_TABLE = 1
        START_COUNTRY = 3
        SICK_INDEX = 0
        RECOVER_INDEX = 1
        DEATH_INDEX = 2
        self.read_coordinates()
        response = self.check_connect()
        if response:
            soup = BeautifulSoup(response, 'html.parser')
            rows = soup.find_all('div', class_='Table-row')[START_TABLE:]
            for row in rows:
                try:
                    country = row.find('div', class_='Table-cell Table-white Table-s').text[START_COUNTRY:]
                    statistic = row.find_all('div', class_='Table-cell Table-white Table-xs')
                    sick = statistic[SICK_INDEX].text
                    recover = statistic[RECOVER_INDEX].text
                    death = statistic[DEATH_INDEX].text
                    coordinates = self.coordinates.get(country, 'Координаты не найдены')
                except AttributeError:
                    continue
                else:
                    self.save_in_bd(country, sick, recover, death, coordinates)


if __name__ == '__main__':
    russian_parser = ParseRussiaData()
    russian_parser.read_town_coordinates()
    news_parser = ParseCoronavitrusNews()
    news_parser.get_articles_content()
    world_parser = ParseWorldData()
    world_parser.parse_statictic()
