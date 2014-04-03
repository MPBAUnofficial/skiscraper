from skicenters.cermis import Cermis
from skicenters.latemar import Latemar
from skicenters.sanmartino import SanMartino
from skicenters.pinzolo import Pinzolo
from skicenters.bondone import Bondone

__all__ = ['Cermis', 'Latemar', 'SanMartino', 'Pinzolo', 'Bondone']


class SkiScraper(object):
    def __init__(self):
        self.skicenters = dict(cermis=Cermis(), latemar=Latemar(),
                               san_martino=SanMartino(), pinzolo=Pinzolo(),
                               bondone=Bondone())

    def __getitem__(self, item):
        return self.skicenters[item]