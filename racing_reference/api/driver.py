from racing_reference.scraper import Scraper

import datetime
from dateutil import relativedelta


# class to describe a driver
class Driver(Scraper):

    def __init__(self, name):
        self.name = name
        self.url = "https://www.racing-reference.info/driver/{}".format(self.name.replace(' ', '_'))
        self.page = self.fetch_page(self.url)

    def get_tables(self):
        """
        simple helper method just return all the tables
        :return: all the tables
        """

        return self.page.find_all('table')

    def driver_info(self, info):
        """
        method to get the drivers basic info
        like DOB and hometown. This info isn't
        marked up well for BS to grab it, so we
        have to do some string manipulation to
        extract it. Fortunately it at least is
        proceeded by a string such as born or home
        so we can use those to parse the info out
        :param info: (str) name of the informative bit to parse info from
        :return: string
        """

        # get the info table
        text = self.get_tables()[4].find('td').text

        # starting point is the string we can use to
        # determine where the info bit is at
        start = text.find(info)

        # the information is the substring from start
        # to the next line break.
        extracted = text[start:text.find('\n', start)].replace(info, '')
        return extracted

    @property
    def birth_date(self):
        return self.driver_info('Born: ')

    @property
    def age(self):
        """
        convert the drivers birth date to age in years
        :return:
        """
        bd = datetime.datetime.strptime(self.birth_date, '%B %d, %Y')
        today = datetime.datetime.today()

        difference = relativedelta.relativedelta(today, bd)
        return difference.years

    @property
    def cup_years_active(self):
        return self.get_tables()[7].find('tr', {'class': 'tot'}).find('td').text.split()[0]
