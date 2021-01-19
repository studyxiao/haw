## 基本配置

|          配置项           | 类型 |          默认           | 必需设置 |                      说明                       |
| :-----------------------: | :--: | :---------------------: | -------- | :---------------------------------------------: |
|        SECRET_KEY         | str  |                         | 是       |            验证码存入 session 时使用            |
|  SQLALCHEMY_DATABASE_URI  | str  |                         | 是       |            **必须**设置，数据库 uri             |
|      FRONT_URL_ROOT       | str  | https://127.0.0.1:8080/ |          |      前端根地址，用于发送激活邮件等设置。       |
|        SITE_DOMAIN        | str  |                         |          |                    后端域名                     |
|       PAGE_DEFAULT        | int  |            0            |          |                   默认起始页                    |
|       COUNT_DEFAULT       | int  |           10            |          |                  默认每页条数                   |
|     MAX_COUNT_DEFAULT     | int  |           20            |          |                默认每页最大条数                 |
|        UPLOAD_PATH        | str  |        uploads/         |          |                  文件上传路径                   |
|        MAIL_SERVER        | str  |           无            | 是       |   强制设置，不设置会报错，<br />smtp.163.com    |
|         MAIL_PORT         | str  |           无            | 是       |                       25                        |
|       MAIL_USERNAME       | str  |           无            | 是       |                    邮箱地址                     |
|       MAIL_PASSWORD       | str  |           无            | 是       |                      密码                       |
|    MAIL_DEFAULT_SENDER    | str  |           无            | 是       |          ('someone', 'example.a.com')           |
| JWT_ACCESS_TOKEN_EXPIRES  | int  |        60\*60\*2        |          |              令牌过期时间，2 小时               |
| JWT_REFRESH_TOKEN_EXPIRES | int  |     60\*60\*24\*30      |          |                 刷新令牌，30 天                 |
|        REDIS_HOST         | str  |                         | 是       |                 redis 设置 host                 |
|        REDIS_PORT         | int  |                         | 是       |                   redis 端口                    |
|         REDIS_DB          | int  |                         | 是       |                     数据库                      |
|      REDIS_PASSWORD       | str  |                         |          |            数据库密码，没有可不设置             |
|       REDIS_EXPIRE        | int  |           60            |          |                 过期时间 60 秒                  |
|       CELERY_BROKER       | str  |                         | 是       | celery broker url，使用 celery 时是**必须**参数 |
|      CELERY_BACKEND       | str  |                         | 是       | celery backend url,使用 celery 时是**必须**参数 |
|        LOGGER_PATH        | str  |         ./logs          |          | 日志存放路径，默认为相对根目录下的/logs 文件夹  |

**备注**

- MAIL 相关与 Flask-Mail 插件有关，更多配置查看[官方文档](https://pythonhosted.org/Flask-Mail/)。
- JWT\_相关与 Flask-JWT-extended 相关。
- 在启用 redis 插件时，为了保证已启动 redis 服务，强制使用时设置 redis 相关值。
- celery 配置项也是使用时强制设置。
- FRONT_URL_ROOT 发送激活或重置密码邮件，后期是否替换为固定激活链接、重置密码链接等。

https://github.com/qzq1111/flask-restful-example
