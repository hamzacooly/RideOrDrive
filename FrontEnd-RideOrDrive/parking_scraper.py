from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import os


class ParkMeScraper:

    def __init__(self):
        self.pagetext = 'https://www.parkme.com/'
        options = Options()
        options.set_headless(True)
        self.driver = webdriver.Chrome(options=options)


    def getLots(self, lat, lon):
        query = 'map?q=' + str(lat) + '%2C+' + str(lon)

        url = self.pagetext+query
        self.driver.get(url)
        time.sleep(1.5)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        lots = []
        for first in soup.find_all('div', attrs={'class':'featured_lot_container'}):
            entry = {}
            entry['name'] = first.find('div',attrs={'class':'fle_lot_name'}).text.strip()
            entry['address'] = first.find('div',attrs={'class':'fle_lot_address'}).text.strip()
            entry['price, hourly'] = first.find('a',attrs={'class':'fle_reserve'}).text.strip()
            entry['occupancy'] = first.find('div',attrs={'class':'occupancy-bar'}).text.strip()
            lots.append(entry)

        return lots
'''
# USE EXAMPLE
from parking_scraper import ParkMeScraper

lots = ParkMeScraper().getLots(30.266926,-97.750519)
print(lots)

'''
