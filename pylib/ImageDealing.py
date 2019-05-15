# -*- coding: utf-8 -*-

import sys, os, time

import cv2
from PIL import  Image
import  numpy

def imageRotate(tImage):
    if os.path.exists(tImage) is False:
        print (u"image not exist")
        return

    lImg = Image.open(tImage)
    width, height = lImg.size


def imageRotateByCv(tImage):
    if os.path.exists(tImage) is False:
        print (u"image not exist")
        return
    lImg = cv2.imread(tImage)
    lHeight = lImg.shape[0]
    lWidth = lImg.shape[1]
    lMatrix = cv2.getRotationMatrix2D((lWidth//2,  lHeight//2), 90,1)
    lDst = cv2.warpAffine(lImg, lMatrix, ( lHeight, lWidth))
    cv2.imshow('show', lDst)
    cv2.waitKey(0)
    return lDst


def imageRotateByPil(tImage):
    if os.path.exists(tImage) is False:
        print (u"image not exist")
        return
    im = Image.open(tImage)
    im_rotate = im.rotate(90,expand=True)
    # im_rotate.show()
    return  im_rotate


def imageRotateByNumpy(tImage):
    if os.path.exists(tImage) is False:
        print (u"image not exist")
        return
    lImg = cv2.imread(tImage)
    lDst = numpy.rot90(lImg)
    cv2.imshow('show', lDst)
    cv2.waitKey(0)

class MainTest():
    @staticmethod
    def testImageRotate():
        lImge = u"screenshot.png"
        imageRotateByCv(lImge)

    @staticmethod
    def testImageRotateByPil():
        lImge = u"screenshot.png"
        imageRotateByPil(lImge)

    @staticmethod
    def testImageRotateByNumpy():
        lImge = u"screenshot.png"
        imageRotateByNumpy(lImge)



if __name__ == "__main__":
    print os.getcwd()
    # MainTest.testImageRotate()
    # MainTest.testImageRotateByPil()
    MainTest.testImageRotateByNumpy()