from peewee import *
from flask_login import UserMixin

database = SqliteDatabase("./instance/db.db")


class BaseModel(Model):
    class Meta:
        database = database


class Inventory(Model):
    def refresh(self):
        return type(self).get(self._pk_expr())

    total_paths = IntegerField()
    skipped_paths = IntegerField()
    finished_paths = IntegerField()
    start_date = DateTimeField()
    end_date = DateTimeField(null=True)

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
    inventory = ForeignKeyField(Inventory, backref="calls")

    class Meta:
        database = database

class User(Model, UserMixin):
    username = CharField()
    password = CharField()

    class Meta:
        database = database  