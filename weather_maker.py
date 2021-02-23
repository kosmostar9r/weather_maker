import datetime

import requests
from bs4 import BeautifulSoup


class WeatherMaker:

    def __init__(self, start_date, end_date):
        self.start_date = start_date.split('-')
        self.end_date = end_date.split('-')
        self.delta = datetime.timedelta(days=1)

        try:
            self.start_date = datetime.date(year=int(self.start_date[2]),
                                            month=int(self.start_date[1]),
                                            day=int(self.start_date[0]))
            self.end_date = datetime.date(year=int(self.end_date[2]),
                                          month=int(self.end_date[1]),
                                          day=int(self.end_date[0]))
        except ValueError:
            print('incorrect date')
        except TypeError:
            print('incorrect date')
        self.weather_info = []

    def _format_date(self, date):
        """format users date to put in url"""
        self.start_date_formated = date.strftime('%Y-%m-%d')
        self.start_date_formated = self.start_date_formated.split('-')
        if self.start_date_formated[2].startswith('0'):
            self.start_date_formated[2] = self.start_date_formated[2][1:]
        if self.start_date_formated[1].startswith('0'):
            self.start_date_formated[1] = self.start_date_formated[1][1:]
        self.start_date_formated = '-'.join(self.start_date_formated)

    def get_forecast(self):
        days_delta = self.end_date - datetime.date.today()
        if days_delta.days >= 10:
            print('can`t predict weather for more than 10 days forward\ntry again')
            return
        else:
            while self.start_date <= self.end_date:
                self._format_date(self.start_date)
                day_url_snippet = f'https://darksky.net/details/55.7616,37.6095/{self.start_date_formated}/si12/en'

                self.analyze_date(day_url_snippet)
                self.start_date += self.delta

    def analyze_date(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                html_doc = BeautifulSoup(response.text, features='html.parser')
                weather_details = html_doc.find_all('div', {'class': 'temperature'})
                weather_overview = html_doc.find('p', {'id': 'summary'})
                for item in weather_details:
                    self.weather_info.append({
                        'date': self.start_date,
                        'temperature': item.find('span', {'class': 'num'}).get_text(),
                        'overview': weather_overview.get_text().replace('\xa0', ' ')
                    })
            else:
                print(f'script ended with status code {response.status_code}')
        except Exception as exc:
            print(exc)


if __name__ == '__main__':
    start_day = datetime.date.today()
    end_day = datetime.date(year=start_day.year, month=start_day.month, day=start_day.day + 4)
    wm = WeatherMaker(start_day.strftime('%d-%m-%Y'), end_day.strftime('%d-%m-%Y'))
    wm.get_forecast()
