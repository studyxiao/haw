## 发送邮件

### 注册邮件

传入变量

name: 用户昵称
website_name: 网站名
valid_url: 验证地址

```
@bp.route('/send-email-celery')
def send_email_celery():
    """ 使用celery发送激活链接邮件 """
    send_valid_mail.delay('example@163.com', 'token127')
    return Success(msg='发送成功')
```

参考：

http://www.pythondoc.com/flask-celery/first.html#id5
