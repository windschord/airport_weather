# -*- coding:utf-8 -*-
from flask import Flask
from sqlalchemy.ext.declarative import declarative_base

__author__ = 'windschord.com'

app = Flask(__name__)
app.db_base = declarative_base()