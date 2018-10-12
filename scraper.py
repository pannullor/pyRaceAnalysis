from bs4 import BeautifulSoup
import requests


# race scraper for any race at
# any track, given that race has
# actually been run of course.
class Scraper(object):
    domain = 'http://racing-reference.info'

    # helper method to get the soup
    # object of any url
    @staticmethod
    def fetch_page(url):
        r = requests.get(url)

        # return the soup if a 200 success
        # otherwise raise an exception.
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            return soup
        else:
            raise Exception("Error with fetching url {} -- status code {} ".format(url, r.status_code))

