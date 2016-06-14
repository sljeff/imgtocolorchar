#!/usr/bin/env python
# coding: utf-8

from PIL import Image
import sys

chars = 'MNHQ$OC?7>!:-;.'
colors = {
    'White'  : '\033[37m',
    'Black'  : '\033[30m',
    'Red'    : '\033[31m',
    'Green'  : '\033[32m',
    'Yellow' : '\033[33m',
    'Blue'   : '\033[34m',
    'Magenta': '\033[35m',
    'Cyan'   : '\033[36m',

    'Reset'  : '\033[0;0m'
}
model = 0


def getColor(rgbTuple):
    R = rgbTuple[0]
    G = rgbTuple[1]
    B = rgbTuple[2]
    aver = (R+G+B) / 3
    if aver >= 230:
        return colors['White']
    elif aver <= 50:
        return colors['Blue']
    elif R-G>=25 and R-B>=25 and R>150:
        return colors['Red']
    elif G-R>=25 and G-B>=25 and G>150:
        return colors['Green']
    elif B-R>=25 and B-G>=25 and B>150:
        return colors['Blue']
    elif R-G>=25 and B-G>=25:
        return colors['Magenta']
    elif G-R>=25 and B-R>=25:
        return colors['Cyan']
    elif G-B>=25 and R-B>=25:
        return colors['Yellow']
    else:
        return colors['Magenta']


def make_char_img(imgs):
    img_greyscale = imgs[0]
    img_rgb = imgs[1]

    pix_greyscale = img_greyscale.load()
    pix_rgb = img_rgb.load()

    pic_str = ''

    width, height = img_greyscale.size

    if model == 0:
        for h in xrange(height):
            for w in xrange(width):
                pic_str += chars[int(pix_greyscale[w, h]) * 14 / 255]
            pic_str += '\n'
    elif model == 1:
        for h in xrange(height):
            for w in xrange(width):
                # pic_str += getColor(pix_rgb[w, h])
                pic_str += colors.values()[int(pix_greyscale[w, h]) * 7 / 255]
                pic_str += chars[int(pix_greyscale[w, h]) * 14 / 255]
            pic_str += '\n'
        pic_str += colors['Reset']
    elif model == 2:
        for h in xrange(height):
            for w in xrange(width):
                pic_str += getColor(pix_rgb[w, h])
                pic_str += chars[int(pix_greyscale[w, h]) * 14 / 255]
            pic_str += '\n'
        pic_str += colors['Reset']

    return pic_str


def preprocess(img_name):
    img = Image.open(img_name)

    w, h = img.size
    m = max(img.size)
    delta = m / 80.0
    w, h = int(w * 1.7 / delta), int(h / delta)
    img = img.resize((w, h))
    img_greyscale = img.convert('L')
    img_rgb = img.convert('RGB')

    return (img_greyscale, img_rgb)

if __name__ == '__main__':
    img_file = sys.argv[1]
    if len(sys.argv) == 3:
        if sys.argv[2] == '1':
            model = 1
        elif sys.argv[2] == '2':
            model = 2

    imgs = preprocess(img_file)
    pic_str = make_char_img(imgs)
    print(pic_str)

