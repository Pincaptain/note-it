from mongoengine import connect

from models.note import Note


class NoteRepository:
    """
    Repository for note model.
    """

    def __init__(self, database, **kwargs):
        """
        Initialize the note repository by connecting to the
        database using provided kwargs.

        :param database: Database to connect to. (String)
        :param kwargs: Set of options for database connection. (*=*)
        """

        connect(database, **kwargs)

    def create(self, note: Note):
        """
        Saves the note to the database.

        :param note: Note to save. (Note)
        :return: Returns the saved note. (Note)
        """

        return note.save()

    def delete(self, **kwargs):
        """
        Deletes single note matching :param kwargs: from database.

        :param kwargs: Set of filters for database objects. (*=*)
        :return: Returns the count of deleted objects. (Int)
        """

        return Note.objects(**kwargs).first().delete()

    def delete_many(self, **kwargs):
        """
        Deletes multiple notes matching :param kwargs: from database.

        :param kwargs: Set of filters for database objects. (*=*)
        :return: Returns the count of deleted objects. (Int)
        """

        return Note.objects(**kwargs).delete()

    def update(self, id: str, **kwargs):
        """
        Update single note matching :param kwargs: using :param update: from database.

        :param id: Id of the note to update. (String)
        :param kwargs: Set of updates to be applied to the specified note. (*=*)
        :return: Returns the count of updated objects. (Int)
        """

        return Note.objects(id=id).first().update(**kwargs)

    def update_many(self, id: str, **kwargs):
        """
        Update multiple notes matching :param kwargs: using :param update: from database.

        :param id: Id of the note to update. (String)
        :param kwargs: Set of updates to be applied to the specified note. (*=*)
        :return: Returns the count of updated objects. (Int)
        """

        return Note.objects(id=id).update(**kwargs)

    def get(self, **kwargs):
        """
        Get single note matching :param kwargs: from database.

        :param kwargs: Set of filters for database objects. (*=*)
        :return: Returns a single note. (Note)
        """

        return Note.objects(**kwargs).first()

    def get_many(self, skip: int = None, limit: int = None, **kwargs):
        """
        Get multiple notes matching :param kwargs: from database.

        :param skip: Skips :param skip: note objects from the start. (Int)
        :param limit: Sets the limit of note objects to retrieve. (Int)
        :param kwargs: Set of filters for database objects. (*=*)
        :return: Returns a list of notes. (List[Note])
        """

        return Note.objects(**kwargs).limit(limit).skip(skip)

    def get_many_sorted(self, skip: int = None, limit: int = None, *args: str, **kwargs):
        """
        Get multiple notes matching :param kwargs:
        sorted using :param args: from database.

        :param skip: Skips :param skip: note objects from the start. (Int)
        :param limit: Sets the limit of note objects to retrieve. (Int)
        :param args: Set of string used to specify ordering. (String...)
        :param kwargs: Set of filters for database objects. (*=*)
        :return: Returns a list of notes. (List[Note])
        """

        return Note.objects(**kwargs).order_by(*args).limit(limit).skip(skip)
