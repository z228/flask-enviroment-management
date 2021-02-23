from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from time import *


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
    save_name = strftime('hua%Y-%m-%d %H%M%S', localtime(time())) + '.png'
    new_img.save('./static/result/' + save_name, 'PNG')
    return save_name
