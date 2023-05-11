import numpy as np
from itertools import groupby
import cv2
from matplotlib import pyplot as plt


# %%
def draw(img): #畫圖用的
    plt.figure(figsize=(10,8))
    plt.imshow(img,cmap = "gray")
    plt.show()

# %%
class projection:
    def __init__(self,sum_arr):
        self.sum_arr = sum_arr
    def get_loc(self,threshold = 0):
        i = 0
        loc = []
        for key,group in groupby(self.sum_arr):
            elems = len(list(group))
            if key > threshold :
                loc.append((i,i+elems))
            i+=elems
        return loc


# %%
class Process:
    def __init__(self, image):
        # self.img_path = image_path #原圖
        # self.img = cv2.imread(self.img_path)
        self.img = image
        self.img_re_vline = self.vertical_line_remove()

    @staticmethod   
    def to_gray(image): #灰階
        gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
        gray = cv2.threshold(gray,254,255,cv2.THRESH_BINARY)[1]
        return gray
    
    def vertical_line_remove(self):
        img  = self.img
        bin_img = cv2.threshold(self.to_gray(img), 254, 255, cv2.THRESH_BINARY)[1]
        counts_Bk = np.sum(bin_img == 0, axis=0)
        v_line = [i for i,e in enumerate(counts_Bk) if e> len(self.img)*0.9]
        for i in v_line:
            img[:,i]=255
        return img

    @staticmethod
    def count_color(image, axis = 1): #求特定顏色的投影量 axis = 0 求垂直的加總
        lstBk = np.sum(image == 0, axis=axis) # 黑
        lstB = np.sum(image == 29, axis=axis) # 
        lstR = np.sum(image == 76, axis=axis) #
        lstW = np.sum(image != 255, axis=axis) # 白色以外
        return lstBk, lstB, lstR, lstW

    def y_coordinate(self): #取得分隔線的y座標
        y_coord = []
        gray_img = self.to_gray(self.img)
        y_count_Bk = self.count_color(gray_img)[0]
        y_seg_line = [i for i,e in enumerate(y_count_Bk) if  e > len(self.img[0])*0.9]
        for i, End in enumerate(y_seg_line[1:]):
            Start = y_seg_line[i]
            if (End - Start) > (len(gray_img) / len(y_seg_line)):
                y_coord.append((Start,End))
        return y_coord
    
    def x_coordinate(self): # 取得絕對座標
        gray_img = self.to_gray(self.img_re_vline)
        loc = []
        for i in self.y_coordinate(): #分割線座標
            start,end = i
            img_y_seg = gray_img[start:end]
            
            #形態學
            y_seg_erode = cv2.erode(img_y_seg,np.ones((int(len(img_y_seg[0])/100),int(len(img_y_seg[0])/100)), np.uint8))
            y_seg_open = cv2.morphologyEx(y_seg_erode,cv2.MORPH_OPEN,np.ones((int(len(img_y_seg[0])/5),int(len(img_y_seg)/5)), np.uint8))

            #依據顏色分組
            groups = []
            group = []
            for i, p in enumerate(y_seg_open[int(len(y_seg_open)/2)]):
                if p == 0 and len(group) == 0:
                    group.append(i)
                elif p == 255 and len(group) == 1:
                    group.append(i-1)
                    groups.append([start,end]+group)
                    group = []
            if len(group) == 1:
                group.append(i)
                groups.append(group)
            loc.append(groups)
        return loc


# %%
if __name__ == "__main__":
    pass
