from bs4 import BeautifulSoup
import requests

import re
import pandas as pd


# race scraper for any race at
# any track, given that race has
# actually been run of course.
class Scraper(object):
    domain = 'https://racing-reference.info'

    # helper method to get the soup
    # object of any url
    def fetch_page(self, relative_url, query_params=None):
        url = F"{self.domain}{relative_url}"

        if query_params:
            r = requests.get(url, params=query_params)
        else:
            r = requests.get(url)

        # return the soup if a 200 success
        # otherwise raise an exception.
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'lxml')
            return soup
        else:
            raise Exception(F"Error with fetching url {r.url} -- status code {r.status_code} ")

    @staticmethod
    def get_table(page, index=None, match='.+'):
        """
        return the HTML at the specified index as
        a pandas dataframe
        :param index:
        :return: table as dataframe
        """

        try:
            if index:
                table = page.find_all('table')[index]
                df = pd.read_html(str(table))[0]
            else:
                # no index provided, return the tables
                # found using a match.
                df = pd.read_html(str(page), match=match)
        except Exception as e:
            df = None

        return df

    def get_season(self, year):
        """
        get the season data for any given year.
        this will turn a list of div elements
        into a dataframe
        :param year:
        :return: dataframe
        """
        url = F"/season-stats/{year}/W"
        page = self.fetch_page(url)

        rows = page.find_all('div', {'class': 'table-row'})

        # regex that will be used to pull out the
        # year and race name from the URL
        race_re = re.compile(r'/(\d{4})_(.*)/W$')

        races = []
        for row in rows:

            # url to the race page. If we can't find a URL then
            # the race hasn't happened yet so that's our season.
            race_url = row.find('div', {'class': 'race-number'}).find('a')
            if race_url:
                race_url = race_url.get('href')
            else:
                break

            # can pull the year and race name portion out of
            # the full URL. with the match split, the year and name
            # portion are the second element in the list,
            # just split those and the name can be extracted.
            match = race_re.search(race_url).group().split('/')[1].split('_')
            del match[0]
            race_name = ' '.join(match)

            # need to pull the race track name out next
            race_track = row.find('div', {'class': 'track'}).find('a').get('href')
            race_track = race_track[race_track.rfind('/')+1:].replace('_', ' ')

            # next we can build the dictionary that will
            # become our dataframe.
            races.append({
                'name': race_name,
                'date': row.find('div', {'class': 'date'}).text,
                'cars': row.find('div', {'class': 'cars'}).text,
                'track': race_track,
                'winner': row.find('div', {'class': 'winners'}).find('a').text.replace('.', '').replace(',', ''),
                'start': row.find('div', {'class': 'st'}).text,
                'manufacturer': row.find('div', {'class': 'manufacturer'}).text,
                'lap_distance': row.find('div', {'class': 'len'}).text,
                'surface': row.find('div', {'class': 'sfc'}).text,
                'distance': row.find('div', {'class': 'miles'}).text,
                'pole_speed': row.find('div', {'class': 'pole'}).text,
                'cautions': row.find('div', {'class': 'cautions'}).text,
                'caution_laps': row.find_all('div', {'class': 'laps'})[1].text,
                'average_speed': row.find('div', {'class': 'speed'}).text,
                'lead_changes': row.find('div', {'class': 'lc'}).text
            })

        season_df = pd.DataFrame(races)

        return season_df


