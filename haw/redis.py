import redis
from redis import ConnectionPool
from flask import Flask, current_app


class Redis:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        """ 配置初始化 """
        self.host = app.config.get('REDIS_HOST')
        self.port = app.config.get('REDIS_PORT')
        self.password = app.config.get('REDIS_PASSWORD')
        self.db = app.config.get('REDIS_DB')
        self.connection_pool = ConnectionPool(host=self.host,
                                              port=self.port,
                                              password=self.password)
        self.set_default_redis()

    def connect(self, db=0):
        """ 链接到那个数据库 """
        r = redis.Redis(connection_pool=self.connection_pool, db=db)
        return r

    def set_default_redis(self):
        """ 默认数据库 """
        self.default_redis = self.connect(db=self.db)

    def write(self, key, value, expire=None):
        """ 写入键值对 """
        expire = expire or current_app.config['REDIS_EXPIRE']
        self.default_redis.set(key, value, ex=expire)

    def read(self, key):
        return self.default_redis.get(key)

    def hset(self, key, value):
        """ 设置哈希 """
        self.default_redis.hset(key, value)

    def hget(self, name, key):
        """ 读取hash  """
        return self.default_redis.hget(name, key)

    def hgetall(self, name):
        """ 获取hash表所有值 """
        return self.default_redis.hgetall(name)

    def delete(self, *names):
        """ 删除一个或多个 """
        self.default_redis.delete(*names)

    def hdel(self, name, key):
        """ 删除 hash中的键值 """
        self.default_redis.hdel(name, key)

    def expire(self, name, expire_time=None):
        """ 设置过期时间 """
        expire_time = expire_time or self.app.config.get('REDIS_EXPIRE')
        self.default_redis.expire(name, expire_time)


redis_client = Redis()
