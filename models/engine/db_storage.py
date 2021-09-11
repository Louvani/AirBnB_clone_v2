#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage():
    """ Class DBStorage"""
    __engine = None
    __session = None

    def __init__(self):
        '''Constructor for the class DBStorage'''
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            getenv('HBNB_MYSQL_USER'), getenv('HBNB_MYSQL_PWD'), getenv(
                'HBNB_MYSQL_HOST'), getenv('HBNB_MYSQL_DB')),
            pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''Query for the current database that bring all objects'''
        new_list = []
        if cls is None:
            #  [User, State, City, Amenity, Place, Review]
            cls_list = [User, State, City, Amenity, Place, Review]
            for class_name in cls_list:
                new_list += self.__session.query(class_name).all()
        else:
            new_list += self.__session.query(cls).all()
        new_dict = {}
        for obj in new_list:
            key = obj.__class__.__name__ + '.' + str(obj.id)
            new_dict[key] = obj
        return new_dict

    def new(self, obj):
        '''Add a new object to the current database'''
        self.__session.add(obj)

    def save(self):
        '''Save the current session'''
        self.__session.commit()

    def delete(self, obj=None):
        '''Delete from the current session'''
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        '''Create all the datatble and create the new session'''
        Base.metadata.create_all(self.__engine)
        session_fact = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_fact)
        self.__session = Session()

    def close(self):
        '''Close the current session'''
        self.__session.close()
