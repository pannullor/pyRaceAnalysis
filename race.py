from pyRaceAnalysis.scraper import Scraper

import pprint


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

    @property
    def url(self):
        return '{}/race/{}_{}/W'.format(self.domain, self.year, self.name.replace(' ', '_'))

    def winner(self):
        page = self.fetch_page(self.url)

        # 6th table down is results on
        # the race page
        driver_table = page.find_all('table')[6]

        row = driver_table.find('tr', {'class': 'odd'})

        return row.find_all('td')[3].find('a').text

    def average_green_flag_run(self):
        page = self.fetch_page(self.url)

        caution_table = page.find_all('table')[9]

        # green flag runs are in the row
        # marked up with the even class.
        runs = caution_table.find_all('tr', {'class': 'even'})

        run_lengths = []
        for run in runs:
            total_laps = int(run.find_all('td')[3].text)
            run_lengths.append(total_laps)

        average = sum(run_lengths) / len(runs)

        print(average)



