from flask import request, current_app
from flask_sqlalchemy import Model
from sqlalchemy import inspect

from .utils import paginate


class RequestParser:
    """
        query_keys:  查询操作，对应的含义查看api接口文档
        by_keys:     排序操作，同上
        __can_query_fields__: list 允许查询字段，默认所有(None)
        __can_by_fields__: list 允许排序字段，默认所有(None)
        fields: 查询结果需要的model字段，默认为去掉`_`开头所有字段，包括property
        detail_fields:  获得单个时的返回字段，默认为fields
    """
    query_keys = set(['gt', 'ge', 'lt', 'le', 'ne', 'eq', 'ic', 'ni', 'in'])
    by_keys = set(['by'])
    __can_query_fields__ = None
    __can_by_fields__ = None

    def __init__(self, model: Model):
        self._model = model()

    @staticmethod
    def paginate():
        """
            获得分页数据(start, start+count)
            start: 起始位置，前端出入page参数后，根据page*count得到start
            count: 数据长度
        """
        start, count = paginate()
        return start, count

    def parse_query_fields(self):
        """ 解析请求中的查询和排序字段 """
        args = request.args
        query_fields = []
        by_fields = []
        for query_key, value in args.items():
            key_split = query_key.split('_', 1)
            if len(key_split) != 2:
                continue
            operator, key = key_split
            if key not in self._columns():
                # 模型中运行的字段没有该查询字段，跳过
                continue
            if not hasattr(self, f'_{operator}'):
                # 没有定义该操作
                continue
            if operator in self.query_keys:
                if self.__can_query_fields__ is not None and key not in self.__can_query_fields__:
                    # 不允许查询字段
                    continue
                query_fields.append(getattr(self, f'_{operator}')(key, value))
            if operator in self.by_keys:
                if self.__can_by_fields__ is not None and key not in self.__can_by_fields__:
                    # 不允许查询字段, 提示（返回错误提示）
                    continue
                by_fields.append(getattr(self, f'_{operator}')(key, value))
        return query_fields, by_fields

    def _parse_property(self):
        """ (暂时没有使用)获得自定义的property （不包括_开头属性）"""
        fields = []
        for name, value in vars(self._model.__class__).items():
            if isinstance(value, property) and not name.startswith('_'):
                # property 同样屏蔽 `_`开头字段
                fields.append(name)
        return fields

    def _columns(self):
        """ 不包含_开头的所有数据字段(Column)名称

        返回 set
        """
        columns = inspect(self._model.__class__).columns
        all_columns = set([
            column.name for column in columns
            if not column.name.startswith('_')
        ])
        return all_columns

    def _gt(self, key, value):
        """
        大于
        :param key:
        :param value:
        :return:
        """
        return getattr(self._model, key) > value

    def _ge(self, key, value):
        """
        大于等于
        :param key:
        :param value:
        :return:
        """
        return getattr(self._model, key) > value

    def _lt(self, key, value):
        """
        小于
        :param key:
        :param value:
        :return:
        """
        return getattr(self._model, key) < value

    def _le(self, key, value):
        """
        小于等于
        :param key:
        :param value:
        :return:
        """
        return getattr(self._model, key) <= value

    def _eq(self, key, value):
        """
        等于
        :param key:
        :param value:
        :return:
        """
        return getattr(self._model, key) == value

    def _ne(self, key, value):
        """
        不等于
        :param key:
        :param value:
        :return:
        """
        return getattr(self._model, key) != value

    def _ic(self, key, value):
        """
        包含
        :param key:
        :param value:
        :return:
        """
        return getattr(self._model, key).like('%{}%'.format(value))

    def _ni(self, key, value):
        """
        不包含
        :param key:
        :param value:
        :return:
        """
        return getattr(self._model, key).notlike('%{}%'.format(value))

    def _by(self, key, value):
        """
        :param key:
        :param value: 0:正序,1:倒序
        :return:
        """
        try:
            value = int(value)
        except ValueError as e:
            # 记录错误
            current_app.logger.error(e)
            return getattr(self._model, key).desc()
        else:
            if value == 0:
                return getattr(self._model, key).asc()
            return getattr(self._model, key).desc()

    def _in(self, key, value):
        """
        查询多个相同字段的值
        :param key:
        :param value:
        :return:
        """
        value = value.split('|')
        return getattr(self._model, key).in_(value)
