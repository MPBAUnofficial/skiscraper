import requests
from bs4 import BeautifulSoup

from base import SkiCenter, Slope, Lift, ApiError


class Cermis(SkiCenter):
    def __init__(self, name=None):
        super(Cermis, self).__init__(name)

    def update(self):
        url = 'http://www.alpecermis.it/en/ski-lifts-and-ski-runs'
        r = requests.get(url)
        if not r.ok:
            raise ApiError

        soup = BeautifulSoup(r.text)

        _slopes, _lifts = [], []
        table = soup.find('table', class_='plain')
        for tr in table.find_all('tr', class_=['odd', 'even']):
            is_open = (tr.img.attrs['alt'] == 'Open')
            name = tr.find_all('td')[3].text.strip()
            _id = tr.find_all('td')[1].text.strip()

            if 'even' in tr.attrs.get('class', []):  # Slopes
                difficulties = dict(Blu=0, Rossa=1, Nera=2)
                difficulty = difficulties[
                    tr.find_all('td')[2].img.attrs['alt']
                ]
                _slopes.append(
                    Slope('Cermis', _id, name, difficulty, is_open)
                )
            elif 'odd' in tr.attrs.get('class', []):  # Lift
                _lifts.append(
                    Lift('Cermis', _id, name, is_open)
                )

        self.slopes, self.lifts = _slopes, _lifts
