
from models import db, Todo

with db:
    db.create_tables([Todo])