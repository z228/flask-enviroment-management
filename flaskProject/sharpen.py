from PIL import Image
from PIL import ImageFilter
from time import *


# 打开一张图片
def sharpen(img):
    image_object = Image.open(r'./static/result/' + img)
    # 使用 sharp filter
    sharpened1 = image_object.filter(ImageFilter.SHARPEN)

    save_name = strftime('sharpen%Y-%m-%d %H%M%S', localtime(time())) + '.png'
    sharpened1.save('./static/result/' + save_name, 'PNG')
    return save_name
