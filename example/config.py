import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = '123456'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        BASE_DIR, 'example.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MIGRATIONS_DIR = os.path.join(BASE_DIR, 'migrations')

    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    ALLOW_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10M
    UPLOAD_PREFIX = '/image'  # 定义文件访问前缀，如 /image/2020/04/03/abc.png
