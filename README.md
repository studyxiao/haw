# 基于 Python Web 应用框架 Flask 的 RESTful API 服务

本项目目标是可以快速搭建自己的 API 服务，把所有通用逻辑封装，在新建项目时，只负责编写业务部分即可。

> 个人学习项目。

## 主要功能封装

### 封装基础数据模型 BaseModel

1. 通过实现上下文管理器简化数据库提交操作（每次的 commit 和可能的异常处理），
2. 数据操作异常 json 化，需要配合全局异常 json 化模块
3. model 可 json 化
4. 增改删查封装，包括分页查询等。
5. 基类模型，添加默认字段等；常用数据模型：User File 等。

### 异常处理

- 异常 json 化
- 统一返回标准，错误代号查看 `exception.md`

### 表单验证

表单异常 json 化

### 文件上传

- 图片上传、校验及存储
- 其他文件

### Redis 服务

- 提供键值对存储服务，如用于验证码存储
- 作为任务队列（邮件发送等）的存储数据库

### Celery 定时任务

- 实现简单任务

### 验证码

- 简单验证码生成，使用第三方字体，造成包体积较大

### 邮件发送

- 异步发送邮件

### 用户系统

- 基本的登录和鉴权

### 日志

- 系统日志, 错误收集：访问错误，逻辑错误，数据库错误
- 操作日志, 用户操作记录

### 工具函数

## 使用到的第三方库 (包)

- Flask
- Flask-SQLAlchemy
- PyMySQL
- Flask-Migrate
- Flask-WTF
- Flask-JWT-Extended
- Flask-Mail
- celery
- redis
- Pillow

## 优秀源码及教程

https://github.com/TaleLin/lin-cms-flask/

https://github.com/qzq1111/flask-restful-example

https://cjolowicz.github.io/posts/hypermodern-python-01-setup/

[Flask Best Practices](https://github.com/yangyuexiong/Flask_BestPractices)

[基于 Flask 开发企业级 REST API 应用（一）](https://juejin.im/post/5d3bc3d25188254cbc32b1cc)

[Flask project setup: TDD, Docker, Postgres and more - Part 1](https://www.thedigitalcatonline.com/blog/2020/07/05/flask-project-setup-tdd-docker-postgres-and-more-part-1/)

## TODO

- [ ] 返回内容格式统一化 https://blog.csdn.net/qq_22034353/article/details/88758395
- [ ] 消息通知服务
- [ ] 缓存
- [ ] 微信登录 手机注册
- [ ] 访问限制
- [ ] 单元测试
- [ ] 源码阅读
- [ ] os.path VS pathlib.Path
- [ ] LocalProxy

## 使用

```bash
pip install git+http://xxx.xxxx.com/xiao.git#egg=haw
```

## BUG 待修复或新提特性

- SQLAlchemy filter()方法传入表达式参数实现原理。此问题导致分类查询失效。
