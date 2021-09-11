#!/usr/bin/python3
""" State Module for HBNB project """
from models.city import City
from sqlalchemy import Column, Integer, String, ForeignKey
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship, backref
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)
    cities = relationship('City', cascade="all, delete", backref='state')

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """
            getter attribute cities that returns the list of City instances
            with state_id equals to the current State.id
            """
            from models import storage
            from models.city import City
            new_list = []
            for key, value in storage.all(City).items():
                if self.id == value.state_id:
                    new_list.append(value)
            return new_list
