""" 鉴权模块，配合manage模块使用 """
from functools import wraps

from flask import request
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_current_user, \
    create_access_token, create_refresh_token, decode_token

from .exception import AuthFailed, InvalidTokenException, ExpiredTokenException, NotFound

jwt = JWTManager()


@jwt.user_loader_callback_loader
def user_loader(identity):
    """ 用户加载 """
    if 'remote_addr' in identity.keys(
    ) and identity['remote_addr'] != request.remote_addr:
        raise AuthFailed()
    from .manager import find_user
    user = find_user(id=identity['uid'])
    if user is None:
        raise NotFound(msg='用户不存在')
    return user


@jwt.expired_token_loader
def expired_loader():
    return ExpiredTokenException()


@jwt.invalid_token_loader
def invalid_loader(e):
    return InvalidTokenException()


@jwt.unauthorized_loader
def unauthorized_loader(e):
    return AuthFailed(msg='请重新登录')


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    """ 添加token 内容"""
    return {
        'uid':
        identity['uid'],
        'remote_addr':
        identity['remote_addr'] if 'remote_addr' in identity.keys() else None
    }


def get_tokens(user, verify_remote_addr=False):
    identify = {'uid': user.id}
    if verify_remote_addr:
        identify['remote_addr'] = request.remote_addr
    access_token = create_access_token(identity=identify)
    refresh_token = create_refresh_token(identity=identify)
    return access_token, refresh_token


def get_access_token(user, expires_delta=None, verify_remote_addr=False):
    identity = {}
    identity['uid'] = user.id
    if verify_remote_addr:
        identity['remote_addr'] = request.remote_addr
    access_token = create_access_token(
        identity=identity,
        expires_delta=expires_delta,
    )
    return access_token


def get_refresh_token(user, expires_delta=None, verify_remote_addr=False):
    identity = {}
    identity['uid'] = user.id
    if verify_remote_addr:
        identity['remote_addr'] = request.remote_addr
    refresh_token = create_refresh_token(identity=identity,
                                         expires_delta=expires_delta)
    return refresh_token


def _check_is_active(current_user):
    if not current_user.is_valid:
        raise AuthFailed(msg='您目前处于未激活状态，请先激活')


def user_logined():
    """ 当前是否有用户登录(对登录和未登录用户显示不同内容时使用)
    已登录返回用户信息,未登录返回None """
    auth = request.headers.get('Authorization', '')
    if auth:
        auth = auth.split('Bearer ')
        if len(auth) > 1:
            token = decode_token(auth[1])
            user = user_loader(token['identity'])
            return user
    return None


def admin_required(fn):
    """ 超级管理员 """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user = get_current_user()
        if not current_user.is_admin:
            raise AuthFailed(msg='没有权限')
        return fn(*args, **kwargs)

    return wrapper


def group_required(fn):
    """ 分组权限 """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user = get_current_user()
        _check_is_active(current_user)
        if not current_user.is_admin:
            group_id = current_user.group_id
            if group_id is None:
                raise AuthFailed(msg='没有分配所属分组')
            from .manager import is_user_allowed
            it = is_user_allowed(group_id)
            if not it:
                raise AuthFailed(msg='权限不够，不能访问')
        return fn(*args, **kwargs)

    return wrapper


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        _check_is_active(current_user=get_current_user())
        return fn(*args, **kwargs)

    return wrapper
