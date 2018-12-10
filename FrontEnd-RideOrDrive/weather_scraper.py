from bs4 import BeautifulSoup
import time
import urllib


class WeatherScraper:

    def __init__(self):
        self.pagetext = 'https://forecast.weather.gov/MapClick.php?'


    def get_weather(self, lat, lon):
        query = 'lat=' + str(lat) + '&lon=' + str(lon)

        url = self.pagetext+query
        response = urllib.request.urlopen(url)
        soup = BeautifulSoup(response, 'html.parser')

        details = {}

        details['desc'] = soup.find('p',attrs={'class':'myforecast-current'}).text.strip()
        details['temp'] = soup.find('p',attrs={'class':'myforecast-current-lrg'}).text.strip()
        for tr in soup.find('div', attrs={'id':'current_conditions_detail'}).find_all('tr'):
            if 'Humidity' in str(tr):
                details['humidity'] = tr.find_all('td')[1].text.strip()
            if 'Visibility' in str(tr):
                details['visibility'] = tr.find_all('td')[1].text.strip()

        return details
'''
# USE EXAMPLE
lots = WeatherScraper().get_weather(30.266926,-97.750519)
print(lots)
'''
