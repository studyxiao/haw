from flask import request
from wtforms import Form, IntegerField, SelectField

from .exception import ParameterException


class BaseForm(Form):
    def __init__(self):
        data = request.get_json(silent=True)
        args = request.args.to_dict()
        if request.files:
            # TODO 文件单独上传？还是文件字段加入到 args 中？
            for key, value in request.files.items():
                args[key] = value
        super().__init__(data=data, **args)

    def validate_for_api(self):
        """ 仿写 validate 函数

        不同之处：发生错误时返回json化响应
        """
        valid = super().validate()
        if not valid:
            raise ParameterException(msg=self.errors)
        return self


def check_type(field, target_type=int):
    """ 检验数据类型 """
    if not isinstance(field.data, target_type):
        raise ParameterException(msg='参数类型错误')


def integer_validate(form, field):
    """ 检验数据是否为整数 """
    check_type(field)
    field.data = int(field.data)


class IntegerFieldX(IntegerField):
    """ 自定义整数字段 """
    def __init__(self, label=None, validators=None, **kwargs):
        if validators is not None and type(validators) == list:
            validators.insert(0, integer_validate)
        else:
            validators = [integer_validate]
        super().__init__(label, validators, **kwargs)


class SelectFieldX(SelectField):
    """ 针对enum设计的选择字段 """
    def iter_choices(self):
        for value, label in self.choices:
            yield (value, label, self.coerce(value) == self.data)

    def process_data(self, value):
        try:
            if self.default and not str(value).strip():
                value = self.default

            self.data = self.coerce(value)
        except (ValueError, TypeError):
            self.data = None

    def pre_validate(self, form):
        for v, _ in self.choices:
            if self.data == v:
                break
        else:
            raise ValueError(self.gettext('不是正确选项'))
