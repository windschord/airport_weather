# -*- coding:utf-8 -*-
from flask import render_template, request
from sqlalchemy import create_engine, func
from sqlalchemy.orm import scoped_session, sessionmaker

from app import app
from app.lib.acquire_meter import GetMeter
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
    app.db_session.add(Station('RJCC', 1.1, 2.2))
    app.db_session.add(Station('RJTT', 1.1, 2.2))

    app.db_session.commit()
    return 'Hello World!'


@app.route('/', methods=['GET', 'POST'])
def index():
    new_meter = []
    if request.method == 'POST':
        station_name = request.form['airport_name'].upper()
        station = app.db_session.query(Station).filter(Station.name == station_name).first()
        new_meter = app.db_session.query(Meter).filter(
            Meter.time == app.db_session.query(func.max(Meter.time))).filter(
            Meter.station_id == station.id).all()
        app.logger.debug(new_meter)
    else:
        pass
    return render_template("index.html", data=new_meter)


@app.route('/get')
def get():
    s = app.db_session.query(Station).all()[0]
    res = GetMeter().execute(s, 3)
    app.logger.debug(res)
    app.db_session.add_all(res)
    app.db_session.commit()
    return 'OK!'


if __name__ == '__main__':
    app.run(debug=True)