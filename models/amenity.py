#!/usr/bin/python3
""" Amenity Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, DateTime, Table, ForeignKey
from datetime import datetime
from sqlalchemy.orm import Relationship

association_table = Table(
    'place_amenity', Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False)
)

class Amenity(BaseModel, Base):
    """Amenity class."""

    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    place_amenities = Relationship('Place', secondary=association_table, viewonly=False)
