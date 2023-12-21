#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.orm import Relationship
from datetime import datetime


class City(BaseModel, Base):
    """ The city class, contains state ID and name """

    __tablename__ = "cities"
    state_id = Column(String(60), ForeignKey('states.id'),
                      nullable=False)
    name = Column(String(128), nullable=False)
    places = Relationship('Place', backref='cities', cascade='all, delete-orphan')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
