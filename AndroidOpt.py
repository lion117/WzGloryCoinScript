# -*- coding: utf-8 -*-

import sys, os, time
import subprocess
import  re
from  dataCfg import  g_adbPath


def tapScreen(x, y, tDevice=None):
    """calculate real x, y according to device resolution."""
    if tDevice is None:
        lCmd = str.format('%s  shell   input tap %d %d ' % (g_adbPath, x, y))
    else:
        lCmd = str.format('%s -s %s shell   input tap %d %d ' % (g_adbPath, tDevice, x, y))
    subprocess.call(lCmd)



def screenShoot( tDevice=None):
    if tDevice is None:
        lShoot = str.format("%s  pull /sdcard/screenshot.png %s " % (g_adbPath, os.getcwd()))
        lCmd1 = str.format("%s shell /system/bin/screencap -p /sdcard/screenshot.png " % (g_adbPath))
    else:
        lShoot = str.format("%s  -s %s pull  /sdcard/screenshot.png %s " % (g_adbPath, tDevice , os.getcwd()))
        lCmd1 = str.format("%s -s %s shell   /system/bin/screencap -p /sdcard/screenshot.png " % (g_adbPath, tDevice))
    subprocess.call(lCmd1)
    subprocess.call(lShoot)


def killWz(tDevice=None):
    lPkg = "com.tencent.tmgp.sgame"
    lPkgSrv = "com.tencent.tmgp.sgame:xg_service_v3"
    if tDevice is None:
        lCmd = str.format('%s shell am force-stop %s' % (g_adbPath, lPkg))
    else:
        lCmd = str.format('%s -s %s shell am force-stop %s' % (g_adbPath, tDevice, lPkg))
    subprocess.call(lCmd)

def closeAndroid(tDevice = None):
    if tDevice is None:
        lCmd = str.format('%s shell reboot -p' % (g_adbPath))
    else:
        lCmd = str.format('%s -s %s shell  reboot -p' % (g_adbPath, tDevice))
    subprocess.call(lCmd)



def getDevices():
    lDvList = []
    lCmd = str.format('%s devices' % (g_adbPath))
    lRet = subprocess.Popen(lCmd,shell=True,stdout=subprocess.PIPE)
    lInfo = lRet.stdout.read()
    lDvList = re.findall(r"127.0.0.1:\d+",lInfo)
    return lDvList










class MainRun():
    @staticmethod
    def testScreenShoot():
        screenShoot()

    @staticmethod
    def testClick():
        tapScreen(733,451)

    @staticmethod
    def runCloseAndroid():
        closeAndroid(None)

#com.tencent.tmgp.sgame

if __name__ == "__main__":

    MainRun.testScreenShoot()
    # MainTest.testClick()
    # fetchEmulatorDevice()
    # MainTest.testAdbDevice()
    # killWz(None)
    # MainRun.runCloseAndroid()