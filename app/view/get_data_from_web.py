# -*- coding:utf-8 -*-
from flask import Blueprint, flash, url_for, redirect
from app.lib.get_web_weather import GetWebWeather
from flask.ext.babel import gettext as _

__author__ = 'windschord.com'

blueprint = Blueprint('get', __name__, url_prefix='/get/')

@blueprint.route('meter')
def get_meter():
    GetWebWeather().execute()
    flash(_('weather data updated'))
    return redirect(url_for('show.index'))