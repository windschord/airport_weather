# -*- coding:utf-8 -*-
from datetime import datetime, timedelta

from flask import render_template, request, flash, Blueprint, current_app
from flask.ext.babel import gettext as _

from app.lib.select_meter import SelectMeter
from app.lib.select_taf import SelectTaf
from app.model.airportinfo import AirportInfo


blueprint = Blueprint('show', __name__, url_prefix='/')


@blueprint.route('', methods=['GET', 'POST'])
def index():
    latest_meter = []
    latest_taf = []
    if request.method == 'POST':
        station_name = request.form['airport_name'].upper()
        station = current_app.db_session.query(AirportInfo).filter(AirportInfo.icao_code == station_name).group_by(
            AirportInfo.id).first()
        if station is None:
            flash(_('Not exist airport code.'))
        else:
            # 最新Meter
            latest_meter = SelectMeter(current_app.db_session).latest(station)
            current_app.logger.debug(latest_meter)
            latest_taf = SelectTaf().latest(station)
            current_app.logger.debug(latest_taf)

    return render_template("index.html", latest_meter=latest_meter, latest_taf=latest_taf)


@blueprint.route('search', methods=['GET', 'POST'])
def search():
    title = None
    res = []

    if request.method == 'POST':
        search_type = request.form['type']
        station_name = request.form['airport_name'].upper()
        station = current_app.db_session.query(AirportInfo).filter(
            AirportInfo.icao_code == station_name).group_by(
            AirportInfo.id).first()

        if station is None:
            flash(_('Not exist airport code.'))
        else:
            # 直近12時間Meter
            to_time = datetime.utcnow()
            from_time = to_time - timedelta(hours=12)

            if search_type == 'meter':
                res = SelectMeter(current_app.db_session).between(station, from_time, to_time)
                title = _('Meter') + ' [' + station_name + ']'
            elif search_type == 'taf':
                res = SelectTaf(current_app.db_session).last_12h(station)
                title = _('Taf') + ' [' + station_name + ']'
            else:
                flash(_('Request type unknown.'))

    current_app.logger.debug(res)
    return render_template("search.html", title=title, search_data=res)





