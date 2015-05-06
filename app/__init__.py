# -*- coding:utf-8 -*-
from flask import Flask
from flask.ext.babel import Babel

from app.view import show_weather, get_data_from_web, manage_stations


__author__ = 'windschord.com'

app = Flask(__name__)
app.config.from_object('app_conf')
babel = Babel(app)

app.register_blueprint(show_weather.blueprint)
app.register_blueprint(get_data_from_web.blueprint)
app.register_blueprint(manage_stations.blueprint)

