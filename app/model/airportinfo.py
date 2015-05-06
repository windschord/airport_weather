# -*- coding:utf-8 -*-

from sqlalchemy import Integer, Column, String, Float, Boolean
from sqlalchemy.orm import relation
from app.model import DB_BASE

from app.model.meter import Meter
from app.model.taf import Taf


__author__ = 'windschord.com'


class AirportInfo(DB_BASE):
    __tablename__ = 'station'
    id = Column(Integer, primary_key=True)
    icao_code = Column(String, unique=True)
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    enable = Column(Boolean, nullable=False)
    meter_data = relation(Meter, order_by=Meter.id, lazy='dynamic', backref='station')
    taf_data = relation(Taf, order_by=Taf.id, lazy='dynamic', backref='station')

    def __init__(self, icao_code, latitude, longitude, enable, country=None, city=None):
        self.icao_code = icao_code
        self.latitude = latitude
        self.longitude = longitude
        self.enable = enable
        self.country = country
        self.city = city

    def __repr__(self):
        return '<AirportInfo %r [%r] [%s]>' % (self.icao_code, self.id, self.enable)

    def __iter__(self):
        for k, v in self.__dict__.items():
            yield k, v