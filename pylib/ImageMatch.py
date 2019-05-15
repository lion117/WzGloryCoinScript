# -*- coding: utf-8 -*-

import os

import cv2
import imutils
import numpy
from PIL import  Image


# # from matplotlib import pyplot as plt
# img = cv2.imread('game.jpg',0)
# img2 = img.copy()
# template = cv2.imread('game_target.jpg',0)
# w, h = template.shape[::-1]
# # All the 6 methods for comparison in a list
# methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
#             'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
#
# for meth in methods:
#     img = img2.copy()
#     method = eval(meth)
#     # Apply template Matching
#     res = cv2.matchTemplate(img,template,method)
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
#     # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
#     if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
#         top_left = min_loc
#     else:
#         top_left = max_loc
#     bottom_right = (top_left[0] + w, top_left[1] + h)
#     cv2.rectangle(img,top_left, bottom_right, 255, 2)
    # plt.subplot(121),plt.imshow(res,cmap = 'gray')
    # plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122),plt.imshow(img,cmap = 'gray')
    # plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    # plt.suptitle(meth)
    # plt.show()


def locateImage(tSrouce, tTarget):
    imgSrc = cv2.imread(tSrouce, 0)
    imgTarget = cv2.imread(tTarget, 0)


    # w, h = imgTarget.shape[::-1]
    # All the 6 methods for comparison in a list
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

    method = eval(methods[0])
    # Apply imgTarget Matching
    res = cv2.matchTemplate(imgSrc, imgTarget, method)


    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val < 0.95:
        print (u"failed to find the image ")
        return (False,0,0)

    data =res.any()
    lTemp  = Image.open(tTarget)
    width , height = lTemp.size
    lx = max_loc[0] + width/2
    ly = max_loc[1] + height/2
    return (True , lx, ly)


def isImageDiffMuch(tImgFirst, tImgSecond):
    if os.path.exists(tImgFirst) is False or os.path.exists(tImgSecond) is False:
        print (u"image is not exist")
        return  (False , -1)

    lMiniArea = 150
    lGrabValue = 80
    lFirst = cv2.imread(tImgFirst, cv2.IMREAD_GRAYSCALE  )
    lSecond = cv2.imread(tImgSecond, cv2.IMREAD_GRAYSCALE )
    lHeight = lFirst.shape[0]
    lWidth = lFirst.shape[1]
    # showImg(lFirst)
    # showImg(lSecond)

    lSecond = adjustImg(lFirst, lSecond)
    # showImg(lFirst)
    # showImg(lSecond)

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    lFirst = cv2.GaussianBlur(lFirst, (21, 21), 0)
    lSecond = cv2.GaussianBlur(lSecond, (21, 21), 0)

    # showImg(lFirst)
    # showImg(lSecond)

    # 图片顺序显示竟然会报错, 这个bug 需要修复
    frameDelta = cv2.absdiff(lFirst, lSecond)
    thresh = cv2.threshold(frameDelta, lGrabValue, 255, cv2.THRESH_BINARY)[1]
    # 扩展阀值图像填充孔洞，然后找到阀值图像上的轮廓
    thresh = cv2.dilate(thresh, None, iterations=2)
    (image, contours, hierarchy) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    # showImg(image)

    lFindDiff =False
    lDiffValue = 0
    for c in contours:
        # if the contour is too small, ignore it
        area = cv2.contourArea(c)
        if area >= lDiffValue:
            lDiffValue = area

        if area < lMiniArea:
            continue
        else:
            lFindDiff = True
    return (lFindDiff , lDiffValue)




def showImg(tImg):
    cv2.imshow("Image",tImg)
    cv2.waitKey(0)


def adjustImg(lFirst, lSecond):

    lHeight = lFirst.shape[0]
    lWidth = lFirst.shape[1]

    lHeight1 = lSecond.shape[0]
    lWidth1 = lSecond.shape[1]

    if lHeight  <=  lWidth and lHeight1 <=  lWidth1 :
        lSecond = imutils.resize(lSecond, width=lWidth, height=lHeight)

    elif lHeight  >=  lWidth and lHeight1 >=  lWidth1 :
        lSecond = imutils.resize(lSecond, width=lWidth, height=lHeight)

    else:
        # 图片旋转无法自适应, 图片旋转顺序出现较大问题, 需要续费
        lSecond = imutils.rotate(lSecond, angle= -90)
        # lSecond= numpy.rot90(lSecond)
        # lSecond = imutils.resize(lSecond, width=lWidth, height=lHeight)

    return  lSecond



class MainTest():
    @staticmethod
    def testLocateImage():
        lSrc = u"game.png"
        lTarget  = u"img/continue.png"
        print locateImage(lSrc, lTarget)

    @staticmethod
    def testFindImgfromImg():
        from image import imagecompare
        lSrc = u"game2.png"
        lTarget  = u"img/icon.png"
        print imagecompare.FindImgFromImg(lSrc, lTarget)

    @staticmethod
    def testFindDiff():
        lFirst = u"template.png"
        lSecond = u"game2.png"
        print isImageDiffMuch(lFirst, lSecond)

if __name__ == "__main__":
    print os.getcwd()
    # MainTest.testLocateImage()
    # MainTest.testFindImgfromImg()
    MainTest.testFindDiff()