import os
import uuid

from flask import current_app, request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from .config import Config
from .tools import all_file_name


def get_full_url(url, image_prefix='image'):
    """
    url_root：http://127.0.0.1:5000/
    url: upload/2020/03/12/abc.png
    image_prefix：
    返回： http://127.0.0.1:5000/api/image/2020/03/12/abc.png
    """
    if url is None:
        return ''
    if url.startswith('http'):
        return url
    url_root = request.url_root

    if image_prefix.startswith('/'):
        image_prefix = image_prefix[1:]
    if image_prefix.endswith('/'):
        image_prefix = image_prefix[0:-1]
    return f'{url_root}{image_prefix}/{url}'


def generate_token(payload, expiration=600):
    """ 生成token，用于邮箱验证，找回密码等

    :payload: {id: user.id}
    """
    s = Serializer(current_app.config['SECRET_KEY'], expiration)
    return s.dumps(payload).decode('utf-8')


def load_token(token):
    """ 解析token，获得用户id等 payload """
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token.encode('utf-8'))
        return data
    except Exception:
        return None


def combine_config(field, custom=None):
    """ 根据字段名 获得最终配置项

    三个来源：用户初始化传递 > 项目自定义 config > 内部 config > None
    :params field: 查找字段 'UPLOAD_FOLDER'
    :params custom: {'UPLOAD_FOLDER': 'uploads'}
    :return: 配置值
    """
    if custom and custom.get(field):
        return custom.get(field)
    if current_app.config.get(field):
        return current_app.config.get(field)
    if hasattr(Config, field) and getattr(Config, field):
        return getattr(Config, field)
    return None


def random_filename(filename):
    """ 重命名文件
    @params: filename: e.g. abc.png
    @return e.g. adfgfgfgffg.png
     """
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


def paginate():
    """ 分页, 返回起始位置和每页个数 """
    count = int(
        request.args.get('count', current_app.config.get('COUNT_DEFAULT', 1)))
    start = int(
        request.args.get('page', current_app.config.get('PAGE_DEFAULT', 0)))
    count = min(max(0, count), current_app.config.get('MAX_COUNT_DEFAULT', 50))
    start = max(0, start) * count
    return start, count


def path_below_app(app, directory_path):
    """ app 对象所在目录下文件夹路径，不会自动创建。
    用来指定一些路径位置，如 设置migrations位置 """
    return os.path.join(app.root_path, directory_path)


def import_all(current_file, pkg_name):
    """  在__init__.py中导入所在文件夹下python文件，__init__.py或以__开头的py文件除外

    :params current_file: 当前文件路径，一般为 __file__
    :params current_file_name: 当前所在模块名称(文件夹)  __name__
    """
    modules = all_file_name(os.path.abspath(os.path.dirname(current_file)))
    [__import__(pkg_name + '.' + name) for name in modules]
