# -*- coding: utf-8 -*-

import sys, os, time
# sys.path.insert(0,os.path.dirname(os.getcwd()))

import  AndroidOpt
import cv2
import  numpy


import pylib.ImageDealing
import pylib.ImageMatch
from  pylib.SiftMatch import findMatchImgXY




class Main():
    @classmethod
    def hello(cls):
        print("hello world")
    @classmethod
    def run(cls):
        lTartget = u"feature0.png"
        lScreenShoot = u"screenshot.png"
        # lTargetList = [u"feature0.png" , u"feature1.png",u"feature3.png",u"feature4.png",u"feature5.png"]
        lTargetList = [u"feature0.png", u"feature2.png", u"feature3.png", u"feature4.png", u"feature5.png",u"feature6.png",u"feature7.png",u"feature8.png"]

        lIndex = 0
        print (u"begin")
        lLastTick = 0
        while True:
            lDev = Main.getAndroidDevice()[0]
            AndroidOpt.screenShoot(lDev)
            if os.path.exists(lScreenShoot) is False:
                print(u"screen shoot error")
                break
            # Main.rotate(lScreenShoot)
            lRet, lx, ly = False, 0, 0
            for itor in lTargetList:
                ltemp = u"img/" + itor
                itor = os.path.join(os.getcwd(),ltemp)
                try:
                    (lRet, lx, ly) = findMatchImgXY(itor, lScreenShoot)
                    if lRet is False:
                        time.sleep(1)
                        print (u"current times %d  skip diff " % (lIndex))
                        continue
                    else:
                        Main.matchTarget(itor, lScreenShoot, lDev, lx, ly)

                except Exception, exInfo:
                    print (u"excepiton %s" % (exInfo))
                    continue

        print (u"done %d" % (lIndex))

    # @staticmethod
    # def rotate(tBigImg):
    #     lImge =  image.ImageDealing.imageRotateByPil(tBigImg)
    #     lImge.save(tBigImg)

    @classmethod
    def matchTarget(cls, tTagertImg, tScreenShoot, tDev, tx, ty):
        tTagertImg = os.path.basename(tTagertImg)
        if tTagertImg == u"feature2.png":
            print(u"found target %s" % (tTagertImg))
            lSrcImg = cv2.imread(tScreenShoot)
            lX0, lY0 = tx - 30, ty - 30
            lX1, lY1 = tx + 30, ty + 30
            lCutImg = lSrcImg[lY0:lY1, lX0:lX1]
            lMean = Main.calAverage(lCutImg)
            if lMean < 150:
                AndroidOpt.tapScreen(tx - 5, ty, tDevice=tDev)
                time.sleep(2)
                print(u"click target %s" % (tTagertImg))
                return True
            else:
                print(u"not fit target %s" % (tTagertImg))
                return False

        elif tTagertImg == u"feature3.png":
            print(u"found target %s" % (tTagertImg))
            AndroidOpt.tapScreen(tx, ty, tDevice=tDev)
            time.sleep(2)
            Main.btnSkipAutoClick(tTagertImg, tScreenShoot, tDev)

        else:
            print(u"found target %s" % (tTagertImg))
            AndroidOpt.tapScreen(tx, ty, tDevice=tDev)
            time.sleep(2)

    @classmethod
    def btnSkipAutoClick(cls, tTagertImg, tScreenShoot, tDev):
        while (True):
            try:
                (lRet, lx, ly) = findMatchImgXY(tTagertImg, tScreenShoot)
            except Exception, exInfo:
                print (u"excepiton %s" % (exInfo))
                break
            if lRet is False:
                time.sleep(1)
                # print (u"current times %d  skip diff " % (lIndex))
                break
            else:
                print(u"find jump again")
                AndroidOpt.tapScreen(lx, ly, tDevice=tDev)
                time.sleep(2)

    @classmethod
    def calAverage(cls, tSrc):
        try:
            mean = cv2.mean(cv2.split(tSrc)[0])[0]
            print mean
            return mean
        except Exception, e:
            return 0

    @classmethod
    def getAndroidDevice(cls):
        lDvList = AndroidOpt.getDevices()
        lSize = len(lDvList)
        return  lDvList




if __name__ == "__main__":
    Main.hello()
    Main.run()
    # Main.getAndroidDevice()