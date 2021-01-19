from flask import Flask

from haw.core import Haw
from haw.manager import Manager

from .config import Config

app = Flask(__name__)
app.config.from_object(Config)

haw = Haw()
haw.init_app(app)

manager = Manager(app)


@app.route('/')
def home():
    app.logger.info('123')
    return 'hello'
