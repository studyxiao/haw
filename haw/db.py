""" 数据库操作 """
from contextlib import contextmanager
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import orm, inspect

from .exception import NotFound


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        """ 数据自动提交 """
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        kwargs['delete_time'] = None  # 只返回未删除数据
        return super().filter_by(**kwargs)

    def get_or_404(self, ident, description=None):
        rv = self.get(ident)
        if not rv:
            raise NotFound()
        return rv

    def first_or_404(self):
        rv = self.first()
        if not rv:
            raise NotFound()
        return rv


db = SQLAlchemy(query_class=Query)


class JSONMixin:
    """ model 可 json 化 """
    @orm.reconstructor
    def init_on_load(self):
        self._fields = []  # 可 json 字段
        self._exclude = []  # 不可 json 字段

        self._set_fields()  # 设置 排除项
        self.__clean_fields()  # 整理 fields

    def _set_fields(self):
        """ 可以设置 _fields 或 _exclude。
            通过子类重写函数实现，
            设置 _fields 后，会覆盖自定义 _fields
        """
        pass

    def _columns(self):
        """ 不包含_开头的所有数据字段(Column)名称

        返回 set
        """
        columns = inspect(self.__class__).columns
        all_columns = set([
            column.name for column in columns
            if not column.name.startswith('_')
        ])
        return all_columns

    def _property_fields(self):
        """ 不包含_开头的所有 property 属性

        返回 set
        """
        property_fields = set()
        fields = vars(self.__class__)
        for name, value in fields.items():
            if name.startswith('_'):
                continue
            if isinstance(value, property):
                property_fields.add(name)
        return property_fields

    def __clean_fields(self):
        """
        整理 _fields
            如果设置了 _fields 则不会覆盖；
            获得所有字段和property属性，排除固定字段/属性；
                如：以`_`开头的字段（包括`__`），
                      PS: 如只需屏蔽 `_` 可使用re.match(r'^_[^_], name)
        """
        if self._fields:
            return
        columns = self._columns() | self._property_fields()
        self._fields = list(columns - set(self._exclude))

    def keys(self):
        return self._fields

    def __getitem__(self, key):
        return getattr(self, key)

    def hide_fields(self, *args):
        """ 隐藏某字段 """
        for key in args:
            self._fields.remove(key)
        return self

    def add_fields(self, **kwargs):
        """ 添加自定义字段 """
        for name, value in kwargs.items():
            setattr(self, name, value)
            if name not in self._fields:
                self._fields.append(name)
        return self


class CRUDMixin:
    """ 增改删查 """
    def _set_attrs(self, **attrs_dict):
        """ 添加属性，不包括主键 """
        columns = get_columns(self.__class__)
        for key, value in attrs_dict.items():
            if key not in columns:
                continue
            if hasattr(self, key) and key not in self.__get_primary_key():
                setattr(self, key, value)

    @classmethod
    def create(cls, **data):
        """
            新增数据
            params: e.g. **{'title': 'ccc', 'content': 'hello'}
            return: 新创建对象
        """
        one = cls()
        with db.auto_commit():
            one._set_attrs(**data)
            db.session.add(one)
        return one

    @classmethod
    def update(cls, id, *condition, **data):
        """ 根据 id 以及其他可选条件更新一个数据
            id: 主键ID
            condition: e.g. Article.user_id==1, 是否属于用户
            data: title=ti
        """
        # query = cls.query
        query = db.session.query(cls)
        if condition:
            query = cls.query.filter(*condition)
        one = query.filter_by(id=id).first()
        if one is None:
            raise NotFound(msg='更新失败，数据不存在')
        one._update(data)
        return one

    @classmethod
    def delete(cls, id, hard=False, *condition):
        """ 删除某条数据（id及可选条件）
        condition: e.g. Article.user_id==1 """
        # query = cls.query
        query = db.session.query(cls)
        if condition:
            query = cls.query.filter(*condition)
        one = query.filter_by(id=id).first()
        if one is None:
            raise NotFound(msg='数据不存在，删除失败')
        if hard:
            result = one._hard_delete()
        else:
            result = one._delete()
        return result

    @classmethod
    def get(cls, *query, **kwargs):
        """
            根据条件获取一个
            query: 查询条件，e.g. Article.publish==1
            kwargs: 查询条件，e.g. title='tit'
        """
        # _query = cls.query
        _query = db.session.query(cls)
        if query:
            _query = _query.filter(*query)
        if kwargs:
            _query = _query.filter_by(**kwargs)
        return _query.first()

    @classmethod
    def find(cls, query=None, by=None, **kwargs):
        """
            根据条件查找所有
            query: ['Article.status==1']
            by: [Article.sort.desc]
            kwargs: title=1
        """
        # _query = cls.query
        _query = db.session.query(cls)
        if query:
            _query = _query.filter(*query)
        if by:
            _query = _query.order_by(*by)
        return _query.filter_by(**kwargs).all()

    @classmethod
    def find_by_page(cls, query, by, start, count, _query=None, fields=None):
        """
            分页，筛选，排序
            query: 查询条件，[Article.status==1]
            by: 排序，[Article.created]
            start: 起始位置
            count: 个数
            _query: 查询集 cls.query.filter()，设置后会在此基础上进行查询
            fields: 返回前端字段，['id', 'title', 'content']，默认model._fields
        """
        if _query is None:
            # _query = cls.query
            _query = db.session.query(cls)
        if query:
            _query = _query.filter(*query)
        if by:
            _query = _query.order_by(*by)
        result = _query.filter_by()
        num = result.count()
        data = result.slice(start, start + count).all()
        if fields is not None:
            for item in data:
                item._fields = fields
        return {'num': num, 'data': data}

    def _update(self, data):
        """ 修改 """
        with db.auto_commit():
            self._set_attrs(**data)
            db.session.add(self)
        return self

    def _delete(self):
        """ 软删除 """
        with db.auto_commit():
            self.delete_time = datetime.now()
            db.session.add(self)
        return True

    def _hard_delete(self):
        """ 硬删除 """
        with db.auto_commit():
            db.session.delete(self)
        return True

    @classmethod
    def __get_primary_key(cls):
        """ 获得model的主键，返回list """
        primary_keys = [item.name for item in inspect(cls).primary_key]
        return primary_keys


def get_columns(_cls):
    """ 不包含_开头的所有数据字段(Column)名称

        返回 set
    """
    columns = inspect(_cls).columns
    all_columns = set(
        [column.name for column in columns if not column.name.startswith('_')])
    return all_columns
