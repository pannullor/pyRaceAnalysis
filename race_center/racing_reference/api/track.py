from racing_reference.scraper import Scraper

import datetime
from dateutil import relativedelta


class Track(Scraper):
    def __init__(self, name):
        self.name = name

        # the active driver page
        self.page = self.fetch_page("/tracks/{}".format(self.name.replace(' ', '_')))

