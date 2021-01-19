from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column
from sqlalchemy import Integer, DateTime, String, SmallInteger, Boolean

from .db import db, JSONMixin, CRUDMixin
from .utils import get_full_url, load_token
from .exception import NotFound, AuthFailed


class BaseModel(db.Model, JSONMixin, CRUDMixin):
    __abstract__ = True
    create_time = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    update_time = Column(DateTime,
                         default=datetime.utcnow,
                         onupdate=datetime.utcnow,
                         comment='修改时间')
    delete_time = Column(DateTime, comment='删除时间，软删除时赋值，表示删除')

    def _set_fields(self):
        if 'delete_time' not in self._exclude:
            self._exclude.append('delete_time')


class User(BaseModel):
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False, comment='邮箱')
    mobile = Column(String(20), comment='手机号')
    name = Column(String(24), unique=True, nullable=False, comment='用户名')
    _password = Column('password', String(100), comment='密码')
    _avatar = Column('avatar', String(255), comment='头像')
    _background = Column('background', String(255), comment='主页背景图')
    sign = Column(String(255), comment='简介')
    birthday = Column(DateTime, default=datetime.utcnow, comment='出生日期')
    gender = Column(SmallInteger, default=0, comment='性别，0-保密，1-女，2-男')
    location = Column(String(255), comment='住址')
    is_valid = Column(Boolean, default=False, comment='当前用户是否为激活状态')
    group_id = Column(Integer,
                      default=2,
                      comment='用户所属权限组id, 0-超级管理员，1-管理员，2-普通用户')
    is_vip = Column(Integer, default=0, comment='是否为VIP, 0-普通1-7等级')
    status = Column(SmallInteger, default=0, comment='当前用户状态，0-正常，1-禁言，2-拉黑')
    open_id = Column(String(200), comment='微信openid')

    def _set_fields(self):
        self._exclude = [
            'password', 'status', 'group_id', 'is_valid', 'is_admin'
        ]
        super()._set_fields()

    @property
    def is_admin(self):
        """ 0为超级管理员 """
        return self.group_id == 0

    @property
    def password(self):
        return ''

    @password.setter
    def password(self, pwd):
        self._password = generate_password_hash(pwd)

    @property
    def avatar(self):
        """ 获得完整路径，BUG:仅host带有 api/ 后缀时才起作用 """
        url = get_full_url(self._avatar)
        return url

    @avatar.setter
    def avatar(self, data):
        self._avatar = data

    @property
    def background(self):
        """ 获得完整路径，BUG:仅host带有 api/ 后缀时才起作用 """
        url = get_full_url(self._background)
        return url

    @background.setter
    def background(self, data):
        self._background = data

    def set_group(self, group_id):
        """ 设置 group id """
        with db.auto_commit():
            self.group_id = group_id

    def set_avatar(self, data):
        """ 设置头像 """
        with db.auto_commit():
            self.avatar = data

    def set_bg(self, data):
        """ 设置背景 """
        with db.auto_commit():
            self.background = data

    def check_password(self, pwd):
        """ 验证密码 """
        if not self._password:
            return False
        return check_password_hash(self._password, pwd)

    def change_password(self, old_password, new_password):
        """ 修改密码（知道密码） """
        if self.check_password(old_password):
            self.password = new_password
            return True
        return False

    def reset_password(self, pwd):
        """ 重置密码（忘记密码） """
        with db.auto_commit():
            self.password = pwd

    @classmethod
    def confirm(cls, token):
        """ 邮箱激活 """
        data = load_token(token)
        if data:
            one = cls.query.get(data.get('id'))
            if one:
                one.update(one.id, is_valid=True)
                return True
        return False

    @classmethod
    def create(cls, **kwargs):
        """ 没有指定name时，取email为name """
        if 'name' not in kwargs.keys():
            kwargs['name'] = kwargs['email']
        return super().create(**kwargs)

    @classmethod
    def update(cls, id, *condition, **kwargs):
        """ 禁止更新email """
        if 'email' in kwargs.keys():
            kwargs.pop('email')
        super().update(id, *condition, **kwargs)

    @classmethod
    def verify(cls, name, password):
        """ 用户登录，重写此方法，覆盖默认登录验证

        使用邮箱密码方式登录
        """
        user = cls.query.filter_by(email=name).first()
        if user is None or not user.check_password(password):
            raise NotFound(msg='用户名或密码错误')
        if not user.is_valid:
            raise AuthFailed(msg='还未激活，请激活后登录')
        return user


class Auth(BaseModel):
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, nullable=False, comment='所属权限组id')
    auth = Column(String(60), comment='权限字段')
    module = Column(String(50), comment='权限所属模块')


class Group(BaseModel):
    id = Column(Integer, primary_key=True)
    name = Column(String(60), comment='权限组名称')
    info = Column(String(255), comment='权限组描述')


class File(BaseModel):
    id = Column(Integer, primary_key=True)
    path = Column(String(500), nullable=False, comment='路径')
    type = Column('type', SmallInteger, default=1, comment='1 local，其他表示其他地方')
    name = Column(String(100), nullable=False, comment='名称')
    extension = Column(String(50), nullable=False, comment='后缀')
    size = Column(Integer, comment='大小')
    md5 = Column(String(40), unique=True, comment='md5值，防止上传重复图片')
