from racing_reference.scraper import Scraper

from nameparser import HumanName

import datetime
from dateutil import relativedelta

import re


# class to describe a driver
class Driver(Scraper):

    def __init__(self, name):
        self.name = name

        # strip any periods or commas from names so we
        # successfully look up the active driver page.
        name_re = re.compile(r'[.,]')
        formatted_name = name_re.sub(' ', self.name).strip().replace('  ', ' ').replace(' ', '_')
        self.page = self.fetch_page(F"/driver/{formatted_name}")

        # the drivers name is used in driver data
        # urls for pages about the driver. The name
        # is used in the URL as the first 5 of the
        # last name and first two of the first name
        parsed_name = HumanName(self.name)
        key = '02' if parsed_name.suffix else '01'
        self.driver_key = F"{parsed_name.last[:5]}{parsed_name.first[0:2]}{key}".lower()

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
        df = self.get_table(self.page, 4)

        text = df[0][0]

        if info.lower() == 'home':
            home_re = re.compile(r'Home: ([\w\s]+),\s(\w){2}')
            match = home_re.search(text)
            if match:
                home = match.group()
                return home[home.find(':')+2:]

        if info.lower() == 'born':
            birthday_re = re.compile(r'Born: (\w+)\s(\d){1,2},\s(\d){4}')
            match = birthday_re.search(text)
            if match:
                birthday = match.group()
                return datetime.datetime.strptime(f"{birthday[birthday.find(':')+2:]}",
                                                  "%B %d, %Y")

        if info.lower() == 'died':
            died_re = re.compile(r'Died: (\w+)\s(\d){1,2},\s(\d){4}')
            match = died_re.search(text)
            if match:
                match_group = match.group()
                return datetime.datetime.strptime(f"{match_group[match_group.find(':')+2:]}",
                                                  "%B %d, %Y")

        return None

    @property
    def hometown(self):
        return self.driver_info('Home')

    @property
    def birth_date(self):
        return self.driver_info('Born')

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
    def cup_stats(self):
        """
        the drivers cup stats aggregated by year
        :return:
        """
        df = self.get_table(self.page, 7)

        # fill the rank NaN with their average career rank
        # if they don't have a rank, it's probably because
        # they didn't run enough races to qualify so just
        # leave it as is.
        try:
            df['Rank'] = df['Rank'].fillna(df['Rank'].mean()).astype(int)
        except:
            pass

        # return the dataframe
        return df

    # get the season stats
    def get_season(self, year):
        # build the url to the season stats sheet

        stats_url = F"/drivdet/{self.driver_key}/{year}/W"

        # fetch the page to scrape.
        stats_page = self.fetch_page(stats_url)

        # next get the table dataframe.
        table = self.get_table(stats_page, 4)

        return table

    # get a drivers career stats at any track
    def track_history(self, track):
        """
        fetch the drivers career statistics for
        any track the driver has driven at.
        :param track: the name of the track
        :return:
        """

        # track name in url
        track_key = track.replace(' ', '_')

        # the track page contains a link to
        # viewing all cup drivers at the track,
        # that needs to be extracted.
        track_page = self.fetch_page(F"/tracks/{track_key}")

        # the table containing the link
        table = track_page.find_all('table')[6]

        # url that contains track ID
        url = table.find('a').get('href')

        # pull the track ID out of that url
        start = len('/trackdet/')
        track_id = url[start: url.find('/', start+1)]

        # with the track ID extracted, a URL to the
        # drivers history at the track can be constructed.
        query_params = {'id': self.driver_key, 'trk': str(track_id), 'series': 'W'}
        track_history_url = "driverlog"

        # the drivers history at the track page.
        track_history_page = self.fetch_page(track_history_url, query_params)

        # finally the dataframe of the driver track history
        df = self.get_table(track_history_page, 4)

        return df
