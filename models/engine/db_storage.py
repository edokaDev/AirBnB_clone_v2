"""A class that will make and manage the database storage."""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


HBNB_MYSQL_USER = os.environ.get('HBNB_MYSQL_USER')
HBNB_MYSQL_PWD = os.environ.get('HBNB_MYSQL_PWD')
HBNB_MYSQL_HOST = os.environ.get('HBNB_MYSQL_HOST')
HBNB_MYSQL_DB = os.environ.get('HBNB_MYSQL_DB')
HBNB_ENV = os.environ.get('HBNB_ENV')


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """Creates an engine that links to the database."""
        self.__engine = create_engine(
            f'mysql+mysqldb://{HBNB_MYSQL_USER}:{HBNB_MYSQL_PWD}@{HBNB_MYSQL_HOST}/{HBNB_MYSQL_DB}',
            pool_pre_ping=True)

        if HBNB_ENV:
            if HBNB_ENV == 'test':
                Base.metadata.drop_all(self.engine)

    def all(self, cls=None):
        """"Returns a dictionary conataning <class>.<id>: <table_object>."""
        if cls is None:
            rows_dict = {}
            types = [User, State, City, Amenity, Place, Review]
            for table in types:
                row = []
                rows = self.__session.query(table).all()
                if len(rows) > 0:
                    for row in rows:
                        key = '.'.join(row.__class__, row.id)
                        value = row
                        rows_dict.update({key: value})
        else:
            rows = self.__session.query(cls).all()
            return rows

    def new(self, obj):
        """Adds a new object (table) to a session."""
        self.__session.add(obj)

    def save(self):
        """Commits the session changes to the database."""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an object from the database if its not None."""
        if obj:
            self.__session.delete(obj)
            self.__session.commit()

    def reload(self):
        """Creates all tables in the database."""
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
        Base.metadata.create_all(self.__engine)
