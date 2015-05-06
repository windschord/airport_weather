# -*- coding:utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey

from app.model import DB_BASE


__author__ = 'windschord.com'


class TafSkyCondition(DB_BASE):
    __tablename__ = 'taf_sky_condition'

    id = Column(Integer, primary_key=True)
    taf_id = Column(Integer, ForeignKey('taf_forecast.id'))
    sky_cover = Column(String(10))
    cloud_base_ft_agl = Column(String(10))

    def __init__(self, sky_cover, cloud_base_ft_agl):
        self.sky_cover = sky_cover
        self.cloud_base_ft_agl = cloud_base_ft_agl

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

    def __iter__(self):
        for k, v in self.__dict__.items():
            yield k, v
