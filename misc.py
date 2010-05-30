#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, math, pango, gtk, gtk.glade
import threading, imp, sys
from interfaces import keyboard, wiimote
from time import time as gettime
Semaphore = threading.Semaphore

sys.path.append(os.path.abspath('.')+'/interfaces')

try:
    import pygtk
except:
    sys.stderr.write("ERROR: Module pygtk-2.0 not found.\n")
    sys.exit(1)

class FighterNames(object):
    def __init__(self, blue="Convidado",red="Convidado"):
        gladefile = "gui/fighternames.glade"
        mainWindow = gtk.glade.XML(gladefile,"main")
        self.blue = blue
        self.red = red

        self.w_mainWindow = mainWindow.get_widget("main")
        self.c_blue = mainWindow.get_widget("c_fighterblue")
        self.c_red = mainWindow.get_widget("c_fighterred")

    def run(self):
        result = self.w_mainWindow.run()

        # Usuario selecionou OK
        if result == 0:
            self.blue = self.c_blue.get_active_text() or "Convidado"
            self.red = self.c_red.get_active_text() or "Convidado"
        self.w_mainWindow.destroy()
        return self.blue,self.red

