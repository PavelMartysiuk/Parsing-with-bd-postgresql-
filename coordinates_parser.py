import requests
from requests import HTTPError
from bs4 import BeautifulSoup
import json


class ParseRussiaTowns:
    """Parse coordinates of russians towns and regions"""

    def __init__(self):
        self.url = 'https://time-in.ru/coordinates/russia'
        self.towns = {}
        self.regions = {}

    def check_connect(self, url):
        try:
            response = requests.get(url)
        except HTTPError as http:
            print(f'Error{http}')
        except Exception as exc:
            print(f'Error{exc}')
        if response.status_code == 404:
            print('Page not found')
            return False
        return response.text

    def write_json(self):
        FILE_NAME = 'russian_towns.json'
        with open(FILE_NAME, 'w') as file:
            json.dump(self.towns, file, indent=2)

    def get_regions_links(self):
        response = self.check_connect(self.url)
        if response:
            soup = BeautifulSoup(response, 'html.parser')
            regions_block = soup.find('ul', class_='coordinates-list')
            regions = regions_block.find_all('li')
            for region in regions:
                link = region.find('a').get('href')
                region_name = region.find('a').text
                self.regions[region_name] = link

    def parse_regions_coordinates(self):
        self.get_regions_links()
        for region in self.regions:
            link = self.regions[region]
            response = self.check_connect(link)
            if response:
                soup = BeautifulSoup(response, 'html.parser')
                coordinates_block = soup.find('ul', class_='coordinates-items')
                coordinates = coordinates_block.find('div', class_='coordinates-items-right').text
                self.towns[region] = coordinates

    def parse_town_coordinates(self):
        response = self.check_connect(self.url)
        if response:
            soup = BeautifulSoup(response, 'html.parser')
            coordinates_block = soup.find('ul', class_='coordinates-items')
            towns = coordinates_block.find_all('li')
            for town in towns:
                town_name = town.find('a', class_='coordinates-items-left').text
                town_coordinates = town.find('div', class_='coordinates-items-right').text
                self.towns[town_name] = town_coordinates


class ParseWorldTowns:
    """Parse coordinates of world towns and countries"""
    def __init__(self):
        self.url = 'https://time-in.ru/coordinates'
        self.countries_links = {}
        self.countries_coordinates = {}
        self.town_coordinates = {}

    def check_connect(self, url):
        try:
            response = requests.get(url)
        except HTTPError as http:
            print(f'Error{http}')
        except Exception as exc:
            print(f'Error{exc}')
        if response.status_code == 404:
            print('Page not found')
            return False
        return response.text

    def write_json(self, file_name, data):
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=2)
        with open(file_name, 'r') as file:
            d = json.load(file)
            print(d)

    def get_countries_links(self):
        response = self.check_connect(self.url)
        if response:
            soup = BeautifulSoup(response, 'html.parser')
            country_block = soup.find('ul', class_='coordinates-list')
            countries = country_block.find_all('li')
            for country in countries:
                country_name = country.find('a').text
                link = country.find('a').get('href')
                self.countries_links[country_name] = link

    def get_countries_coordinates(self):
        self.get_countries_links()
        COUNRTIES_COONRDINATES_FILE = 'countries.json'
        WORLD_TOWNS_COORDINATE_FILE = 'world_town.json'
        for country in self.countries_links:
            link = self.countries_links[country]
            response = self.check_connect(link)
            if response:
                soup = BeautifulSoup(response, 'html.parser')
                try:
                    capital_coordinates = soup.find('div', class_='coordinates-items-right').text
                except AttributeError:
                    continue
                else:
                    self.countries_coordinates[country] = capital_coordinates
                    towns_block = soup.find('ul', class_='coordinates-items')
                    towns = towns_block.find_all('li')
                    for town in towns:
                        town_name = town.find('a').text
                        town_coordinates = town.find('div', class_='coordinates-items-right').text
                        self.town_coordinates[town_name] = town_coordinates

        self.write_json(COUNRTIES_COONRDINATES_FILE, self.countries_coordinates)
        self.write_json(WORLD_TOWNS_COORDINATE_FILE, self.town_coordinates)


if __name__ == '__main__':
    towns_russia = ParseRussiaTowns()
    towns_russia.parse_town_coordinates()
    towns_russia.parse_regions_coordinates()
    towns_russia.write_json()
    countries = ParseWorldTowns()
    countries.get_countries_coordinates()
