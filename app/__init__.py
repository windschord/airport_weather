# -*- coding:utf-8 -*-
from flask import Flask
from flask.ext.babel import Babel

from app.view import show_weather, get_data_from_web, manage_stations, system_preferences


__author__ = 'windschord.com'

app = Flask(__name__)
app.config.from_object('app_conf')
babel = Babel(app)

app.register_blueprint(show_weather.blueprint)
app.register_blueprint(get_data_from_web.blueprint)
app.register_blueprint(manage_stations.blueprint)
app.register_blueprint(system_preferences.blueprint)


