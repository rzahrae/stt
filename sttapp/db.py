from peewee import *

database = SqliteDatabase("./instance/db.db")


class BaseModel(Model):
    class Meta:
        database = database


class Call(Model):
    path = CharField()
    incoming = BooleanField(null=True)
    number1 = IntegerField(null=True)
    number2 = IntegerField(null=True)
    text = CharField(null=True)
    date_time = DateTimeField(null=True)
    duration = FloatField(null=True)

    class Meta:
        database = database
