import os
import logging.config

from flask import Flask
from jinja2 import ChoiceLoader, FileSystemLoader

from .app import JSONEncoder
from .config import Config
from .db import db
from .exception import UnknownException, APIException, HTTPException
from .redis import redis_client
from .celery import celery
from .task import mail
from .extension import cors, migrate
from .logger import logging_conf


class Haw():
    def __init__(self, app: Flask = None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        """ 初始化 """
        # 修改json encoder
        self._enable_json_encoder(app)
        # 设置默认配置
        self._set_default_config(app)
        # 内置三方扩展注册
        self._register_extensions(app)
        # 添加jinja2模板寻找位置
        self._add_template_path(app)
        # 使用内置统一错误处理
        self._handle_error(app)
        self._register_logger(app)
        # TODO 挂载内部方法（视图）、用户日志处理

    def _enable_json_encoder(self, app: Flask):
        """ 替换 flask 内部 JSONEncoder

        支持格式化特定对象（实现 key 和 __getitem__ 方法的类），时间等
        """
        app.json_encoder = JSONEncoder

    def _set_default_config(self, app: Flask):
        """ 默认配置 """
        for item in vars(Config):
            if item.isupper():
                # 如果没有设置则会使用内部默认值
                app.config.setdefault(item, getattr(Config, item))

    def _register_extensions(self, app):
        """ 注册三方扩展 """
        self._check_in_config(app, 'SQLALCHEMY_DATABASE_URI')
        db.init_app(app)
        redis_client.init_app(app)
        celery.init_app(app)
        mail.init_app(app)
        migrate.init_app(app, db)
        cors.init_app(app)

    def _check_in_config(self, app: Flask, name: str):
        """ 检查配置中是否设置某项配置

        用于强制性配置项
        """
        try:
            app.config[name]
        except KeyError:
            raise Exception(f'{name} 没有设置')

    def _add_template_path(self, app):
        """ 添加当前 templates 文件夹到 jinja2 的寻找路径 """
        base_dir = os.path.abspath(os.path.dirname(__file__))
        loader = ChoiceLoader([
            app.jinja_loader,
            FileSystemLoader(os.path.join(base_dir, 'templates'))
        ])
        app.jinja_loader = loader

    def _handle_error(self, app):
        """ 处理错误 """
        @app.errorhandler(Exception)
        def handler(e):
            if isinstance(e, APIException):
                return e
            if isinstance(e, HTTPException):
                code = e.code
                msg = e.description
                error_code = 20000
                return APIException(code, error_code, msg)
            else:
                if not app.config['DEBUG']:
                    import traceback
                    app.logger.error(traceback.format_exc())
                    return UnknownException()
                else:
                    raise e

    def _register_logger(self, app):
        logging.config.dictConfig(logging_conf(app))
