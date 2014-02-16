import requests
from bs4 import BeautifulSoup

from base import SkiCenter, Slope, Lift, ApiError


class Latemar(SkiCenter):
    def __init__(self, name=None):
        super(Latemar, self).__init__(name)

    def update(self):
        r = requests.get(
            'http://www.latemar.it/default.asp?cms=6&lingua=2&stagione=i'
        )
        if not r.ok:
            raise ApiError

        soup = BeautifulSoup(r.text)
        tables = soup.find_all('table', class_='cms-tabella-imp')

        _slopes, _lifts = [], []
        for table in tables:
            area_name = \
                table.previous_element.previous_element.split(':')[0].strip()

            for tr in table.find_all('tr'):
                if tr.img is None or tr.strong is None:
                    continue

                is_open = ('stato_1.gif' in tr.img.attrs['src'])
                name = tr.strong.text.strip()

                if 'cms-titolo' in tr.attrs.get('class', ''):  # it's a lift
                    # Website does not supply ID for lifts. If that's really
                    # necessary, superski app's APIs does provide that.
                    _id = 'no_id'
                    _lifts.append(
                        Lift(area_name, _id, name, is_open)
                    )
                else:
                    difficulties = dict(a=0, r=1, n=2)

                    difficulty_img_src = \
                        tr.find('td', class_='cms-sottotitolo') \
                        .next_sibling.next_sibling.img.attrs['src']

                    # retrieve difficulty
                    difficulty = -1
                    for k in difficulties:
                        if 'pista_{0}.gif'.format(k) in difficulty_img_src:
                            difficulty = difficulties[k]

                    _id = tr.find_all('td')[2].text.strip()
                    _slopes.append(
                        Slope(area_name, _id, name, difficulty, is_open)
                    )

        self.slopes, self.lifts = _slopes[:], _lifts[:]

