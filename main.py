import time
import json
import cv2
import pandas as pd
from get_coordinate import Process
import re
import pytesseract
import os
import platform
import numpy as np

if platform.system() is 'Windows':
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

if __name__ == "__main__":
    image = cv2.imread("ex.png")
    image_process = Process(image)
    img = image_process.img_re_vline  # 去除垂直隔線的原圖
    img_cor = image_process.x_coordinate()  # title_content座標
    img_g = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # 灰階二極化
    result = []
    for each_line in img_cor:
        line_dict = {}
        for idx in range(0, len(each_line), 2):
            try:
                key, value = each_line[idx], each_line[idx+1]
            except:
                key, value = each_line[idx], None
            iimg = cv2.resize(img_g[key[0]:key[1], key[2]:key[3]], dsize=None, fx=2, fy=2)
            key_word = pytesseract.image_to_string(iimg, config='--psm 3')
            key_word = key_word.lstrip(" !()-[]{};:'\",\\<>./?@\#$%^&*_~】").rstrip(" !(-[]{};:'\",\\<>./?@\#$%^&*_。\t\n\r\v\f")
            if value is not None:
                iimg = cv2.resize(img_g[value[0]:value[1], value[2]:value[3]], dsize=None, fx=2, fy=2)
                value_word = pytesseract.image_to_string(iimg, config='--psm 3')
                value_word = value_word.lstrip(" !()-[]{};:'\",\\<>./?@\#$%^&*_~】").rstrip(" !(-[]{};:'\",\\<>./?@\#$%^&*_。\t\n\r\v\f")
            else:
                value_word = None
            line_dict[key_word] = value_word
        result.append(line_dict)
    print(result)