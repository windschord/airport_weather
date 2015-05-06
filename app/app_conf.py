# -*- coding:utf-8 -*-
from datetime import timedelta
__author__ = 'windschord.com'

### app settings ###
DEBUG = True
#SERVER_NAME = 'localhost'
REQUEST_HOURS = 3
WEATHER_UPDATE_INTERVAL = 30 # (min)
SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

### Celery settings ###
# CELERY_BROKER_URL = 'amqp://'
# CELERY_RESULT_BACKEND = 'amqp://'
# CELERYBEAT_SCHEDULE = {
#     'add-every-30-seconds': {
#         'task': 'tasks.add',
#         'schedule': timedelta(seconds=30),
#         'args': (16, 16)
#     },
# }
#
# CELERY_TIMEZONE = 'UTC'
# CELERY_IMPORTS = ("app.tasks")