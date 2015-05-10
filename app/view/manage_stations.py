# -*- coding:utf-8 -*-
import traceback

from flask import current_app, Blueprint, request, flash, render_template
from flask.ext.babel import gettext as _

from app.model.airportinfo import AirportInfo


__author__ = 'windschord.com'

blueprint = Blueprint('stations', __name__, url_prefix='/station/')


@blueprint.route('add')
def add_station():
    pass


@blueprint.route('manage', methods=['GET', 'POST'])
def manage():
    title = _('All airports')
    search_res = None

    mode = request.args.get('mode', '')

    if request.method == 'POST' and mode == 'search':
        station_name = request.form['airport_name'].upper()
        search_res = current_app.db_session.query(AirportInfo).filter(
            AirportInfo.icao_code == station_name).group_by(
            AirportInfo.id).first()
    elif request.method == 'POST' and mode == 'edit':
        req_id = request.form['id']
        crud_type = request.form['type']
        icao_code = request.form['icao_code'].upper()
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])
        enable = (request.form['enable'] == 'TRUE')
        country = trim_str_to_none(request.form['country'])
        city = trim_str_to_none(request.form['city'])
        current_app.logger.debug('Forms: %s' % request.form)

        try:
            if crud_type == 'add':
                target = AirportInfo(icao_code, latitude, longitude,
                                     enable, country, city)
                current_app.db_session.add(target)
                current_app.db_session.commit()
                current_app.logger.debug('ADD: %s' % target)

            elif crud_type == 'delete':
                target = current_app.db_session.query(AirportInfo).filter(
                    AirportInfo.id == req_id).first()
                current_app.db_session.delete(target)
                current_app.db_session.commit()
                current_app.logger.debug('UPDATE: %s' % target)

            elif crud_type == 'update':
                target = current_app.db_session.query(AirportInfo).filter(
                    AirportInfo.id == req_id).first()
                target.icao_code = icao_code
                target.country = country
                target.city = city
                target.latitude = latitude
                target.longitude = longitude
                target.enable = enable
                current_app.db_session.commit()
                current_app.logger.debug('UPDATE: %s' % target)

            else:
                current_app.logger.warning('Unknown CRUD type.: %s' % crud_type)
                flash(_('Unknown CRUD type.'))

        except Exception:
            current_app.logger.debug('Not correct Data: %s \n%s' % (request.form, traceback.format_exc()))
            current_app.db_session.rollback()
            search_res = target
            flash(_('Input data is not Correct'))

    res = current_app.db_session.query(AirportInfo).order_by(
        AirportInfo.icao_code.asc()).all()
    current_app.logger.debug(' search_res: %s \n res: %s' % (search_res, res))

    if res is None:
        flash(_('Not exist airport code.'))

    return render_template("stations.html", title=title, search_res=search_res, form_data=request.form,
                           stations=res)


def trim_str_to_none(str):
    if len(str) > 0:
        return str
    else:
        return None