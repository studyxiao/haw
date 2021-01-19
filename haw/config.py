class Config():
    """ 默认配置项 """
    # SECRET_KEY = ''  # 必须设置

    # SQLALCHMEY
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 文件上传配置
    FILE = {
        'ALLOW_EXTENSIONS': ['jpg', 'png'],
        'ALLOW_SINGLE_MAX_SIZE': 2 * 1024 * 1024,
        'ALLOW_ALL_MAX_SIZE': 5 * 1024 * 1024,
        'ALLOW_NUMS': 5,
        'STORE_DIR': 'upload'
    }

    UPLOAD_DIR = 'upload'
    ALLOW_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    EXCLUDE_EXTENSIONS = None  # 不允许的后缀
    SINGLE_LIMIT = 5 * 1024 * 1024  # 单文件限制 5M
    TOTAL_LIMIT = 25 * 1024 * 1024  # 25M
    FILE_NUMS = 5  # 单次允许上传文件数
    UPLOAD_PREFIX = '/upload'  # 定义文件访问前缀，如 /upload/2020/04/03/abc.png

    # Redis 配置
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_PASSWORD = None
    REDIS_EXPIRE = 10 * 60  # 10分钟

    # Celery 配置
    CELERY_BROKER = 'redis://localhost:6379/1'
    CELERY_BACKEND = 'redis://localhost:6379/2'

    # 邮件配置
    MAIL_SERVER = None
    MAIL_PORT = 25
    MAIL_USE_SSL = False
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    MAIL_DEFAULT_SENDER = 'test@test.test'

    # 前端相关配置
    FRONT_URL_ROOT = 'https://daohang.studyxiao.cn'  # 发送邮件的激活地址前缀
    # 发送邮件的激活地址前缀
    FRONT_REGISTER_VALID_PREFIX = 'http://localhost:8000/api/user/valid/'
    FRONT_RESET_PWD_PREFIX = 'http://localhost:8000/api/user/resetpwd/'
    SITE_NAME = 'studyxiao'  # 可用于发送邮件的前缀

    # 日志配置
    LOGGER_PATH = './logs'
    LOGGER_MAIL_HOST = ''  #
    LOGGER_MAIL_FROM_ADDR = ''  # example@test.co
    LOGGER_MAIL_TO_ADDRS = []  # ['example@test.co', 'example2@test.co']
    LOGGER_MAIL_SUBJECT = '【HAW】 ERROR'  # 主题

    # 分页
    PAGE_DEFAULT = 0  # 起始页
    COUNT_DEFAULT = 10  # 个数
