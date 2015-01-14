# -*- coding: utf-8 -*-
# ref:
# http://www.wieschoo.com/tutorials/botsuite/captcha-ocr-tutorial-neural-network/00746/
# http://weijr-note.blogspot.tw/2012/11/python.html
# http://opencv-python-tutroals.readthedocs.org/en/latest/index.html
import cv2
import cv
import numpy as np
import pytesser
import random
import json
from collections import defaultdict

__all__ = ['TwseHisTraderCaptcha0', 'TwseHisTraderCaptcha1']

class TwseHisTraderCaptcha0(object):
    def __init__(self, debug=False):
        self._debug = debug

    def run(self, img):

        def normalize(img):
            img = cv2.cvtColor(img, cv2.CV_32F)
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            gray = cv2.equalizeHist(gray)
            ret,th0 = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
            return th0

        def resize(img, resize=1):
            h,w = img.shape
            img = cv2.resize(img, (w*resize,h*resize), interpolation=cv2.INTER_CUBIC)
            return img

        def feature(img):
            kernel = np.ones((1,1), np.uint8)
            # smooth backgroun noise
            blur = cv2.GaussianBlur(img, (5,5), 0)
            # threshold filter
            ret,th1 = cv2.threshold(blur, 235, 255, cv2.THRESH_BINARY)
            # colsing/opening
            open = cv2.morphologyEx(th1, cv2.MORPH_OPEN, kernel, iterations=5)
            close = cv2.morphologyEx(open, cv2.MORPH_CLOSE, kernel, iterations=5)
            mask = cv2.bitwise_and(th1, th1, mask=close)
            return mask

        def debug(img):
            cv2.imshow('test', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        ft = feature(resize(normalize(img)))
        text = pytesser.iplimage_to_string(cv.fromarray(ft), 'eng').strip()
        if self._debug:
            debug(ft)
            text = raw_input("debug:")
        return text if text else ''


class TwseHisTraderCaptcha1(object):
    def __init__(self, debug=False):
        self._debug = debug

    def run(self, img):

        def normalize(img):
            img = cv2.cvtColor(img, cv2.CV_32F)
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            gray = cv2.equalizeHist(gray)
            ret,th0 = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
            return th0

        def resize(img, resize=1):
            h,w = img.shape
            img = cv2.resize(img, (w*resize,h*resize), interpolation=cv2.INTER_CUBIC)
            return img

        def boundary(img, bund=3):
            h, w = img.shape
            # find best match captcha area
            # smooth background noise
            blur = cv2.GaussianBlur(img, (5,5), 0)
            # threshold filter
            ret,th1 = cv2.threshold(blur, 235, 255, cv2.THRESH_BINARY)
            contours,hierarchy = cv2.findContours(th1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            area = lambda (x, y, w, h): (w*h, x, y, w, h)
            best = sorted([area(cv2.boundingRect(cnt)) for cnt in contours], reverse=True)
            # iter sub captcha
            x0 = lambda x: x-bund if x > bund else 0
            y0 = lambda y: y-bund if y > bund else 0
            x1 = lambda x: x+bund if w-bund > x else w
            y1 = lambda y: y+bund if h-bund > y else h
            for it in sorted(best[:5], key=lambda x: x[1]):
                yield ((x0(it[1]),y0(it[2])), (x1(it[1]+it[3]),y1(it[2]+it[4])))

        def feature(img):
            kernel = np.ones((1,1), np.uint8)
            # smooth backgroun noise
            blur = cv2.GaussianBlur(img, (5,5), 0)
            # threshold filter
            ret,th1 = cv2.threshold(blur, 235, 255, cv2.THRESH_BINARY)
            # colsing/opening
            open = cv2.morphologyEx(th1, cv2.MORPH_OPEN, kernel, iterations=5)
            close = cv2.morphologyEx(open, cv2.MORPH_CLOSE, kernel, iterations=5)
            mask = cv2.bitwise_and(th1, th1, mask=close)
            return mask

        def debug(img, bund):
            cv2.rectangle(img, bund[0], bund[1], (255,255,255), 1)
            cv2.imshow('test', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        text = ''
        img = resize(normalize(img), 1)
        h, w = img.shape
        bkimg = np.zeros((h,w,3), np.uint8)
        bkimg = resize(normalize(bkimg), 1)
        for bund in boundary(img):
            x,y = zip(*bund)
            bkimg[y[0]:y[1],x[0]:x[1]] = img[y[0]:y[1],x[0]:x[1]]
            if self._debug:
                debug(feature(bkimg), bund)
        text = pytesser.iplimage_to_string(cv.fromarray(feature(bkimg)), 'eng').strip()
        return text if text else ''


def test_captcha():
    exp = ['HKYAX', 'YK2F1', 'EVAH8']
    record = defaultdict(list)
    tests = [
        TwseHisTraderCaptcha0(debug=True),
        TwseHisTraderCaptcha1(debug=True),
    ]
    for test in tests:
        cnt = 0
        for i,it in enumerate(exp):
            img = cv2.imread("./crawler/spiders/train/twse_test%d.jpeg" %(i))
            cnt = cnt + 1 if test.run(img) == exp[i] else cnt
        record[cnt].append((test.__class__.__name__))
    print json.dumps(record, sort_keys=True, indent=4, separators=(',', ': '))

def main():
    test_captcha()

if __name__ == '__main__':
    main()
