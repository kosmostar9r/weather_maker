import argparse
import datetime

import weather_maker as wm
import database_updater as dm
import image_maker as im

INIT_END_DATE = datetime.date.today()
INIT_START_DATE = datetime.date(year=INIT_END_DATE.year, month=INIT_END_DATE.month, day=INIT_END_DATE.day - 7)


def str_to_bool(string):
    if isinstance(string, bool):
        return string
    if string.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif string.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


class WeatherManager:

    def __init__(self):
        self.weather_parser = argparse.ArgumentParser('Weather application.'
                                                      'It cans show you weather in Moscow'
                                                      ' for the dates you want using darksky.net.'
                                                      '\nFor more info type -h or --help.')

    def add_arguments(self):
        self.weather_parser.add_argument('-s', '--start_date', required=False, help='Type the first date of period '
                                                                                    'you want to check weather.\n'
                                                                                    'Pattern: "dd-mm-yyyy".\n'
                                                                                    'Note: application can'
                                                                                    ' give you correct weather '
                                                                                    'no further than 10 day forward.')
        self.weather_parser.add_argument('-e', '--end_date', required=False, help='Type the second date of period '
                                                                                  'you want to check weather.\n'
                                                                                  'Pattern: "dd-mm-yyyy".\n'
                                                                                  'Note: application can'
                                                                                  ' give you correct weather '
                                                                                  'no further than 10 day forward.')
        self.weather_parser.add_argument('-w', '--write_to_db', required=False, type=str_to_bool,
                                         help='Write down the forecast for given dates to database.')
        self.weather_parser.add_argument('-r', '--read_from_db', required=False, type=str_to_bool,
                                         help='Read info from database for given dates.')
        self.weather_parser.add_argument('-c', '--weather_card', required=False, type=str_to_bool,
                                         help='Make card with weather info.')
        self.weather_parser.add_argument('-g', '--get_forecast', required=False, type=str_to_bool,
                                         help='Show in console forecast for given dates.')

        self.weather = self.weather_parser.parse_args()

    def run(self):
        self.add_arguments()
        if self.weather.start_date is None \
                and self.weather.end_date is None \
                and self.weather.write_to_db is None \
                and self.weather.read_from_db is None \
                and self.weather.weather_card is None \
                and self.weather.get_forecast is None:
            option = WeatherOptions()
            option.forecaster()
        else:
            option = WeatherOptions(self.weather.start_date,
                                    self.weather.end_date)
            if self.weather.write_to_db:
                option.db_writer()
            elif self.weather.read_from_db:
                option.db_reader()
            elif self.weather.weather_card:
                option.card_maker()
            elif self.weather.get_forecast:
                option.forecaster()


class WeatherOptions:

    def __init__(self, start_date=INIT_START_DATE.strftime('%d-%m-%Y'), end_date=INIT_END_DATE.strftime('%d-%m-%Y')):
        self.start_date = start_date
        self.end_date = end_date

    def db_writer(self):
        weather_maker = dm.DatabaseUpdater(self.start_date, self.end_date)
        weather_maker.write_to_db()
        print('Written to database')

    def db_reader(self):
        weather_maker = dm.DatabaseUpdater(self.start_date, self.end_date)
        weather_maker.read_from_db()
        print('Dates got form db.')

    def card_maker(self):
        print('Drawing image...')
        weather_maker = im.ImageMaker(self.start_date, self.end_date)
        weather_maker.weather_card()
        print('Weather cards saved at "weather_images"')

    def forecaster(self):
        print('Collecting data...')
        weather_maker = wm.WeatherMaker(self.start_date, self.end_date)
        weather_maker.get_forecast()
        for item in weather_maker.weather_info:
            print(f'Date : {item["date"]}, temperature : {item["temperature"]}, overview : {item["overview"]}')


manager = WeatherManager()
manager.run()

# $ python3 console_access.py
# $ python3 console_access.py -s 20-02-2021 -e 22-02-2021 -g true