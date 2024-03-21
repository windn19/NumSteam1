from datetime import datetime

from peewee import PostgresqlDatabase, Model, DateTimeField, CharField, TextField

from settings import postgre


# db = SqliteDatabase('../base.db')
db = PostgresqlDatabase(**postgre)


class Numbers(Model):
    datetime = DateTimeField(primary_key=True, default=datetime.now())
    num = CharField(max_length=9)
    crop = CharField(max_length=100)
    image = CharField(max_length=100)
    res = TextField()
    cam_name = CharField(max_length=10)

    class Meta:
        database = db
        table_name = 'base'
    
    def __str__(self):
        return f'{self.datetime.strftime("%d.%m.%Y-%H:%M")} создана запись с номером {self.num} с камеры {self.cam_name}'


db.create_tables([Numbers])

