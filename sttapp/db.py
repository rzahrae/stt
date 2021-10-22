from peewee import *

database = SqliteDatabase("./instance/db.db")

class BaseModel(Model):
    class Meta:
        database = database

class Call(Model):
    path = CharField()
    incoming = BooleanField(null = True)
    extension = IntegerField(null = True)
    text = CharField(null = True)
    date_time = DateTimeField(null = True)
    duration = TimeField(null = True)

    class Meta:
        database = database