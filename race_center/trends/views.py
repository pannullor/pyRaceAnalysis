from django.http import HttpResponse
from django.views import View

from racing_reference.api.race import Race

import datetime
import pprint


class RaceView(View):

    def get(self, request, *args, **kwargs):
        name = kwargs['name']
        year = datetime.datetime.today().year

        # the object
        race = Race(year, name)

        # flag breakdown
        breakdown = race.flag_breakdown('yellow')

        total_cautions = race.total_cautions
        total_caution_laps = race.total_caution_laps

        return HttpResponse('Total Cautions: {} \n'
                            'Total Caution Laps: {} \n'
                            'Race Length: {}'.format(
                                total_cautions,
                                total_caution_laps,
                                race.race_length
                                ))


