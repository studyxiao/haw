import base64
import io
import random
import string
import os

from PIL import Image, ImageFont, ImageDraw

from .redis import redis_client
from .exception import ParameterException


class Captcha:
    """ 图片验证码

    生成 base64 格式验证码；
    并且存于 redis 中，需配合 redis 使用
    """
    def __init__(self,
                 width=100,
                 height=24,
                 fontsize=24,
                 font_nums=4,
                 font_path=None,
                 background='white',
                 line=True,
                 format='jpeg'):
        """ 初始化图片验证码

        :params width: 验证码图片宽度
        :params height: 验证码图片高度
        :params fontsize: 字体大小，最后字体大小与高度和宽度都有关，但最小不能小于8
        :params font_path: 字体路径，不设置则使用内置字体
        :params font_nums: 验证码字体个数
        :params background: 图片背景
        :params line: 是否绘制干扰线
        :params format: 图片格式
        """
        self.width = width
        self.height = height
        self.background = background
        self.line = line
        self.format = format
        self.font_nums = font_nums
        self.fontsize = max(min([fontsize, width / font_nums, height]), 8)
        self.image = Image.new('RGB', (width, height), background)
        if font_path is None:
            font_path = os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                'font/AlegreyaSansSC-Black.ttf')
        self.font = ImageFont.truetype(font_path, fontsize)
        self.draw = ImageDraw.Draw(self.image)

    def draw_lines(self, num=1):
        """ 划线 """
        for n in range(num):
            x1 = random.randint(0, int(self.width / 3))
            y1 = random.randint(0, int(self.height / 3))
            x2 = random.randint(int(self.height * 2 / 3), self.width)
            y2 = random.randint(self.height / 2, self.height)
            self.draw.line(((x1, y1), (x2, y2)), fill='black', width=1)

    def draw_text(self):
        """ 生成字体，目前仅数字 """
        x_float = 4  # 横向随机移动最大距离
        y_float = 2  # 纵向随机移动最大距离
        per_x_length = self.width / self.font_nums
        code = ''.join(random.sample(string.digits, self.font_nums))
        for item in range(len(code)):
            x = (per_x_length - x_float) * (item + 1) + random.randint(
                -x_float, x_float)
            y = (self.height - self.fontsize) + random.randint(
                -y_float, y_float)
            self.draw.text((x, y),
                           code[item],
                           fill=(random.randint(32,
                                                127), random.randint(32, 127),
                                 random.randint(32, 127)),
                           font=self.font)
        return code

    def get_code(self, save=True, sid=None, expire=1200):
        """ 生产验证码图像(base64格式) """
        # 随机数字验证码
        code = self.draw_text()
        # 绘制干扰线
        self.draw_lines()
        # 图片转为base64字符串
        buffered = io.BytesIO()
        self.image.save(buffered, format=self.format)
        _format = f'data:image/{self.format};base64,'
        img_str = bytes(_format, 'utf-8') + base64.b64encode(
            buffered.getvalue())
        if save:
            self.save(sid, code, expire)
        return img_str, code

    @staticmethod
    def save(sid, code, expire=1200):
        """ 保存至 redis, 默认20分钟过期 """
        if sid is None:
            raise ParameterException(msg='请传入 sid')
        redis_client.write(sid, code)

    @staticmethod
    def check_captcha(sid, code):
        """ 检查验证码有效性 """
        redis_code = redis_client.read(sid)
        if isinstance(redis_code, bytes):
            redis_code = redis_code.decode('utf8')
        if str(code) == str(redis_code):
            return True
        return False
