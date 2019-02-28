from racing_reference.scraper import Scraper

import re


class Race(Scraper):
    def __init__(self, year, name):
        """
        create an instance of a race from
        the given year, with the given name.
        :param year: (str) year race was run in YYYY format
        :param name: (str) name of the race
        """
        self.year = year
        self.name = name

        self.url = F"/race/{self.year}_{self.name.replace(' ', '_')}/W"

        # save the race page to reuse
        self.page = self.fetch_page(self.url)

        # 6th table down is results on
        # the race page
        self.results = self.get_table(self.page, 6)

    @property
    def winner(self):
        return self.results.iloc[0]

    def race_info(self):
        """
        Method is meant to return the basic race
        information as a list
        :return:
        """
        stats = self.get_table(self.page, 4)

        # stats is a two row, single column, dataframe.
        # the value for both rows in just a string so
        # concatenating them will make pulling the
        # particular info out easier.
        stats_str = F"{stats.iloc[0][0]} {stats.iloc[0][1]}"

        # split on the Capital letters that follow whitespace,
        # this will make each bit of info it's own element. It
        # this will also remove the first letter of each metric
        # but that's fine. the individual methods to pull the
        # data from this list will account for that.
        return re.split(' [A-Z]', stats_str)

    def caution_info(self, info='total'):
        """
        get the total number of cautions in this race
        :return:
        """

        stats = self.race_info()

        # caution info is the 3rd element if this changes
        # we'll come up with a more clever method. Split
        # that on the whitespace now and we can get the
        # total cautions and lap counts from the 1st and
        # 3rd elements respectively
        cautions = stats[3].split()

        # normalize info to all lower to check it
        info = info.lower()

        if info == 'total':
            return cautions[1]
        elif info == 'laps':
            return cautions[3]
        else:
            raise Exception("Invalid caution info. Valid values are total or laps.")

    @property
    def total_cautions(self):
        return self.caution_info('total')

    @property
    def total_caution_laps(self):
        return self.caution_info('laps')

    @property
    def race_length(self):
        stats = self.race_info()

        # race length is the 0th element.
        # split that again and take the
        # 1st element.
        return stats[0].split(': ')[1]

    def flag_breakdown(self, flag='green'):
        """
        breakdown of green and yellow flag laps
        :param flag: the flag to breakdown, default is green
        :return: dataframe of flag breakdown
        """
        flag_table = self.get_table(self.page, 10)

        # green flags start at index 2 and they're
        # every even index, yellow starts at 3 and
        # they're every odd index after.
        flag = flag.lower()
        if flag not in['green', 'yellow']:
            raise NameError(F"Flag {flag} is not valid. Must be either \'green\' or \'yellow.\'")

        index = 2 if flag == 'green' else 3

        # slice the dataframe from the index by 2 leaving
        # off the last row.
        df = flag_table.iloc[index:-1:2]

        return df
