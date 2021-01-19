""" 目前是固定格式，后期扩展为可配置插件 from yml """
from pathlib import Path


def logging_conf(app):
    logger_path = app.config.get('LOGGER_PATH')
    logger_mail_host = app.config.get('LOGGER_MAIL_HOST')
    logger_mail_from_addr = app.config.get('LOGGER_MAIL_FROM_ADDR')
    logger_mail_to_addrs = app.config.get('LOGGER_MAIL_TO_ADDRS')
    logger_mail_subject = app.config.get('LOGGER_MAIL_SUBJECT')
    Path(logger_path).mkdir(exist_ok=True)
    _logging_conf = {
        "version": 1,  # 目前固定1
        "disable_existing_loggers": False,  # 允许存在非 root 的 logger 记录器
        "formatters": {  # 输出格式
            "simple": {
                "format": "%(message)s"
            },
            "error": {
                "format":
                "[%(asctime)s][%(filename)s:%(lineno)s][%(thread)s][%(funcName)s] - %(message)s"
            }
        },
        "handlers": {  # 处理器
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",  # 输出的控制台
                "formatter": "simple",
                "stream": "ext://flask.logging.wsgi_errors_stream"  # 监听flask日志
            },
            "info_file": {
                "level": "INFO",
                "class": "logging.handlers.RotatingFileHandler",  # 输出到文件
                "formatter": "simple",
                "filename": f"{logger_path}/info.log",
                "maxBytes": 10485760,  # 每个文件最大10MB
                "backupCount": 20,  # 最多保留20个文件备份
                "encoding": "utf8"
            },
            "error_file": {
                "level": "ERROR",
                "class": "logging.handlers.RotatingFileHandler",  # 输出到文件
                "formatter": "error",
                "filename": f"{logger_path}/errors.log",
                "maxBytes": 10485760,  # 每个文件最大10MB
                "backupCount": 20,  # 最多保留20个文件备份
                "encoding": "utf8"
            },
            "email": {
                "level": "ERROR",
                "class": "logging.handlers.SMTPHandler",
                "mailhost": logger_mail_host,
                "fromaddr": logger_mail_from_addr,
                "toaddrs": logger_mail_to_addrs,
                "subject": logger_mail_subject,
            }
        },
        # "loggers": {  # 其它日志对象
        #     "app": {  # 定义一个名为 app 的 logger 对象
        #         "level": "DEBUG",
        #         "handlers": ["console"],
        #     }
        # },
        "root": {  # root 日志对象（记录器），默认记录器
            "level": "INFO",
            "handlers": ["console", "info_file", "error_file", "email"]
        }
    }
    return _logging_conf
