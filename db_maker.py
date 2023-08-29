import datetime
from peewee import *

db = SqliteDatabase('people.db')

class Person(Model):
    username = CharField()
    city = CharField()
    date1 = CharField(null=True)
    date2 = CharField(null=True)
    command = CharField()
    minimum = IntegerField(null=True)
    photo = CharField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = db

class Hotel(Model):
    owner = ForeignKeyField(Person, backref='htls')
    hotel_name = CharField()
    class Meta:
        database = db

#
# with db:
#     db.create_tables([Person, Hotel])