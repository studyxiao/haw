'''
目前没有使用，作为保留模块，后期整合
返回前端前进行数据整合清理
'''


class ViewModel:
    __name = '子类中定义属性,作为返回属性,字段需和model一致'

    def __init__(self, model=None, *args, **kwargs):
        """ 一般情况下，都需要重写此方法，进行数据清洗 """
        if model:
            self.set_attrs(dict(model))

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            setattr(self, key, value)

    def __getitem__(self, item):
        return getattr(self, item)

    def keys(self):
        fields = []
        for name, v in vars(self.__class__).items():
            if isinstance(v, property):
                fields.append(name)
            if not name.startswith('__') and not callable(v):
                fields.append(name)
        fields = list(set(fields))
        return fields


class Collection:

    view_model = ViewModel

    def fill(self, query_items):
        self.total = len(query_items)
        self.items = [self.view_model(q_item) for q_item in query_items]

    def collect(self, query_items):
        """ 仅返回清洗的数据集 """
        return [self.view_model(q_item) for q_item in query_items]

    def __getitem__(self, item):
        return getattr(self, item)

    def keys(self):
        return ['total', 'items']
