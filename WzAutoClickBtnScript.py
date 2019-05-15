# -*- coding: utf-8 -*-
import shutil
import sys, os, time
lParentDir = os.path.dirname(os.getcwd())
sys.path.insert(0,lParentDir)

import  AndroidOpt
import image.ImgFeature.ImageRotate
from image.ImgFeature.ImageMatch import isImageDiffMuch
from image.ImgFeature.SiftMatch import findMatchImgXY

g_ticks =0
g_LastScreenShot = u"LastSceenshot.png"
g_ScreenShoot = u"screenshot.png"


class DeviceTimeoutMgr():
    global g_LastScreenShot,g_ScreenShoot
    _deviceMap = {}
    _timeout = 5*60
    @classmethod
    def isDeviceDead(cls,tDevice):
        if tDevice is None:
            tDevice = "default"
        if len(cls._deviceMap) == 0:  # add new device image
            cls._deviceMap[str(tDevice)] =  time.time()
            return  False
        if cls._deviceMap.has_key(str(tDevice)):
            (lRet , lValue)=isImageDiffMuch(g_ScreenShoot, g_LastScreenShot)
            if lRet is True: # image changed
                cls._deviceMap[str(tDevice)] =  time.time()
            else: # image no changed , asjust timeout
                lTimeDiff = time.time() - cls._deviceMap[str(tDevice)]
                if lTimeDiff > cls._timeout:
                    print(u"time out %d"%(lTimeDiff))
                    return  True
                else:
                    print(u"time run %d"%(lTimeDiff))
                    return False
        return  False


class Main():

    @classmethod
    def run(cls):
        global  g_ticks ,g_ScreenShoot
        lTartget = u"feature0.png"
        lJumpImg = u"skip.png"
        lIndex = 0
        print (u"begin")
        while True:
            g_ticks +=1
            # Main.isTimeToKill(g_ticks)
            lDevice = Main.getAndroidDevice()
            AndroidOpt.screenShoot(tDevice=lDevice)
            if os.path.exists(g_ScreenShoot) is False:
                print(u"screen shoot error")
                break

            Main.rotate(g_ScreenShoot)
            (lRet, lx, ly)  = findMatchImgXY(lTartget, g_ScreenShoot)
            if lRet is False:
                (lRet1, lx1, ly1)  = findMatchImgXY(lJumpImg, g_ScreenShoot)
                if lRet1 is False:
                    time.sleep(2)
                    print (u"current times %d  not found target image device:%s "%( lIndex,lDevice))
                    # Main.isTimeToKill(lDevice)
                    # Main.makeCopy(g_ScreenShoot, g_LastScreenShot)
                    continue
                else:
                    AndroidOpt.tapScreen(lx1, ly1,tDevice=lDevice)
                    print (u"current times %d  skip button device:%s "%( lIndex,lDevice))
                    time.sleep(10)
                    continue
            else:
                AndroidOpt.tapScreen(lx, ly,tDevice=lDevice)
                time.sleep(2)
                lIndex +=1
                print (u" %d Times device:%s"%(lIndex,lDevice))

        print (u"done %d"%(lIndex))

    @classmethod
    def getAndroidDevice(cls):
        lDvList = AndroidOpt.fetchEmulatorDevice()
        lSize = len(lDvList)
        if lSize <2:
            return None
        else:
            lIndex = g_ticks % lSize
            return lDvList[lIndex]



    @classmethod
    def rotate(cls,tBigImg):
        lImge =  image.ImageDealing.imageRotateByPil(tBigImg)
        lImge.save(tBigImg)

    @classmethod
    def isTimeToKill(cls, tDevice):
        if DeviceTimeoutMgr.isDeviceDead(tDevice= tDevice):
            AndroidOpt.killWz(tDevice)
            print(u"kill device program as time out %s"%(tDevice))
            return  True
        else:
            return  False

    @staticmethod
    def makeCopy( tSrc , tDest):
        if os.path.exists(tSrc) :
            shutil.copyfile(tSrc, tDest)



class MainTest():
    @staticmethod
    def testPrint():
        pass

if __name__ == "__main__":
    print os.getcwd()
    Main.run()
