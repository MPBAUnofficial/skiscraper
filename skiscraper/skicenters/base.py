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
        self.difficulty = difficulty  # 0: easy, 1: middle, 2: difficult

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
    def __init__(self, area, station_id):
        self.area = area
        self.station_id = station_id

        # instantaneous data
        self.temperature = None
        self.rainfall = None
        self.humidity = None
        self.wind_speed = None
        self.pressure = None

        self.update()

    def __str__(self):
        return '{x.area} [{x.station_id}]:\ntemp.: {x.temperature}, ' \
               'rainfall: {x.rainfall}, humidity: {x.humidity}, ' \
               'wind: {x.wind_speed}, pressure: {x.pressure}'.format(x=self)

    def __repr__(self):
        return self.__str__()

    def update(self):
        url = 'http://hydstraweb.provincia.tn.it/wgen/cache/anon/lf{0}.xml'\
              .format(self.station_id.lower())
        r = requests.get(url)
        root = objectify.fromstring(r.text)

        for var in root.tsfile.variable:
            name = var.attrib['name']
            get_value = lambda node: float(node.data.p.attrib['value'])

            # todo: save date?
            if name == 'Pioggia':
                self.rainfall = get_value(var)
            elif name == 'Temperatura aria':
                self.temperature = get_value(var)
            elif name == 'Umidita\' aria':  # dat Italian
                self.humidity = get_value(var)
            elif name == 'Velocita\' vento media':
                self.wind_speed = get_value(var)
            elif name == 'Pressione atmosferica':
                self.pressure = get_value(var)


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