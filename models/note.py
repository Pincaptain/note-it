import datetime

from mongoengine import Document, StringField, ListField, DateTimeField


class Note(Document):
    """
    Representation of a note.

    :cvar title: Title of the note. (String)
    :cvar body: The content of the note. (String)
    :cvar tags: List of tags/keywords. (List[String])
    :cvar author: The author of the note. (String)
    :cvar date: The date and time of creation. (DateTime)
    :cvar meta: Used to specify document meta data like the name of the collection in this instance (Dictionary)
    """

    title = StringField(max_length=64, required=True)
    body = StringField(required=True)
    tags = ListField(required=True)
    author = StringField(max_length=256, required=True)
    date = DateTimeField(default=datetime.datetime.now)
    meta = {'collection': 'notes'}
