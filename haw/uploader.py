""" 文件上传 """
import hashlib
from typing import List
from uuid import uuid1
from datetime import datetime
from pathlib import Path

from flask import current_app

from .model import File, db
from .utils import get_full_url


class Uploader:
    def __init__(self, files, config: dict = {}) -> None:
        """ files: request.files """
        self.allow_extensions: List[str] = []
        self.allow_single_max_size: int = 1024 * 1024 * 2  # 2M
        self.allow_all_max_size: int = 1024 * 1024 * 10  # 10M
        self.allow_nums: int = 5
        self.file_storages = []  # 所有上传的文件（fileStorage）
        self.set_config(config)
        self.get_fileStorage(files)
        self.verify()

    def set_config(self, config: dict) -> None:
        """ 设置配置项，自定义 config > 内部预设 """
        default_config = current_app.config.get('FILE')
        self.allow_extensions = config.get('ALLOW_EXTENSIONS',
                                           default_config['ALLOW_EXTENSIONS'])
        self.allow_single_max_size = config.get(
            'ALLOW_SINGLE_MAX_SIZE', default_config['ALLOW_SINGLE_MAX_SIZE'])
        self.allow_all_max_size = config.get(
            'ALLOW_ALL_MAX_SIZE', default_config['ALLOW_ALL_MAX_SIZE'])
        self.allow_nums = config.get('ALLOW_NUMS',
                                     default_config['ALLOW_NUMS'])
        app_path = current_app.root_path
        store_dir = config.get('STORE_DIR', default_config['STORE_DIR'])
        if store_dir.startswith('..') or store_dir.startswith('/'):
            assert Exception('文件存储路径只能是 app 实例下的相对路径')
        if store_dir.endswith('/'):
            store_dir = store_dir[0:-1]
        self._relation_store_dir = store_dir
        self.store_dir: Path = Path(app_path) / store_dir

    def get_fileStorage(self, files) -> None:
        """ files: request.files """
        for key, v in files.items():
            self.file_storages += files.getlist(key)

    def verify(self) -> None:
        """ 验证是否符合条件 """
        if self.file_storages == []:
            raise Exception('未传入文件')
        self._check_extention()
        self._check_size()

    def _check_extention(self):
        for _file in self.file_storages:
            filename = _file.filename
            if '.' not in filename:
                raise Exception('文件格式不正确')
            ext = filename.split('.')[-1]
            if ext not in self.allow_extensions:
                raise Exception('文件格式不正确')

    def _check_size(self):
        lens = len(self.file_storages)
        if lens > self.allow_nums:
            raise Exception('文件过多')

        total_size = 0
        for _file in self.file_storages:
            size = self.__get_size(_file)
            if size > self.allow_single_max_size:
                raise Exception('文件太大')
            total_size += size
        if total_size > self.allow_all_max_size:
            raise Exception('文件总体积过大')

    @staticmethod
    def __get_size(file):
        file.seek(0, 2)  # seek()跳到指定位置，2表示从文件末尾，0表示偏移量
        size = file.tell()  # tell() 获得当前指针位置，获得文件大小
        file.seek(0)  # 跳到文件起始位置，第二个参数默认为0（表示从文件起始），
        return size

    @staticmethod
    def __get_ext(file):
        filename = file.filename
        ext = filename.split('.')[-1]
        return ext

    def rename(self, file):
        uuid = uuid1().hex
        name = f'{uuid}.{self.__get_ext(file)}'
        return name

    @staticmethod
    def generate_md5(file):
        md5 = hashlib.md5()
        md5.update(file.read())
        file.seek(0)
        md5 = md5.hexdigest()
        return md5

    def make_dir(self):
        time = datetime.now()
        year = time.year
        month = time.month
        day = time.day
        relation_path = Path(
            self._relation_store_dir) / str(year) / str(month) / str(day)
        path = self.store_dir / str(year) / str(month) / str(day)
        Path.mkdir(path, parents=True, exist_ok=True)
        return relation_path, path

    def upload(self):
        result = []
        for _file in self.file_storages:
            md5 = self.generate_md5(_file)
            exited = File.query.filter_by(md5=md5).first()
            if not exited:
                relation_path, path = self.make_dir()
                name = self.rename(_file)
                _file.save(str(path / name))
                try:
                    exited = File(
                        **{
                            'name': name,
                            'md5': md5,
                            'path': str(relation_path),
                            'type': 1,
                            'extension': self.__get_ext(_file),
                            'size': self.__get_size(_file)
                        })
                    db.session.add(exited)
                    db.session.commit()
                except Exception:
                    db.session.rollback()
            result.append({
                'name': exited.name,
                'path': get_full_url(exited.path)
            })
        return result
