# -*- coding:utf-8 -*-
from sqlalchemy import Integer, Column, String, ForeignKey, Float, DateTime, UniqueConstraint
from sqlalchemy.orm import relation
from app import app
from app.model.meter_sky_condition import MeterSkyCondition

__author__ = 'windschord.com'


class Meter(app.db_base):
    __tablename__ = 'meter'
    __table_args__ = (UniqueConstraint('station_id', 'time', name='meter_pk1'),)

    id = Column(Integer, primary_key=True)
    station_id = Column(Integer, ForeignKey('station.id'))
    time = Column(DateTime())
    air_temp = Column(Float)
    dewpoint = Column(Integer)
    wind_dir = Column(Integer)
    wind_speed = Column(Integer)
    visibility = Column(Float)
    altimeter = Column(Float)
    sea_level_press = Column(Float)
    wx_string = Column(String(20))
    sky_condition = relation(MeterSkyCondition, order_by=MeterSkyCondition.id, backref='meter')
    flight_category = Column(String(10))
    elevation_m = Column(Float)

    def __init__(self, station_id, time, air_temp, dewpoint, wind_dir,
                 wind_speed, visibility, altimeter, sky_condition,
                 flight_category, elevation_m, sea_level_press=None,):
        self.station_id = station_id
        self.time = time
        self.air_temp = air_temp
        self.dewpoint = dewpoint
        self.wind_dir = wind_dir
        self.wind_speed = wind_speed
        self.visibility = visibility
        self.altimeter = altimeter
        self.sea_level_press = sea_level_press
        self.sky_condition = sky_condition
        self.flight_category = flight_category
        self.elevation_m = elevation_m

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

    def __iter__(self):
        for k, v in self.__dict__.items():
            yield k, v