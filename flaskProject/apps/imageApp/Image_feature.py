# -*- coding: UTF-8 -*-
from cv2 import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageFont, ImageDraw
from time import *
import os
from aip import AipOcr

_uploads_path = './static/uploads/'
_result_path = 'static/results/'


def mark(image):
    print(image)
    _u = _uploads_path + image
    _r = _result_path + image
    img = np.ndarray
    if os.path.exists(_u):
        img = cv2.imread(_u)
    elif os.path.exists(_r):
        img = cv2.imread(_r)
    new = np.clip(2.0 * img - 160, 0, 255).astype(np.uint8)
    save_name = strftime('water%Y-%m-%d_%H%M%S', localtime(time())) + '.png'
    cv2.imwrite(_result_path + save_name, new)
    return save_name


# 打开一张图片 尖锐化
def sharpen(img):
    image_object = Image.open(_result_path + img)
    # 使用 sharp filter
    sharpened1 = image_object.filter(ImageFilter.SHARPEN)

    save_name = strftime('sharpen%Y-%m-%d_%H%M%S', localtime(time())) + '.png'
    sharpened1.save(_result_path + save_name, 'PNG')
    return save_name


# 读取图片
def get_file_content(filename):
    _u = _uploads_path + filename
    _r = _result_path + filename
    if os.path.exists(_u):
        with open(_u, 'rb') as fp:
            return fp.read()
    elif os.path.exists(_r):
        with open(_r, 'rb') as fp:
            return fp.read()


# 调用通用文字识别接口
def ocr(image):
    # 定义常量
    app_id = '23693404'  # 百度生成的
    api_key = 'OUyhOWVScVG2diDe5E1Qv50n'
    secret_key = 'LVrDQqFP9ESaoQC3Q21keGm0psMF9GOX'

    # 初始化AipFace对象
    aip_ocr = AipOcr(app_id, api_key, secret_key)
    # 定义参数变量
    options = {
        'detect_direction': 'true',
        'language_type': 'CHN_ENG',
    }
    result = aip_ocr.basicAccurate(get_file_content(image), options)  # basicAccurate是高精度版，识别率高， basicGeneral是普通识别版
    txt = ''
    for i in result['words_result']:
        txt += '<p>' + i['words'] + '</p>'
    return txt


def change(txt, from_file):
    font_size = 10
    font = ImageFont.truetype('simsun.ttc', font_size)  # 9为字体大小
    im_path = from_file  # 原图路径
    im = Image.open(from_file)
    width, height = im.size
    new_img = Image.new("RGBA", (width, height), (10, 10, 10))  # 背景色rgb，偏黑显示好一些
    x = 0
    for i in range(0, height, font_size):  # 需要与字体大小一致
        for j in range(0, width, font_size):  # 需要与字体大小一致
            a, b, c = im.getpixel((j, i))
            draw = ImageDraw.Draw(new_img)
            draw.text((j, i), str(txt[x % len(txt)]), fill=(a, b, c), font=font)
            x += 1
            del draw
    save_name = strftime('hua%Y-%m-%d_%H%M%S', localtime(time())) + '.png'
    new_img.save(_result_path + save_name, 'PNG')
    return save_name
