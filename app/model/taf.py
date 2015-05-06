# -*- coding:utf-8 -*-
from sqlalchemy import Column, Float, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relation

from app.model import DB_BASE
from app.model.taf_forecast import TafForecast


__author__ = 'windschord.com'


class Taf(DB_BASE):
    __tablename__ = 'taf'
    __table_args__ = (UniqueConstraint('station_id', 'issue_time', name='taf_pk1'),)

    id = Column(Integer, primary_key=True)
    station_id = Column(Integer, ForeignKey('station.id'))
    issue_time = Column(DateTime())
    bulletin_time = Column(DateTime())
    valid_time_from = Column(DateTime())
    valid_time_to = Column(DateTime())
    elevation_m = Column(Float)
    forecast = relation(TafForecast, order_by=TafForecast.id, backref='taf')

    def __init__(self, station_id, issue_time, bulletin_time, valid_time_from, valid_time_to,
                 forecast):
        self.station_id = station_id
        self.issue_time = issue_time
        self.bulletin_time = bulletin_time
        self.valid_time_from = valid_time_from
        self.valid_time_to = valid_time_to
        self.forecast = forecast


    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

    def __iter__(self):
        for k, v in self.__dict__.items():
            yield k, v