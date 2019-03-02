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

        # race results
        self.results = self.get_table(self.page, 6)

    def race_details(self):
        """
        method to get the race details like
        scheduled distance, laps, track type.
        :return:
        """

        # get the raw page text so we can hit
        # it with the distance regex to get
        # the races scheduled distance and laps
        raw_text = self.page.text

        # the regex we can use to pull out the info
        distance_re = re.compile(r'(\d+) laps\*? on a (\d?\.\d{3}) mile (.*) \((\d+\.\d+) miles\)', re.IGNORECASE)
        match = distance_re.search(raw_text)
        return match

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

        return stats_str

    def speed_info(self):
        """
        regex uses to capture the average speed,
        the pole speed, and the margin of victory.
        :return:
        """
        stats = self.race_info()

        speed_re = re.compile(r': (\d{1,3}\.\d{2,3})', re.IGNORECASE)
        result = speed_re.findall(stats)
        return result

    def caution_info(self):
        stats = self.race_info()
        cautions_re = re.compile(r'\d{1,3} for \d{1,3} laps', re.IGNORECASE)
        match = cautions_re.search(stats)
        return match.group().split()

    @property
    def winner(self):
        return self.results.iloc[0]

    @property
    def laps_run(self):
        return self.results.iloc[0]['Laps']

    @property
    def total_cautions(self):
        return self.caution_info()[0]

    @property
    def total_caution_laps(self):
        return self.caution_info()[2]

    @property
    def average_speed(self):
        return F"{self.speed_info()[0]} MPH"

    @property
    def pole_speed(self):
        return F"{self.speed_info()[1]} MPH"

    @property
    def margin_of_victory(self):
        return F"{self.speed_info()[2]} Sec"

    @property
    def scheduled_laps(self):
        return self.race_details()[1]

    @property
    def lap_distance(self):
        return self.race_details()[2]

    @property
    def track_type(self):
        return self.race_details()[3]

    @property
    def scheduled_distance(self):
        return self.race_details()[4]

    @property
    def length(self):
        stats = self.race_info()

        time_re = re.compile(r'Time of race: ([01]?\d|2[0-3]):([0-5]?\d):([0-5]?\d)')
        result = time_re.search(stats)
        return result[0].split(': ')[1]

    @property
    def lead_changes(self):
        stats = self.race_info()

        lead_re = re.compile(r'(Lead changes:) (\d{1,3})', re.IGNORECASE)
        match = lead_re.search(stats)
        return match.group().split(': ')[1]

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
