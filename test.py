#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PIL import Image
import hashlib


im = Image.open("captcha.gif")
# (将图片转换为8位像素模式)
# im = im.convert("P")

# 打印颜色直方图
print(im.histogram())

# 颜色直方图的每一位数字都代表了在图片中含有对应位的颜色的像素的数量。
# 每个像素点可表现256种颜色，你会发现白点是最多（白色序号255的位置，也就是最后一位，可以看到，有625个白色像素）。
# 红像素在序号200左右，我们可以通过排序，得到有用的颜色。
his = im.histogram()
values = {}

for i in range(256):
    values[i] = his[i]

for j, k in sorted(values.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(j, k)

# 我们得到了图片中最多的10种颜色，其中 220 与 227 才是我们需要的红色和灰色，可以通过这一讯息构造一种黑白二值图片。
im2 = Image.new("P", im.size, 255)
for x in range(im.size[1]):
    for y in range(im.size[0]):
        pix = im.getpixel((y, x))
        if pix == 220 or pix == 227:  # these are the numbers to get
            im2.putpixel((y, x), 0)

# im2.show()

# 得到单个字符的像素集合，由于例子比较简单，我们对其进行纵向切割
inletter = False
foundletter = False
start = 0
end = 0

letters = []

for y in range(im2.size[0]):
    for x in range(im2.size[1]):
        pix = im2.getpixel((y, x))
        if pix != 255:
            inletter = True
    if foundletter == False and inletter == True:
        foundletter = True
        start = y

    if foundletter == True and inletter == False:
        foundletter = False
        end = y
        letters.append((start, end))

    inletter = False
# 得到每个字符开始和结束的列序号。
print(letters)

count = 0
for letter in letters:
    m = hashlib.md5()
    im3 = im2.crop((letter[0], 0, letter[1], im2.size[1]))
    m.update('%s'.encode() % bytes(count))
    im3.save("./%s.gif" % (m.hexdigest()))
    count += 1
