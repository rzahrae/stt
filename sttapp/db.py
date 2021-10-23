from peewee import *

database = SqliteDatabase("./instance/db.db")


class BaseModel(Model):
    class Meta:
        database = database


class Call(Model):
    path = CharField()
    incoming = BooleanField(null=True)
    receiving = IntegerField(null=True)
    initiating = IntegerField(null=True)
    text = CharField(null=True)
    date_time = DateTimeField(null=True)
    duration = FloatField(null=True)

    class Meta:
        database = database
