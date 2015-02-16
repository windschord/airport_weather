# -*- coding:utf-8 -*-
from datetime import datetime
from flask import render_template, request
from sqlalchemy import create_engine, func
from sqlalchemy.orm import scoped_session, sessionmaker

from app import app
from app.lib.acquire_meter import AcquireMeter
from app.lib.acquire_taf import AcquireTaf
from app.model.meter import Meter
from app.model.station import Station


@app.before_first_request
def setup():
    engine = create_engine('sqlite:///app.db')
    app.db_base.metadata.create_all(engine)
    Session = scoped_session(sessionmaker(autocommit=False,
                                          autoflush=False,
                                          bind=engine))
    app.db_session = Session()


@app.route('/setup')
def setup():
    app.db_session.rollback()
    app.db_session.add(Station('RJCC', 1.1, 2.2))
    app.db_session.add(Station('RJTT', 1.1, 2.2))

    app.db_session.commit()
    return 'Hello World!'


@app.route('/', methods=['GET', 'POST'])
def index():
    latest_meter = []
    last_12h_meter = []
    if request.method == 'POST':
        station_name = request.form['airport_name'].upper()
        # 最新Meter
        station = app.db_session.query(Station).filter(Station.name == station_name).first()
        latest_meter = app.db_session.query(Meter).filter(
            Meter.time == app.db_session.query(func.max(Meter.time))).filter(
            Meter.station_id == station.id).first()
        latest_meter.station_id = station.name
        app.logger.debug(latest_meter)

        # fixme this code is not true....
        # 直近12時間
        last_12h_meter = app.db_session.query(Meter).filter(
            Meter.time < datetime.utcnow()).filter(
            Meter.station_id == station.id).all()
        for n in last_12h_meter:
            n.station_id = station.name
        app.logger.debug(last_12h_meter)
        
    else:
        pass
    return render_template("index.html", latest=latest_meter, data=last_12h_meter)


@app.route('/get/meter')
def get_meter():
    s = app.db_session.query(Station).first()
    res = AcquireMeter().execute(s, 3)
    app.logger.debug(res)
    app.db_session.add_all(res)
    app.db_session.commit()
    return 'OK!'

@app.route('/get/taf')
def get_taf():
    s = app.db_session.query(Station).first()
    res = AcquireTaf().execute(s, 1)
    app.logger.debug(res)
    app.db_session.add_all(res)
    app.db_session.commit()
    return 'OK!'

if __name__ == '__main__':
    app.run(debug=True)
