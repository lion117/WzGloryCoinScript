# -*- coding: utf-8 -*-

import sys, os, time
import subprocess
import  re

g_exeDevice = 'D:\\program_test\\yeshen\\Nox\\bin\\nox_adb.exe'

def tapScreen(x, y, tDevice=None):
    """calculate real x, y according to device resolution."""
    if tDevice is None:
        lCmd = str.format('%s  shell   input tap %d %d ' % (g_exeDevice, x, y))
    else:
        lCmd = str.format('%s -s %s shell   input tap %d %d ' % (g_exeDevice, tDevice, x, y))
    subprocess.call(lCmd)


def clickScreen():
    lCmd = str.format('%s shell  input tap %d %d '%(g_exeDevice, 300,400 ))
    subprocess.call(lCmd)


def screenShoot( tDevice=None):
    if tDevice is None:
        lShoot = str.format("%s  pull /sdcard/screenshot.png %s "%(g_exeDevice, os.getcwd()))
        lCmd1 = str.format("%s shell /system/bin/screencap -p /sdcard/screenshot.png "%(g_exeDevice))
    else:
        lShoot = str.format("%s  -s %s pull  /sdcard/screenshot.png %s "%(g_exeDevice,tDevice ,os.getcwd()))
        lCmd1 = str.format("%s -s %s shell   /system/bin/screencap -p /sdcard/screenshot.png "%(g_exeDevice,tDevice))
    subprocess.call(lCmd1)
    subprocess.call(lShoot)

def fetchEmulatorDevice():
    lCmd = str.format('%s devices'%(g_exeDevice))
    lRet = subprocess.Popen(lCmd,shell=True,stdout=subprocess.PIPE)
    lInfo = lRet.stdout.read()
    lDvList = parseDevices(lInfo)
    return lDvList

def parseDevices(tInfo):
    if len(tInfo) == 0 :
        return  []

    lRet = re.findall(r"127.0.0.1:\d+",tInfo)
    return  lRet

def killWz(tDevice=None):
    lPkg = "com.tencent.tmgp.sgame"
    lPkgSrv = "com.tencent.tmgp.sgame:xg_service_v3"
    if tDevice is None:
        lCmd = str.format('%s shell am force-stop %s'%(g_exeDevice,lPkg))
    else:
        lCmd = str.format('%s -s %s shell am force-stop %s'%(g_exeDevice, tDevice,lPkg))
    subprocess.call(lCmd)

def closeAndroid(tDevice):
    if tDevice is None:
        lCmd = str.format('%s shell reboot -p' % (g_exeDevice))
    else:
        lCmd = str.format('%s -s %s shell  reboot -p' % (g_exeDevice, tDevice))
    subprocess.call(lCmd)

class MainRun():
    @staticmethod
    def testScreenShoot():
        screenShoot()

    @staticmethod
    def testClick():
        tapScreen(733,451)

    @staticmethod
    def testAdbDevice():
        lList =  fetchEmulatorDevice()
        if len(lList) > 0:
            tapScreen(0,0,lList[0])
            screenShoot(lList[0])
    @staticmethod
    def runCloseAndroid():
        closeAndroid(None)

#com.tencent.tmgp.sgame

if __name__ == "__main__":
    print os.getcwd()
    MainRun.testScreenShoot()
    # MainTest.testClick()
    # fetchEmulatorDevice()
    # MainTest.testAdbDevice()
    # killWz(None)
    # MainRun.runCloseAndroid()