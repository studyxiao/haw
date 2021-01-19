## captcha 图形验证码

### 获得图形验证码

`/api/captcha`，内置 api，在`xiao/cms/apicaptcha.py`。返回二进制图像资源。

e.g.

> data:image/png;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwc0U.......x9euduaei6NZaBpcWm6dG0drFnYrMWIyc9TRRRQB/9k=

把对应`code`存入 session 中，code 就是键名。

### 验证图形验证码

需要自己实现相应 api 视图，不过内部已经实现了生成、验证 API。在`haw/captcha.py`文件中的`get_code`、`check_captcha`

使用举例：

```python
captcha = Captcha()


@bp.route('/captcha')
def get_captcha():
    """ 获取验证码 """
    sid = request.args.get('sid')
    img, code = captcha.get_code(sid)
    return img

from haw.captcha import Captcha
@app.route('/api/login')
def login():
    sid = request.args.get('sid')
    code = request.args.get('code')
    if Captcha.check_captcha(sid, code):  # 前端提交的验证码键名
        raise Fail(msg='验证码错误')
```
