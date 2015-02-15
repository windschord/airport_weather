# -*- coding:utf-8 -*-
from sqlalchemy import Integer, Column, String, Float
from sqlalchemy.orm import relation
from app import app
from app.model.meter import Meter


__author__ = 'windschord.com'

class Station(app.db_base):
    __tablename__ = 'station'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    latitude = Column(Float, unique=True)
    longitude = Column(Float, unique=True)
    meter_data = relation(Meter, order_by=Meter.id, lazy='dynamic', backref='station')

    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return '<Station %r [%r]>' % (self.name, self.id)

    def __iter__(self):
        for k, v in self.__dict__.items():
            yield k, v