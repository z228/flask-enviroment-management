# -*- coding: UTF-8 -*-
from aip import AipOcr

# 定义常量
APP_ID = '23693404'  # 百度生成的
API_KEY = 'OUyhOWVScVG2diDe5E1Qv50n'
SECRET_KEY = 'LVrDQqFP9ESaoQC3Q21keGm0psMF9GOX'

# 初始化AipFace对象
aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)


# 读取图片
def get_file_content(filePath):
    with open('./static/result/' + filePath, 'rb') as fp:
        return fp.read()


# 定义参数变量
options = {
    'detect_direction': 'true',
    'language_type': 'CHN_ENG',
}


# 调用通用文字识别接口

def ocr(image):
    result = aipOcr.basicAccurate(get_file_content(image), options)  # basicAccurate是高精度版，识别率高， basicGeneral是普通识别版
    txt = ''
    for i in result['words_result']:
        txt += '<p>'+i['words'] + '</p>'
    print(txt)
    return txt
