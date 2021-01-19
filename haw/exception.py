from flask import request, json
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    code = 500
    error_code = 999
    msg = '服务器未知错误'

    def __init__(self, code=None, error_code=None, msg=None, headers=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        if headers:
            headers
        super().__init__(msg, None)

    def get_body(self, environ=None):
        body = dict(msg=self.msg,
                    error_code=self.error_code,
                    request=request.method + ' ' + request.path)
        return json.dumps(body)

    @staticmethod
    def get_url_no_param():
        """ 使用 request.path 代替 """
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]


class Success(APIException):
    code = 201
    msg = '成功'
    error_code = 0


class Failed(APIException):
    code = 400
    msg = '失败'
    error_code = 9999


class AuthFailed(APIException):
    code = 401
    msg = '认证失败'
    error_code = 10000


class NotFound(APIException):
    code = 404
    msg = '资源不存在'
    error_code = 10020


class ParameterException(APIException):
    code = 400
    msg = '参数错误'
    error_code = 10030


class InvalidTokenException(APIException):
    code = 401
    msg = '令牌失效'
    error_code = 10040


class ExpiredTokenException(APIException):
    code = 422
    msg = '令牌过期'
    error_code = 10050


class UnknownException(APIException):
    code = 500
    msg = '服务器未知错误'
    error_code = 999


class RepeatException(APIException):
    code = 400
    msg = '字段重复'
    error_code = 10060


class Forbidden(APIException):
    code = 401
    msg = '不可操作'
    error_code = 10070


class RefreshException(APIException):
    code = 401
    msg = 'refresh token 获取失败'
    error_code = 10100


class FileTooLargeException(APIException):
    code = 413
    msg = '文件体积过大'
    error_code = 10110


class FileTooManyException(APIException):
    code = 413
    msg = '文件数量过多'
    error_code = 10120


class FileExtensionException(APIException):
    code = 401
    msg = '文件扩展名不符合规范'
    error_code = 10130
