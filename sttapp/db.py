from peewee import *

database = SqliteDatabase("./instance/db.db")


class BaseModel(Model):
    class Meta:
        database = database


class Call(Model):
    path = CharField()
    incoming = BooleanField()
    initiating = IntegerField()
    receiving = IntegerField()
    text = CharField()
    date_time = DateTimeField()
    duration = FloatField()

    class Meta:
        database = database
