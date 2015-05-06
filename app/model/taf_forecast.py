# -*- coding:utf-8 -*-
from sqlalchemy import Column, Float, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relation

from app.model import DB_BASE

from app.model.taf_sky_condition import TafSkyCondition


__author__ = 'windschord.com'


class TafForecast(DB_BASE):
    __tablename__ = 'taf_forecast'

    id = Column(Integer, primary_key=True)
    taf_id = Column(Integer, ForeignKey('taf.id'))
    fcst_time_from = Column(DateTime())
    fcst_time_to = Column(DateTime())
    change_indicator = Column(String(10))
    wind_dir = Column(Integer)
    wind_speed = Column(Integer)
    visibility = Column(Float)
    sky_condition = relation(TafSkyCondition, order_by=TafSkyCondition.id, backref='taf_forecast')
    flight_category = Column(String(10))
    elevation_m = Column(Float)

    def __init__(self, fcst_time_from, fcst_time_to, change_indicator, wind_dir,
                 wind_speed, visibility, sky_condition,
                 flight_category, elevation_m):
        self.fcst_time_from = fcst_time_from
        self.fcst_time_to = fcst_time_to
        self.change_indicator = change_indicator
        self.wind_dir = wind_dir
        self.wind_speed = wind_speed
        self.visibility = visibility
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