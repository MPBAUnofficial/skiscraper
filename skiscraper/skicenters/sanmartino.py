import requests
from base import SkiCenter, Lift, Slope, ApiError


class SanMartino(SkiCenter):
    def __init__(self, name=None):
        super(SanMartino, self).__init__(name)

    def update(self):
        # It won't work without these headers
        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'it',
            'Host': 'core.dolomitisuperski.com',
            'User-Agent': 'com.dolomitisuperski.skibeep/6.1 (Linux; Android)',
            'X-Dss-Device-Os': 'android',
            'X-Dss-Device-Resolution': '320, 480',
            'deviceid': 'SuchAPrettyDeviceID'  # todo: dynamic device id?
        }
        url = 'http://core.dolomitisuperski.com/skiareas/19/localities'
        r = requests.get(url, headers=headers)
        j = r.json()
        if j['status']['value'] != 'ok':
            raise ApiError
        res = j['response']

        _lifts = []
        for area in res:
            area_name = area['name']

            for lift in area['lifts']:
                l = Lift(
                    area_name, str(lift['id']), lift['name'], lift['isOpen']
                )
                _lifts.append(l)

        self.lifts = _lifts[:]
