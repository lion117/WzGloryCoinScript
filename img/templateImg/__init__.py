# -*- coding: utf-8 -*-

import sys, os, time
import cv2, numpy


class MainRun():
    _curDir = os.getcwd()
    _tarDir = os.path.dirname(os.path.dirname(_curDir))
    _img = os.path.join(_tarDir, u"ShareMedia/Images/cat0_gray.jpg")

    @classmethod
    def runTest(cls):
        print(u"hello world")


if __name__ == "__main__":
    MainRun.runTest()