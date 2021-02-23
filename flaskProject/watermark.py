from cv2 import cv2
import numpy as np
from PIL import Image
from time import *
import os


# img = np.array(Image.open(r'2.png').convert('RGB'))

def mark(image):
    print(image)
    if os.path.exists(r'./static/uploads/' + image):
        img = cv2.imread(r'./static/uploads/' + image)
    else:
        img = cv2.imread(r'./static/result/' + image)
    new = np.clip(2.0 * img - 160, 0, 255).astype(np.uint8)
    save_name = strftime('water%Y-%m-%d %H%M%S', localtime(time())) + '.png'
    cv2.imwrite('./static/result/' + save_name, new)
    return save_name
