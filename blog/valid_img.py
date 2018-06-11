# -*- coding:utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random

from blog import settings


def get_random_color():
    res = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return res


def get_valid_img():
    image = Image.new('RGB', (settings.VALID_IMG_WIDTH, settings.VALID_IMG_HEIGHT), get_random_color())
    # 画笔
    draw = ImageDraw.Draw(image)
    # 样式
    font = ImageFont.truetype('blog/static/font/kumo.ttf', size = settings.FONT_SIZE)
    # 生成随机5个字符
    temp = []
    for i in range(5):
        random_num = str(random.randint(0, 9))
        random_low_alpha = chr(random.randint(97, 122))  # a-z
        random_upper_alpha = chr(random.randint(65, 90))  # A-Z

        random_char = random.choice([random_num, random_low_alpha, random_upper_alpha])
        draw.text((24+i*36, 0), random_char, get_random_color(), font= font)

        temp.append(random_char)

    # 造点 造线 造圆
    for i in range(2):
        x1 = random.randint(0, settings.VALID_IMG_WIDTH)
        x2 = random.randint(0, settings.VALID_IMG_WIDTH)
        y1 = random.randint(0, settings.VALID_IMG_HEIGHT)
        y2 = random.randint(0, settings.VALID_IMG_HEIGHT)
        draw.line((x1, y1, x2, y2), fill= get_random_color())

    for i in range(2):
        draw.point([random.randint(0,settings.VALID_IMG_WIDTH),random.randint(0, settings.VALID_IMG_HEIGHT)], fill= get_random_color())
        x = random.randint(0,settings.VALID_IMG_WIDTH)
        y = random.randint(0,settings.VALID_IMG_HEIGHT)
        draw.arc((x, y, x+10, y+5), 0, 360, fill=get_random_color())

    # 在内存中生成图片
    f = BytesIO()
    image.save(f, 'png')
    # 一张图片验证码
    data = f.getvalue()
    f.close()

    # 生成的随机字符串
    valid_str = ''.join(temp)

    res = (valid_str, data)
    return res
