#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../../")
from misc import Judge

import cwiid
from time import sleep
from threading import Thread
from gui import gtk

NAME = 'Wiimote'

class Interface(object):
    def __init__(self, pointCounter, blueFighter, redFighter):
        self.__pointCounter = pointCounter
        self.__bFighter = blueFighter
        self.__rFighter = rFighter
        self.t_quit = False
        self.__judges = {}

    def configure(self):
        gtk.GUI()

    def connect(self):
        """ Connect to a wiimote """

        try:
            wm = cwiid.Wiimote()
        except:
            raise

        wm.enable(cwiid.FLAG_MESG_IFC|cwiid.FLAG_NONBLOCK)
        wm.rpt_mode = cwiid.RPT_BTN

        # Add number of judges
        judge = Judge(self.__pointCounter.getNJudge()+1)
        self.__pointCounter.addJudge(judge)

        self.__judges[judge] = wm

        # Set wiimote led
        wm.led = getattr(cwiid,'LED'+str(len(self.__judges))+'_ON')

        # Start monitor
        Thread(target=self.__eventGrab, args=[wm,len(self.__judges)]).start()

    def __eventGrab(self,wiimote, judge):
        messages=[]
        while not self.t_quit:
            messages = wiimote.get_mesg()
            if messages:
                for message in messages:
                    if message[1] & cwiid.BTN_1:
                        self.__pointCounter.judgeSignal(judge,
                            self.__bFighter)
                    if message[1] & cwiid.BTN_2:
                        self.__pointCounter(judge,
                            self.__rFighter)
            sleep(0.05)
