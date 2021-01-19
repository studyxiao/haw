from flask import current_app
from celery import Celery
from celery import Task as _Task


class Task(_Task):
    def __call__(self, *args, **kwargs):
        with current_app.app_context():
            return self.run(*args, **kwargs)


class FlaskCelery:
    def __init__(self, app=None):
        self._celery = Celery()
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self._celery.conf.update({
            'timezone': 'Asia/Shanghai',
            'enable_utc': True,
            'broker_url': app.config['CELERY_BROKER'],
            'result_backend': app.config['CELERY_BACKEND']
        })
        with app.app_context():
            self._celery.Task = Task

    def __getattr__(self, name):
        return getattr(self._celery, name)

    def __getitem__(self, name):
        return self._celery[name]

    def __setitem__(self, name, value):
        self._celery[name] = value

    def __delitem__(self, name):
        del self._celery[name]


celery = FlaskCelery()
