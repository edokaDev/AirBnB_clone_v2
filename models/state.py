#!/usr/bin/python3
"""State Module for HBNB project."""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import Relationship
from datetime import datetime
from .city import City


class State(BaseModel, Base):
    """State class."""

    __tablename__ = "states"
    id = Column(String(60), primary_key=True, nullable=False)
    name = Column(String(128), nullable=False)
    cities = Relationship('City',
                          backref='states',
                          cascade='all, delete-orphan')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    @property
    def cities(self):
        """Returns a list of cities that have the same state_id as State.id."""
        from models import storage
        all_cities_dict = storage.all(City)
        cities_list = []
        for city in all_cities_dict.keys():
            if all_cities_dict[city].state_id == self.id:
                cities_list.append(all_cities_dict[city])
        return cities_list
