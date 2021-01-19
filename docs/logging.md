## 系统日志

日志的格式、文件存储地址、自动切分日志

使用 logger 中的配置进行日志收集，info 以上输入到 info.log，error 输入到 errors.logs，默认的路径为项目路径下的'./logs'目录下，可通过设置 LOGGER_PATH 进行设置，修改后需要重启服务。

### 使用

```python
# 使用内置
current_app.logger.info('info')
current_app.logger.error('error')
# 自定义
import logging
logger = logging.getLogger(__name__)
logger.info('info')
```

## logging

几个知识点：formatter(格式化形式)、handler(处理器)、root 记录器（默认 logging 实例）

一个程序可以有多个记录器，默认是 root；一个记录器可以有多个处理器；一个处理器有一个对应格式化形式。

一个简单配置结构

```python
{
  "version": 1,  # 后续扩展，目前有效值只有1
  "disable_existing_loogers": True,  # 不允许非 root 记录器，默认是 True
  "formatters": {  # 输出格式
    "simple": {  # 格式名称（代号）
      "format": "%(message)s"  # 具体格式形式
    },
    "simple2": {
      "format": "[%(asctime)s] - %(message)s"
    }
  },
  "handlers":{  # 处理器, 也可多个
    "console": {
      "level": "DEBUG",  # 记录级别
      "class": "logging.StreamHandler",  # 输出到控制台
      "formatter": "simple",  # 输出格式
      "stream": "ext://flask.logging.wsgi_errors_stream"  # 监听flask日志
    }
  },
  "root":{  # 记录器
    "level": "INFO",
    "handlers": ["console"]  # 可多个
  }
}
```

## 教程

[Flask logging offical Example](https://flask.palletsprojects.com/en/1.1.x/logging/)

[一文看懂 Flask 的日志使用姿势](https://www.flyml.net/2018/12/12/flask-logging-usage-demo/) 【推荐】

https://www.cnblogs.com/cwp-bg/p/8946394.html

[Python logging Doc](https://docs.python.org/3.8/library/logging.html)

[配置文件详解](https://docs.python.org/3.8/library/logging.config.html#configuration-dictionary-schema)

[日志输出格式属性](https://docs.python.org/3.8/library/logging.html#logrecord-attributes)

[日志处理器](https://docs.python.org/3.8/library/logging.handlers.html#module-logging.handlers)
