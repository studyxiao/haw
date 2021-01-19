from datetime import date, datetime

from flask.json import JSONEncoder as _JSONEncoder


class JSONEncoder(_JSONEncoder):
    def default(self, obj):
        if (hasattr(obj, 'keys')) and hasattr(obj, '__getitem__'):
            return dict(obj)
        if isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        return super().default(obj)
