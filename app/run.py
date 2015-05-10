# -*- coding:utf-8 -*-
from flask import request, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app import app, babel
from app.model import DB_BASE
from app.view.system_preferences import load_db


__author__ = 'windschord.com'


@babel.localeselector
def get_locale():
    # この場合はブラウザのAccept Languagesを見るようになっている。
    return request.accept_languages.best_match(['ja', 'ja_JP', 'en'])


@app.before_first_request
def setup():
    app.db_engine = create_engine('sqlite:///app.db')
    DB_BASE.metadata.create_all(app.db_engine)

    Session = scoped_session(sessionmaker(autocommit=False,
                                          autoflush=False,
                                          bind=app.db_engine))
    app.db_session = Session()
    app.db_session.rollback()
    load_db()

    # デバッグ時のみルートを表示する。
    if app.config['DEBUG']:
        list_routes()


@app.before_request
def before_request():
    Session = scoped_session(sessionmaker(autocommit=False,
                                          autoflush=False,
                                          bind=app.db_engine))
    app.db_session = Session()
    app.db_session.rollback()


@app.teardown_request
def teardown_request(exception):
    app.db_session.close()


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")


def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    app.logger.debug('\n'.join(sorted(output)))

if __name__ == '__main__':
    app.run()