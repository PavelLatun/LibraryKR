from peewee import *


class BookModel(Model):
    id = PrimaryKeyField(null=False)
    title = CharField(max_length=100)
    year = IntegerField()
    author = CharField(max_length=100)

    class Meta:
        db_table = "books"
        order_by = ("id",)
