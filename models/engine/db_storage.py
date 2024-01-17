#!/usr/bin/python3
"""New engine DBStorage which uses sql"""
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """New Storage engine that uses the database"""
    __engine = None
    __session = None

    def __init__(self):
        """create the engine (self.__engine)
        the engine must be linked to the MySQL database
        and user created before
        """
        user = os.environ.get('HBNB_MYSQL_USER')
        pwd = os.environ.get('HBNB_MYSQL_PWD')
        host = os.environ.get('HBNB_MYSQL_HOST', 'localhost')
        db = os.environ.get('HBNB_MYSQL_DB')
        env = os.environ.get('HBNB_ENV')

        """Create the engine"""
        self.__engine = create_engine(
                'mysql+mysqldb://{}:{}@{}:3306/{}'.
                format(user, pwd, host, db),
                pool_pre_ping=True)

        """Drop tables if environment is test"""
        if env == 'test':
            self.__engine.echo = True  # For debugging purposes
            self.__engine.execute("DROP TABLE IF EXISTS cascade")


        """Create all tables if not in test environment"""
        if env != 'test':
            Base.metadata.create_all(self.__engine)

        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()

    def all(self, cls=None):
        """Query on the current database session (self.__session)
        all objects depending on the class name (argument cls).
        if cls=None, query all types of objects
        this method must return a dictionary: (like FileStorage)
        """
        my_class = {'State': State, 'City': City
                }
        obj_dict = {}
        for class_name, mapped_class in my_class.items():
            if cls is None or cls == mapped_class.__name__:
                objs = self.__session.query(mapped_class).all()
                for obj in objs:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)
        print(f"Added {obj} to the session")

    def delete(self, obj):
        """delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def reload(self):
        """create all tables in the database (feature of SQLAlchemy)"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
                sessionmaker(bind=self.__engine,
                             expire_on_commit=False))
