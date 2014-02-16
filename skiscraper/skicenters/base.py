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


class SkiCenter(object):
    __metaclass__ = ABCMeta

    def __init__(self, name=None):
        self.name = name or self.__class__.__name__

        self._slopes = None  # list of <Slope>
        self._lifts = None  # list of <Lift>

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