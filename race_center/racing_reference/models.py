from django.db import models

from enum import Enum


class StateChoice(Enum):
    AL = 'Alabama'
    AK = 'Alaska'
    AZ = 'Arizona'
    AR =  'Arkansas'
    CA = 'California'
    CO = 'Colorado'
    CT = 'Connecticut'
    DE = 'Delaware'
    FL = 'Florida'
    GA = 'Georgia'
    HI = 'Hawaii'
    ID = 'Idaho'
    IL = 'Illinois'
    IN = 'Indiana'
    IA = 'Iowa'
    KS = 'Kansas'
    KY = 'Kentucky'
    LA = 'Louisiana'
    ME = 'Maine'
    MD = 'Maryland'
    MA = 'Massachusetts'
    MI = 'Michigan'
    MN = 'Minnesota'
    MS = 'Mississippi'
    MO = 'Missouri'
    MT = 'Montana'
    NE = 'Nebraska'
    NV = 'Nevada'
    NH = 'New Hampshire'
    NJ = 'New Jersey'
    NM = 'New Mexico'
    NY = 'New York'
    NC = 'North Carolina'
    ND = 'North Dakota'
    OH = 'Ohio'
    OK = 'Oklahoma'
    OR = 'Oregon'
    PA = 'Pennsylvania'
    RI = 'Rhode Island'
    SC = 'South Carolina'
    SD = 'South Dakota'
    TN = 'Tennessee'
    TX = 'Texas'
    UT = 'Utah'
    VT = 'Vermont'
    VA = 'Virginia'
    WA = 'Washington'
    WV = 'West Virginia'
    WI = 'Wisconsin'
    WY = 'Wyoming'


class Track(models.model):
    # name of the race
    name = models.CharField(max_length=200)

    # track location
    city = models.CharField(max_length=50)
    state = models.IntegerField(choices=[(tag, tag.value) for tag in StateChoice])

    # length in miles
    length = models.FloatField()

    # date of first race
    first_race = models.DateField()
    last_race = models.DateField()

    TrackTypeChoices = (
        (1, 'Intermediate'),
        (2, 'Superspeedway'),
        (3, 'Intermediate'),
        (4, 'Short Track')
    )
    type = models.IntegerFIeld(TrackTypeChoices)

class Race(models.model):
    # name of the race
    name = models.CharField(max_length=200)

    # track race occurred at
    track = models.ForeignKey('Track', related_name='races')

    # race length in miles
    distance = models.IntegerField()

    # race length in time
    length = models.TimeField()

    # date of race
    date = models.DateField()

    # race time of day
    race_start = models.TimeField()

    # total caution laps
    caution_laps = models.IntegerField(default=0)

    # total number of cautions
    caution_flags = models.IntegerField(default=0)

    # surface of the track
    SurfaceChoices = (
        (1, 'Paved'),
        (2, 'Road'),
        (3, 'Dirt')
    )
    surface = models.IntegerField(choices=SurfaceChoices)

    # lap length
    lap_length = models.FloatField()


class Driver(models.model):
    name = models.CharField(max_length=200)

    birth_date = models.DateField()

    home_city = models.CharFIeld()
    home_state = models.IntegerField(choices=[(tag, tag.value) for tag in StateChoice])

    career_starts = models.IntegerField(default=0)
    career_wins = models.IntegerField(default=0)


class RaceResult(models.model):
    race = models.ForeignKey('Race')
    driver = models.ForeignKey('Driver', related_name='drivers')

    starting_position = models.IntegerField()
    finishing_position = models.IntegerField()

    sponsor = models.CharField(max_length=100)
    owner = models.ForeignKey('Owner')

    CarChoices = (
        (1, 'Ford'),
        (2, 'Chevrolet'),
        (3, 'Toyota'),
        (4, 'Dodge'),
        (5, 'Pontiac')
    )
    car = models.IntegerField(choices=CarChoices)

    laps_completed = models.IntegerField()

    StatusChoices = (
        (1, 'Running'),
        (2, 'Crash'),
        (3, 'Mechanical'),
        (4, 'Parked')

    )
    status = models.CharField


class Owner(models.model):
    name = models.CharField(max_lenght=100)
