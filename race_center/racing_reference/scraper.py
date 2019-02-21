from bs4 import BeautifulSoup
import requests

import pandas as pd


# race scraper for any race at
# any track, given that race has
# actually been run of course.
class Scraper(object):
    domain = 'https://racing-reference.info'

    # helper method to get the soup
    # object of any url
    def fetch_page(self, relative_url, query_params=None):
        url = "{}{}".format(self.domain, relative_url)

        print(url)
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
            raise Exception("Error with fetching url {} -- status code {} ".format(r.url, r.status_code))

    def get_table(self, page, index):
        """
        return the HTML at the specified index as
        a pandas dataframe
        :param index:
        :return: table as dataframe
        """

        table = page.find_all('table')[index]

        df = pd.read_html(str(table))[0]

        return df

