# -*- coding:utf-8 -*-
from sqlalchemy import Column, Integer, String

from app.model import DB_BASE


__author__ = 'windschord.com'


class SystemSetting(DB_BASE):
    __tablename__ = 'system_setting'

    id = Column(Integer, primary_key=True)
    key = Column(String(32), nullable=False, unique=True)
    value = Column(String(256))

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

    def __iter__(self):
        for k, v in self.__dict__.items():
            yield k, v
