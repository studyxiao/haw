## 使用 celery 处理耗时过程

### 默认使用 xiao 时启用了 celery，在初始化时可设置

```python
Lin(celery=False)
# 或者
lin.init_app(celery=False)
```

### 配置

```python
class Config:
    CELERY_BROKER = 'redis://:123456@127.0.0.1:6379/0'
    CELERY_BACKEND = 'redis://:123456@127.0.0.1:6379/0'
```

- redis 有密码：redis://:123456@127.0.0.1:6379/0
- redis 没有密码：redis://127.0.0.1:6379/0

### 使用

```python
from xiao.celery import celery

@celery.task
def send_email():
    ...
```

默认使用 flask context 环境。

记得提前运行 celery 服务

```bash
# Linux
# celery_worker.celery 的含义 celery_app_path.celery_app_file:celery_app_name   默认celery_app_name为celery可不写
celery worker -A celery_worker.celery -l INFO
```

https://medium.com/@frassetto.stefano/flask-celery-howto-d106958a15fe

http://einverne.github.io/post/2018/05/flask-celery-import-error.html

https://github.com/Ushinji/celery_sample/blob/master/docker-compose.yml

https://github.com/celery/celery/blob/master/docker/docker-compose.yml

https://docs.celeryproject.org/en/v4.4.5/getting-started/first-steps-with-celery.html#first-steps

https://flask.palletsprojects.com/en/1.1.x/patterns/celery/
