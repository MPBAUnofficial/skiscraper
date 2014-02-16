import requests
from base import SkiCenter, Slope, Lift, ApiError


class Pinzolo(SkiCenter):
    def __init__(self, name=None):
        super(Pinzolo, self).__init__(name)

    def update(self):
        # TODO: dynamic device token? :P
        api_url = \
            'http://m.trientgroup.it/ae/api.do?cmd=ly&dt=SuchAPrettyDeviceToken'
        r = requests.get(api_url)

        if not r.ok:
            raise ApiError

        json_data = r.json()
        if json_data['result'] != 0:
            raise ApiError

        skiareas = json_data['atypes'][1]['acts'][2]['sm']['lt']  # trust me
        _slopes, _lifts = [], []

        for area in skiareas:
            is_open = \
                (
                    area['i'] ==
                    'http://m.trientgroup.it/ae/image/image/c_nd01vigmal.3.png'
                )
            if area['t'] == 1:
                color = area['c']
                difficulties = {'0000FF': 0, 'EE4000': 1, '000000': 2}
                difficulty = difficulties[color]
                slope = Slope('Pinzolo', area['n'], area['ttl'],
                              difficulty, is_open)
                _slopes.append(slope)
            elif area['t'] == 2:
                lift = Lift('Pinzolo', area['n'], area['ttl'], is_open)
                _lifts.append(lift)

        self.slopes, self.lifts = _slopes[:], _lifts[:]