import requests
from lxml import objectify

from abc import ABCMeta, abstractmethod


class ApiError(Exception):
    pass


class Slope(object):
    def __init__(self, area, _id, name, difficulty, _open):
        self.area = area
        self.id = _id
        self.name = name
        self.open = _open
        # 0: easy, 1: middle, 2: difficult, 3: snowpark, 4: off-piste
        self.difficulty = difficulty

    def __repr__(self):
        u = lambda s: s.encode('utf-8')
        return '{0} {1} - {2}'\
            .format(u(self.id), u(self.name), 'Open' if self.open else 'Closed')

    def __str__(self):
        return self.__repr__()


class Lift(object):
    def __init__(self, area, _id, name, _open):
        self.area = area
        self.id = _id
        self.name = name
        self.open = _open

    def __repr__(self):
        u = lambda s: s.encode('utf-8')
        return '{0} {1} - {2}' \
            .format(u(self.id), u(self.name), 'Open' if self.open else 'Closed')

    def __str__(self):
        return self.__repr__()


class Weather(object):
    """
    Weather data provided by MeteoTrentino
    """
    def __init__(self, *stations):
        self.stations = []
        for s in stations:
            # make a list of (area, station_id) tuple.
            self.stations.append((s.split('::', 1)))

        # instantaneous data
        self.station_name = self.station_id = None
        self.temperature = None
        self.tmin = None
        self.tmax = None
        self.rainfall = None
        self.wind_speed = None
        self.radiations = None

        self.update()

    def __str__(self):
        return '{x.station_name} [{x.station_id}]:\ntemp.: {x.temperature} C,' \
               ' rainfall: {x.rainfall} mm, radiations: {x.radiations} W/mq, ' \
               'wind: {x.wind_speed} m/s'.format(x=self)

    def __repr__(self):
        return self.__str__()

    def update(self):
        for station_name, station_id in self.stations:
            url = 'http://dati.meteotrentino.it' \
                  '/service.asmx/ultimiDatiStazione?codice={0}'\
                .format(station_id.lower())
            r = requests.get(url)

            if not r.ok:
                continue

            root = objectify.fromstring(r.text.encode('utf-8'))

            self.tmin = root.tmin
            self.tmax = root.tmax
            self.rainfall = root.rain

            # just an awful fix to the unreliability of meteotrentino data
            #todo: refactor?
            try:
                self.temperature = \
                    root.temperature.temperatura_aria[-1].temperatura
            except AttributeError:
                self.temperature = None

            try:
                self.wind_speed = int(root.venti.vento_al_suolo[-1].v)
            except AttributeError:
                self.wind_speed = None

            try:
                self.radiations = root.radiazione.radiazioneglobale[-1].rsg
            except AttributeError:
                self.radiations = None

            self.station_name = station_name
            self.station_id = station_id

            break


class SkiCenter(object):
    __metaclass__ = ABCMeta

    def __init__(self, name=None):
        self.name = name or self.__class__.__name__

        self._slopes = None  # list of <Slope>
        self._lifts = None  # list of <Lift>
        self.weather = None

    @property
    def slopes(self):
        if self._slopes is None:
            self._slopes = []
            self.update()
        return self._slopes

    @slopes.setter
    def slopes(self, value):
        self._slopes = value

    @property
    def lifts(self):
        if self._lifts is None:
            self._lifts = []
            self.update()
        return self._lifts

    @lifts.setter
    def lifts(self, value):
        self._lifts = value

    @abstractmethod
    def update(self):
        pass

    def get_slope_by_name(self, name):
        if not self.slopes:
            self.update()

        transform = lambda s: s.strip().lower()
        name = transform(name)

        for slope in self.slopes:
            if transform(slope.name) == name:
                return slope
        return None

    def get_slope_by_id(self, _id):
        if not self.slopes:
            self.update()

        for slope in self.slopes:
            if slope.id == _id:
                return slope
        return None
