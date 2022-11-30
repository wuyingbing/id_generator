from operator import index
import os
from tkinter import font
import PIL.Image as PImage
from PIL import ImageFont, ImageDraw
import cv2

base_dir = os.path.join(os.path.dirname(__file__), 'usedres')


def changeBackground(img, img_back, zoom_size, center):
    # 缩放
    img = cv2.resize(img, zoom_size)
    rows, cols, channels = img.shape

    # 转换hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # 获取mask
    # lower_blue = np.array([78, 43, 46])
    # upper_blue = np.array([110, 255, 255])
    diff = [5, 30, 30]
    gb = hsv[0, 0]
    lower_blue = np.array(gb - diff)
    upper_blue = np.array(gb + diff)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # cv2.imshow('Mask', mask)

    # 腐蚀膨胀
    erode = cv2.erode(mask, None, iterations=1)
    dilate = cv2.dilate(erode, None, iterations=1)

    # 粘贴
    for i in range(rows):
        for j in range(cols):
            if dilate[i, j] == 0:  # 0代表黑色的点
                img_back[center[0] + i,
                         center[1] + j] = img[i, j]  # 此处替换颜色，为BGR通道

    return img_back


def paste(avatar, bg, zoom_size, center):
    avatar = cv2.resize(avatar, zoom_size)
    rows, cols, channels = avatar.shape
    for i in range(rows):
        for j in range(cols):
            bg[center[0] + i, center[1] + j] = avatar[i, j]
    return bg


def generator(name, sex, nation, year, mon, day, addr, idn, org, life, fname):

    # print fname
    im = PImage.open(os.path.join(base_dir, 'empty.png'))
    avatar = PImage.open(os.path.join(base_dir, fname))  # 500x670

    name_font = ImageFont.truetype(os.path.join(base_dir, 'hei.ttf'), 72)
    other_font = ImageFont.truetype(os.path.join(base_dir, 'hei.ttf'), 60)
    bdate_font = ImageFont.truetype(os.path.join(base_dir, 'fzhei.ttf'), 60)
    id_font = ImageFont.truetype(os.path.join(base_dir, 'ocrb10bt.ttf'), 72)

    draw = ImageDraw.Draw(im)
    draw.text((630, 690), name, fill=(0, 0, 0), font=name_font)
    draw.text((630, 840), sex, fill=(0, 0, 0), font=other_font)
    draw.text((1030, 840), nation, fill=(0, 0, 0), font=other_font)
    draw.text((630, 980), year, fill=(0, 0, 0), font=bdate_font)
    draw.text((950, 980), mon, fill=(0, 0, 0), font=bdate_font)
    draw.text((1150, 980), day, fill=(0, 0, 0), font=bdate_font)
    start = 0
    loc = 1120
    ends = []
    width = 0
    for index, c in enumerate(addr):
        if width >= 22:
            ends.append(index)
            width = 0
        if ord(c) < 128:
            width += 1
        else:
            width += 2
    ends.append(len(addr))

    for index, end in enumerate(ends):
        draw.text((630, loc),
                  addr[((ends[index - 1]) if index > 0 else 0):end],
                  fill=(0, 0, 0),
                  font=other_font)
        loc += 100
    draw.text((950, 1475), idn, fill=(0, 0, 0), font=id_font)
    draw.text((1050, 2750), org, fill=(0, 0, 0), font=other_font)
    draw.text((1050, 2895), life, fill=(0, 0, 0), font=other_font)
    avatar = avatar.resize((500, 670))
    avatar = avatar.convert('RGBA')
    im.paste(avatar, (1500, 690), mask=avatar)
    im.save('color.png')
    im.convert('L').save('bw.png')
    print(u'成功', u'文件已生成到目录下,黑白bw.png和彩色color.png')


def main():
    generator(name='吴XXX',
              sex='男',
              nation='汉',
              year='2010',
              mon='1',
              day='1',
              addr='北京市昌平区东小镇', 
              idn='123456789012345678', # 18位的身份证号, 不会验证号码
              org='北京市公安局昌平分局',
              fname='avatar.png',  # 头像的照片, 背景是透明的png.
              life='2016.11.07-2036.11.07')


if __name__ == "__main__":
    main()
