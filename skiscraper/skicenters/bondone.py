import requests
from bs4 import BeautifulSoup

from base import SkiCenter, Slope, Lift, ApiError, Weather


class Bondone(SkiCenter):
    def __init__(self, name=None):
        super(Bondone, self).__init__(name)
        # Weather set to 'Monte Bondone - Giardino Botanico'
        # To switch to 'Monte Bondone - Viote', set code to T0368
        self.weather = Weather(
            'Monte Bondone (Viote)::T0368'
        )

    def update(self):
        r = requests.get(
            'http://www.skirama.it/en/skiarea/pistes-lifts/'
            'monte-bondone-ski-resort/'
        )
        if not r.ok:
            raise ApiError

        text = r.text.replace('\n', '')

        soup = BeautifulSoup(text)
        tables = soup.find_all('table', class_='pisteImpianti detail')

        _slopes, _lifts = [], []
        for table in tables:
            _type = table.previous_sibling.text
            if _type == 'Ski lifts':
                for lift in table.find_all('tr'):
                    #print lift
                    name = lift.find('td', class_='headerCell').text.strip()
                    is_open = \
                        'icoOpen.png' in lift.find_all('img')[-1].attrs['src']
                    _lifts.append(Lift(self.name, '', name, is_open))
            else:
                for slope in table.find_all('tr'):
                    name = slope.find('td', class_='headerCell').text.strip()
                    is_open = \
                        'icoOpen.png' in slope.find_all('img')[-1].attrs['src']

                    d_map = {
                        'Blue Slope (Easy)': 0,
                        'Red Slope (Medium)': 1,
                        'Snowboard': 3,
                        'Off-Piste': 4
                    }
                    _difficulty_text = slope.find_all('a')[-2].span.text.strip()
                    difficulty = d_map.get(_difficulty_text, -1)
                    _slopes.append(
                        Slope(self.name, '', name,difficulty, is_open)
                    )

        self.slopes, self.lifts = _slopes[:], _lifts[:]