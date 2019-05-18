# -*- coding: utf-8 -*-

import sys, os, time
sys.path.insert(0,os.path.dirname(os.getcwd()))

import  AndroidOpt
import image.ImageDealing
import image.ImageMatch
from  image.SiftMatch import findMatchImgXY
import cv2

class Main():
    @classmethod
    def run(cls):
        lTartget = u"feature0.png"
        lScreenShoot = u"screenshot.png"
        # lTargetList = [u"feature0.png" , u"feature1.png",u"feature3.png",u"feature4.png",u"feature5.png"]
        lTargetList = [u"feature0.png" ,u"feature2.png",u"feature3.png",u"feature4.png",u"feature5.png"]
        # lTargetList = [u"feature2.png"]


        lIndex = 0
        print (u"begin")
        lLastTick = 0
        while True:
            lDev = Main.getAndroidDevice()[0]
            AndroidOpt.screenShoot(lDev)
            if os.path.exists(lScreenShoot) is False:
                print(u"screen shoot error")
                break

            Main.rotate(lScreenShoot)

            lRet, lx, ly = False, 0 ,0


            for itor in lTargetList:
                try:
                    (lRet, lx, ly)  = findMatchImgXY(itor,lScreenShoot)
                except Exception,exInfo:
                    print (u"excepiton %s"%(exInfo))
                    continue
                if lRet is False:
                    time.sleep(1)
                    print (u"current times %d  skip diff "%( lIndex))
                    continue
                else:
                    if itor == u"feature2.png" :
                        lSrcImg = cv2.imread(lScreenShoot)
                        lX0 , lY0= lx-30, ly-30
                        lX1, lY1 = lx+30,ly+30
                        lCutImg = lSrcImg[lY0:lY1, lX0:lX1]
                        lMean = Main.calAverage(lCutImg)
                        if lMean < 150:
                            AndroidOpt.tapScreen(lx-5, ly,tDevice=lDev)
                            time.sleep(2)
                            print(u"++++")
                            continue
                        else:
                            print(u"----")
                            continue
                    elif itor == u"feature0.png":
                        lIndex +=1
                    elif itor == u"feature3.png":
                        print(u"find jump first")
                        AndroidOpt.tapScreen(lx, ly,tDevice=lDev)
                        time.sleep(2)
                        while(True):
                            try:
                                (lRet, lx, ly) = findMatchImgXY(itor, lScreenShoot)
                            except Exception, exInfo:
                                print (u"excepiton %s" % (exInfo))
                                break
                            if lRet is False:
                                time.sleep(1)
                                print (u"current times %d  skip diff " % (lIndex))
                                break
                            else:
                                print(u"find jump again")
                                AndroidOpt.tapScreen(lx, ly,tDevice=lDev)
                                time.sleep(2)



                    AndroidOpt.tapScreen(lx, ly,tDevice=lDev)
                    time.sleep(2)

                print (u" %d Times"%(lIndex))

        print (u"done %d"%(lIndex))



    @staticmethod
    def rotate(tBigImg):
        lImge =  image.ImageDealing.imageRotateByPil(tBigImg)
        lImge.save(tBigImg)


    @classmethod
    def calAverage(cls,tSrc):
        try:
            mean = cv2.mean(cv2.split(tSrc)[0])[0]
            print mean
            return mean
        except Exception,e:
            return 0

    @classmethod
    def getAndroidDevice(cls):
        lDvList = AndroidOpt.fetchEmulatorDevice()
        lSize = len(lDvList)
        return  lDvList



if __name__ == "__main__":
    print os.getcwd()
    Main.run()