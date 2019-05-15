# -*- coding: utf-8 -*-

import sys, os, time
from AndroidOpt import  screenShoot


class MainRun():
    @classmethod
    def runTest(cls):
        print(u"hello world")

    @classmethod
    def shootScreen(cls):
        screenShoot(None)


if __name__ == "__main__":
    MainRun.runTest()
    MainRun.shootScreen()