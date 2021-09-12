#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship, backref
from os import getenv
import models

metadata = Base.metadata
place_amenity = Table('place_amenity', metadata,
                      Column('place_id', String(60), ForeignKey(
                          'places.id'), primary_key=True, nullable=False),
                      Column('amenity_id', String(60), ForeignKey(
                          'amenities.id'), primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """

    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenities_id = []

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship(
            'Review', backref='place')
        amenities = relationship(
            'Amenity', secondary=place_amenity, viewonly=False)
    else:
        @property
        def reviews(self):
            """
            getter attribute cities that returns the list of Review instances
            with state_id equals to the current Place.id
            """
            from models.review import Review
            from models import storage
            new_list = []
            for value in storage.all(Review).values():
                if value.place_id == self.id:
                    new_list.append(value)
            return new_list

        @property
        def amenities(self):
            """
            Getter attribute amenities that returns the list of Amenity
            instances based on the attribute amenity_ids that contains all
            Amenity.id linked to the Place
            """
            from models.amenity import Amenity
            from models import storage
            new_list = []
            for key, value in storage.all(Amenity).items():
                if self.id == value.amenity_ids:
                    new_list.append(value)
            return new_list

        @amenities.setter
        def amenities(self, value):
            """Setter attribute amenities that handles append method for
            adding an Amenity.id to the attribute amenity_ids. This method
            should accept only Amenity object, otherwise, do nothing"""
            from models.amenity import Amenity

            if isinstance(value, Amenity):
                self.amenity_ids.append(value.id)
