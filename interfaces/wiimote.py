#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cwiid
from time import sleep
from threading import Thread
import gtk,gtk.glade
import common

NAME = 'Wiimote'

class Interface(object):
    def __init__(self, fight):
        self.n_of_judges = 0
        self.fight = fight
        self.t_quit = False

    def configure(self):

        gladefile = 'interfaces/wiimote.glade'
        MWindow = gtk.glade.XML(gladefile, 'main')

        signals = { 'on_bu_connect_clicked' : self.connect_wiimote }
        MWindow.signal_autoconnect(signals)
        w_MWindow = MWindow.get_widget('main')

        self.h_box_not_sensitive = []
        for i in ['2', '3', '4']:
            self.h_box_not_sensitive.append(MWindow.get_widget("hbox"+i))

        self.wmdict = {1:None,2:None,3:None,4:None}

        result = w_MWindow.run()
        w_MWindow.destroy()


    def connect_wiimote(self, widget):

        # Connect controller
        try:
            msg = "Clique em OK e mantenha pressionado simultaneamente os "
            msg += "botões 1 e 2 do wiimote que deseja associar ao juiz."
            common.infoDlg(msg)
            wm = cwiid.Wiimote()
        except:
            msg = "Ocorreu um erro enquanto o emparelhamento era feito, "
            msg += "tente novamente ou clique em cancelar para sair."
            common.errorDlg(msg)
            return False

        wm.enable(cwiid.FLAG_MESG_IFC|cwiid.FLAG_NONBLOCK)
        wm.rpt_mode = cwiid.RPT_BTN

        # Add number of judges
        self.n_of_judges += 1

        # Add controller to dict
        self.wmdict[self.n_of_judges] = wm

        # Set wiimote led
        wm.led = getattr(cwiid,'LED'+str(self.n_of_judges)+'_ON')

        # Set next hbox as sensitive
        self.h_box_not_sensitive.pop(0).set_sensitive(True)

        # Start monitor
        Thread(target=self.event_grab, args=[wm,self.n_of_judges]).start()

    def event_grab(self,wiimote, judge):
        messages=[]
        while not self.t_quit:
            messages = wiimote.get_mesg()
            if messages:
                for message in messages:
                    if message[1] & cwiid.BTN_1:
                        self.fight.point_control(judge,1)
                    if message[1] & cwiid.BTN_2:
                        self.fight.point_control(judge,2)
            sleep(0.1)
