#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from .review import Review
from .amenity import Amenity
import os

class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    reviews = relationship('Review', backref='places', cascade='all, delete-orphan')
    amenity_ids = []

    @property
    def reviews(self):
        """Returns a list of Review intances that have the same place_id as Place.id."""
        from models import storage
        all_reviews_dict = storage.all(Review)
        reviews_list = []
        for review in all_reviews_dict.keys():
            if Review.id in review:
                reviews_list.append(all_reviews_dict[review])
        return reviews_list

    @property
    def amenities(self):
        """Getter attribute amenities that returns the list of Amenity instances based on the attribute amenity_ids"""
        from models import storage

        amenities_list = []
        for amenity_id in self.amenity_ids:
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                amenities_list.append(amenity)
        return amenities_list

    @amenities.setter
    def amenities(self, obj):
        """Setter attribute amenities that handles append method for adding \
        an Amenity.id to the attribute amenity_ids"""
        if isinstance(obj, Amenity):
            self.amenity_ids.append(obj.id)

if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    Place.amenities = relationship('Amenity',
                                   secondary='place_amenity',
                                   viewonly=False,
                                   backref='places')

