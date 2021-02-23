import peewee

db = peewee.SqliteDatabase('weather.db')


class BaseTable(peewee.Model):
    class Meta:
        database = db


class Weather(BaseTable):
    temperature = peewee.CharField()
    overview = peewee.CharField()
    date = peewee.DateField(unique=True)
