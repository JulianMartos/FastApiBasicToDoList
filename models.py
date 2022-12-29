import datetime
from peewee import SqliteDatabase, Model, IntegerField, CharField, BooleanField, DateTimeField

db = SqliteDatabase('todo.sqlite3')


class BaseModel(Model):
    class Meta:
        database = db


class Todo(BaseModel):
    __tablename__ = 'todos'
    id = IntegerField(primary_key=True)
    task = CharField()
    completed = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now)

    def toJson(self):
        return {
            "id":self.id,
            "task":self.task,
            "completed":self.completed,
            "created":str(self.created_at)
        }