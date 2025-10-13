from flask_mongoengine import MongoEngine
import datetime

db = MongoEngine()

class Memory(db.Document):
    title = db.StringField(required=True, max_length=100)
    story = db.StringField(required=True)
    event_date = db.DateTimeField(required=True)
    image_filename = db.StringField(required=True)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'memories'}