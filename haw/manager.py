""" 权限管理 """
from collections import namedtuple

from flask import Flask, current_app, request
from werkzeug.local import LocalProxy

from .model import User, Auth, Group
from .auth import jwt

# 元信息，相当于：
# class Meta:
#     auth = ''
Meta = namedtuple('Meta', ['auth'])

# 存储路由函数权限信息，e.g. {'indexagc': Meta(auth='首页')}
route_metas = {}


def route_meta(auth):
    """
    记录路由函数的权限信息的装饰器，
    在没有app实例时就运行了
    """
    def decorator(func):
        name = func.__name__ + str(func.__hash__())
        existed = route_metas.get(name)
        if existed:
            raise Exception('name 已经存在')
        else:
            route_metas.setdefault(name, Meta(auth))
        return func

    return decorator


class Manager:
    """ 用户及权限管理

    :params ep_metas: endpoint 与 route_meta 一对一关系，
    用于后期通过 endpoint 查找路由权限信息
    需要注册所有蓝图后才能初始化此插件
    """
    ep_metas = {}

    def __init__(self,
                 app: Flask = None,
                 user_model=None,
                 group_model=None,
                 auth_model=None):
        if app is not None:
            self.init_app(app, user_model, group_model, auth_model)

    def init_app(self,
                 app,
                 user_model=None,
                 group_model=None,
                 auth_model=None):
        self.user_model = user_model or User
        self.auth_model = auth_model or Auth
        self.group_model = group_model or Group
        app.extensions['manager'] = self
        # 把 endpoint 与 route_metas 结合,
        # 这也是为什么需要蓝图注册后才能使用此插件的原因
        for ep, func in app.view_functions.items():
            info = route_metas.get(func.__name__ + str(func.__hash__()), None)
            if info:
                self.ep_metas.setdefault(ep, info)
        # 注册jwt
        jwt.init_app(app)

    def find_user(self, **kwargs):
        return self.user_model.query.filter_by(**kwargs).first()

    def verify_user(self, name, password):
        return self.user_model.verify(name, password)

    def find_group(self, **kwargs):
        return self.group_model.query.filter_by(**kwargs).first()

    def verify_user_in_group(self, group_id, auth):
        return self.auth_model.query.filter_by(
            group_id=group_id,
            auth=auth,
        ).first()


manager = LocalProxy(lambda: get_manager())


def get_manager():
    _manager = current_app.extensions['manager']
    if _manager:
        return _manager
    app = current_app._get_current_object()
    with app.app_context():
        return app.extensions['manager']


def find_user(**kwargs):
    return manager.find_user(**kwargs)


def find_group(**kwargs):
    return manager.find_group(**kwargs)


def get_ep_infos():
    """ 权限信息，{auth: [ep1, ep2]} """
    infos = {}
    for ep, meta in manager.ep_metas.items():
        mod = infos.get(meta.auth, None)
        if mod:
            mod.append(ep)
        else:
            infos.setdefault(meta.auth, [ep])
    return infos


def find_info_by_ep(ep):
    return manager.ep_metas.get(ep)


def is_user_allowed(group_id):
    """ yoghurt是否有权限访问路由 """
    ep = request.endpoint
    meta = manager.ep_metas.get(ep)
    return manager.verify_user_in_group(group_id, meta.auth)


def find_auth_module(auth):
    """ 通过权限查找 meta 信息 """
    for _, meta in manager.ep_metas.items():
        if meta.auth == auth:
            return meta
    return None
