# -*- coding:utf-8 -*-

from flask import current_app, Blueprint, render_template, request, url_for, redirect, g
from flask.ext.babel import gettext as _
from app.model.airportinfo import AirportInfo

from app.model.system_settings import SystemSetting


__author__ = 'windschord.com'

blueprint = Blueprint('SystemSetting', __name__, url_prefix='/SystemSetting/')


@blueprint.route('setup')
def setup():
    try:
        current_app.db_session.add(AirportInfo('RJCC', 1, 2, True))
        current_app.db_session.add(AirportInfo('RJTT', 2, 3, True))
        current_app.db_session.add(AirportInfo('RJAA', 2, 3, True))

        current_app.db_session.commit()
        return _('Setup is Success!!')
    except Exception as e:
        current_app.logger.exception('Setup is Fail!!\n')
        return _('Setup is Fail!!')


@blueprint.route('index', methods=['GET', 'POST'])
def index():
    title = 'SystemSetting'

    if request.method == 'GET':
        search_settings = None
    elif request.method == 'POST':
        settings, search_settings = crud()
    else:
        return 'Error....404'

    settings = current_app.db_session.query(SystemSetting).all()
    return render_template("system_setting_index.html", title=title, settings=settings, search_settings=search_settings)

@blueprint.route('load_db', methods=['GET'])
def load_db():
    current_app.REQUEST_HOURS = current_app.db_session.query(SystemSetting).filter(SystemSetting.key == 'REQUEST_HOURS').first().value
    current_app.logger.debug(current_app.REQUEST_HOURS)
    return 'OK'

def crud():
    current_app.logger.debug(request.form)
    req_id = request.form['id']
    req_type = request.form.get('type', None)
    key = request.form.get('key', None)
    value = request.form.get('value', None)

    all_settings = current_app.db_session.query(SystemSetting).all()
    target = current_app.db_session.query(SystemSetting).filter(SystemSetting.id == req_id).first()

    current_app.logger.debug(target)
    if req_type == 'add':
        target = SystemSetting(key, value)
        current_app.db_session.add(target)
        current_app.db_session.commit()
        current_app.logger.debug('ADD: %s' % target)
    elif req_type == 'update':
        target.value = value
        current_app.db_session.commit()
        current_app.logger.debug('UPDATE: %s' % target)
    elif req_type == 'delete':
        target = current_app.db_session.query(SystemSetting).filter(
        SystemSetting.id == req_id).first()
        current_app.db_session.delete(target)
        current_app.db_session.commit()
        current_app.logger.debug('UPDATE: %s' % target)
        target = None
    else:
        current_app.logger.exception('Unknown type: %s' % target)

    return all_settings, target