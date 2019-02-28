from django.core.management.base import BaseCommand
import datetime

from racing_reference.scraper import Scraper
from racing_reference.api.driver import Driver as racer
from racing_reference.api.race import Race as rr_race
from racing_reference.api.track import Track as rr_track

from racing_reference.models import Driver, Race, RaceResult, Track, Owner, StateChoice

class Command(BaseCommand):

    def handle(self, **options):
        """
        populate the database with nascar data
        from the 1972 daytona 500 to today. This
        time is the nascar modern era and that's
        what we'll be analyzing
        :param options:
        :return:
        """

        # Base scraper object
        s = Scraper()

        season = s.get_season('2004')
        #
        # # next step is to go through and create
        # # each race for that season.
        # races = season['races'].tolist()

        for race in season.itertuples():
            # create a racing reference race
            # scraper to data not available
            # in the season race data
            rr = rr_race(race.name)

            # build race data
            race_data = {
                'name': race.name,
                'track': race.track,
                'date': race.date,
                'lap_distance': race.lap_distance,
                'distance': race.distance,
                'surface': race.surface,
                'caution_flags': race.cautions,
                'caution_laps': race.caution_laps,
                'lead_changes': race.lead_changes,
                'length': rr.race_length
            }

        # # get the active driver list to populate.
        # active_driver_page = s.fetch_page('/active_drivers')
        # driver_table = Scraper.get_table(active_driver_page, 5)
        #
        # # if a driver drives in cup just replace any other
        # # series key with cup since we're specifically working
        # # with the cup sereies here
        # def find_cup(value):
        #     if value.find('Cup') > -1:
        #         return 'Cup'
        #     return value
        # driver_table['Series'] = driver_table['Series'].apply(find_cup)
        #
        # # filter the df down to cup drivers
        # driver_table = driver_table[driver_table['Series'] == 'Cup']
        #
        # for driver in driver_table.itertuples():
        #     # turn the drivers birthday into a date field
        #     date_born = datetime.datetime.strptime(driver.Born, '%m-%d-%Y').date()
        #
        #     # so for drivers with a suffix their name
        #     # is output first last, suffix. We need to
        #     # strip that formatting out.
        #     name = driver.Driver.replace('.', '').replace(',', '')
        #
        #     driver_data = {
        #         'name': name,
        #         'date_born': date_born,
        #         'home': driver.Home
        #     }
        #     d = racer(name)
        #
        #     # get the drivers stats in cup.
        #     cup_stats = d.cup_stats
        #     career_starts = cup_stats['Races'].iloc[-1]
        #     career_wins = cup_stats['Win'].iloc[-1]
        #
        #     driver_data.update(
        #         {
        #             'career_starts': career_starts,
        #             'career_wins': career_wins
        #         }
        #     )
        #
        #     d = Driver.objects.create(**driver_data)

