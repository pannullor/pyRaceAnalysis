from pyRaceAnalysis.scraper import Scraper

import copy


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
        self.results = []

        # save the race page to reuse
        self.page = self.fetch_page(self.url)

        # 6th table down is results on
        # the race page
        driver_table = self.page.find_all('table')[6]

        # skip the first tr element as it's just
        # the table header and we don't need that.
        rows = driver_table.find_all('tr')[1:]

        for row in rows:
            td = row.find_all('td')

            # racing reference race results columns are
            # finish, start, number, name, sponsor/owner,
            # manufacturer, laps run, running status, laps
            # led, points, playoff points. We'll split the
            # sponsor and owner for our data.
            result = {
                'finish': td[0].text,
                'start': td[1].text,
                'number': td[2].text,
                'driver': td[3].find('a').text,
                'sponsor': td[4].find('b').text,
                'owner': td[4].find('a').text,
                'manufacturer': td[5].text,
                'laps_completed': td[6].text,
                'running_status': td[7].text,
                'laps_led': td[8].text,
                'points': td[9].text,
                'playoff_points': td[10].text,
            }

            self.results.append(result)

    @property
    def url(self):
        return '{}/race/{}_{}/W'.format(self.domain, self.year, self.name.replace(' ', '_'))

    @property
    def winner(self):
        return self.results[0]

    def race_statistics(self):
        """
        simple method to gather the basic
        stats shown on the top of the page
        :return: dictionary of basic race stats
        """
        stats_table = self.page.find_all('table')[4]

        data = {}
        for stat in stats_table.find_all('td'):
            stat_list = stat.text.split('\n')

            for i in range(1, len(stat_list)-1, 1):
                s = stat_list[i]
                dil = s.find(': ')
                data.update({
                    s[:dil]: s[dil+2:]
                })

        return data

    def flag_breakdown(self, flag='green'):
        """
        breakdown of green and yellow flag laps
        :param flag: the flag to breakdown, default is green
        :return:
        """
        flag_table = self.page.find_all('table')[9]

        # green flags are marked up as even and yellow
        # flags are marked as odd. Check to make sure
        # that no other flag was passed here.
        flag = flag.lower()
        if flag not in['green', 'yellow']:
            raise NameError('Flag {} is not valid. Must be either \'green\' or \'yellow.\'')

        marker = 'even' if flag == 'green' else 'odd'
        flag_laps = flag_table.find_all('tr', {'class': 'odd'})

        breakdown = []
        for lap in flag_laps:
            for bkd in lap.find_all('td'):
                data = {
                    'from_lap': bkd[1].text,
                    'to_lap': bkd[2].text,
                    'total_laps': bkd[3].text
                }
                if flag == 'yellow':
                    data.update({
                        'reason': bkd[4].text,
                        'free_pass': bkd[5].text
                    })

                breakdown.append(data)

        return breakdown
