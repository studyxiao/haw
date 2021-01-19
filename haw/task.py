""" 异步任务 """
from flask import current_app, render_template
from flask_mail import Mail, Message

from .celery import celery

mail = Mail()


@celery.task
def send_mail(to, subject, template):
    """
    to: 发送给谁
    subject: 主题
    template: 模板
    """
    app = current_app._get_current_object()
    msg = Message(app.config.get('SITE_NAME') + subject,
                  sender=app.config.get('MAIL_DEFAULT_SENDER'),
                  recipients=[to])
    msg.html = template
    mail.send(msg)


def send_valid_mail(to, token, name, front_register_valid_prefix=None):
    """ 激活账户邮件

    :params to: 发送对象
    :params token: 生成的token，用于激活链接地址中
    :params name: 用户昵称
    :params front_register_valid_url: 前端注册激活前缀链接，可以在配置项中配置FRONT_URL_ROOT
    """
    valid_url = front_register_valid_prefix or current_app.config.get(
        'FRONT_REGISTER_VALID_PREFIX') + token
    subject = '账户激活'
    html = render_template('email/register.html',
                           valid_url=valid_url,
                           name=name,
                           website_name=current_app.config.get('SITE_NAME'))
    send_mail.delay(to, subject, html)


def send_forget_pwd_mail(to, token, front_reset_pwd_prefix=None):
    """ 忘记密码

    :params to: 发送对象
    :params token: 生成的token，用于链接地址中
    :params front_register_valid_url: 前端注册激活前缀链接，可以在配置项中配置FRONT_URL_ROOT
    """
    valid_url = front_reset_pwd_prefix or current_app.config.get(
        'FRONT_RESET_PWD_PREFIX') + token
    subject = '密码重置'
    html = render_template('email/forget.html', valid_url=valid_url)
    send_mail.delay(to, subject, html)
