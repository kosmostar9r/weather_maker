import datetime

from weather_maker import WeatherMaker
from playhouse.db_url import connect
from weather_database import Weather


class DatabaseUpdater(WeatherMaker):

    def __init__(self, start_date, end_date):
        super().__init__(start_date, end_date)
        self.db = connect('sqlite:///weather.db')
        self.got_from_db_dates = []

    def read_from_db(self):
        with self.db:
            days_info = Weather.select().where(Weather.date.between(self.start_date, self.end_date))
            for day in days_info:
                day_info = {'date': day.date,
                            'temperature': day.temperature,
                            'overview': day.overview}
                self.got_from_db_dates.append(day_info)
        print('Dates got form db.')

    def write_to_db(self):
        self.get_forecast()
        with self.db:
            self.db.create_tables([Weather])
            for day in self.weather_info:
                weather, created = Weather.get_or_create(
                    date=day['date'],
                    defaults={'temperature': day['temperature'],
                              'overview': day['overview']})
                if not created:
                    Weather.update(temperature=day['temperature'],
                                   overview=day['overview']).where(Weather.date == weather.date).execute()
        print('Written to database')


if __name__ == '__main__':
    start_day = datetime.date.today()
    end_day = datetime.date(year=start_day.year, month=start_day.month, day=start_day.day + 3)
    weather_db = DatabaseUpdater(start_day.strftime('%d-%m-%Y'), end_day.strftime('%d-%m-%Y'))
    weather_db.write_to_db()
    weather_db.read_from_db()
