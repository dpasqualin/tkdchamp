#!/usr/bin/env python
# -*- coding: utf-8 -*-

sys.path.append(os.path.abspath('.')+'/interfaces')
sys.path.append("../../")

import os, math, pango, gtk, gtk.glade
import imp, sys
from interfaces import keyboard, wiimote
from time import time as gettime
from misc import Fighter

try:
    import pygtk
    pygtk.require("2.0")
except:
    sys.stderr.write("ERROR: Module pygtk-2.0 not found.\n")
    sys.exit(1)

class GUI(object):

    def __init__(self, eventManager=None):
        gladefile = 'glade/tkd.glade'
        self.Main_Window = gtk.glade.XML(gladefile, 'main')

        w_Main_Window = self.Main_Window.get_widget('main')
        w_Main_Window.show_all()

        buttons = { "on_main_destroy" : self.quit,
                    "on_newgame_activate": self.newGame,
                    "on_halfFaultToBlue":self.gothalfFaultToBlue,
                    "on_b_f1f_clicked":self.gotFaultToBlue,
                    "on_b_f2mf_clicked":self.gotHaldFaultToRed,
                    "on_b_f2f_clicked":self.gotFaultToRed,
                  }

        self.Main_Window.signal_autoconnect(buttons)

        # Connect widgets
        # Label to show points
        self.l_f1p = self.Main_Window.get_widget('l_f1p')
        self.l_f2p = self.Main_Window.get_widget('l_f2p')

        # Label to show faults
        self.l_f1mf = self.Main_Window.get_widget('l_f1mf')
        self.l_f1f = self.Main_Window.get_widget('l_f1f')
        self.l_f2mf = self.Main_Window.get_widget('l_f2mf')
        self.l_f2f = self.Main_Window.get_widget('l_f2f')

        # Necessary to draw in blue/red the boxes
        ebox_blue = self.Main_Window.get_widget('ebox_blue')
        ebox_red = self.Main_Window.get_widget('ebox_red')

        # Set background color in points boxes
        ebox_blue.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("blue"))
        ebox_red.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("red"))

        # Buttons to compute faults
        b_f1mf = self.Main_Window.get_widget('b_f1mf')
        b_f1f = self.Main_Window.get_widget('b_f1f')
        b_f2mf = self.Main_Window.get_widget('b_f2mf')
        b_f2f = self.Main_Window.get_widget('b_f2f')

        # Fighter's names
        self.l_blue_name = self.Main_Window.get_widget("l_fighter_blue_name")
        self.l_red_name = self.Main_Window.get_widget("l_fighter_red_name")

        self.interfaces = self.getInterfaces()

        # Menu item 'interface selecion'
        menu_is = self.Main_Window.get_widget('menu_is')

        self.__createInterfacesMenu(menu_is)

        self.__eventManager = eventManager

    def __createInterfacesMenu(self,menu):
        group = gtk.RadioMenuItem()
        for i in self.interfaces:
            self.__appendItemToMenu(menu,group,i)

    def __appendItemToMenu(self, menu, group, title):
        item = gtk.RadioMenuItem(group=group, label=title)
        item.set_name(title)
        item.connect("activate", self.setInterface)
        item.show()
        menu.append(item)

    def getInterfaces(self):
        dir_interfaces = "interfaces"
        interfaces = {}

        interfacesList = [ os.path.splitext(fname)[0]
        for fname in os.listdir(dir_interfaces)
        if os.path.splitext(fname)[1] ==".py" and fname[0] != '_' and
            fname != 'common.py' ]

        for filepath in interfacesList:
            filepath = os.path.join(dir_interfaces, filepath)
            fp, path, desc = imp.find_module(filepath)
            try:
                interface = imp.load_module(filepath, fp, path, desc)
            finally:
                if fp: fp.close()

            # Add the new interface
            interfaces[interface.NAME] = { 'module':interface }

        return interfaces

    def setInterface(self, ikey):
        interface = self.interfaces[ikey.name]['module']
        self.interface = interface.Interface(self)
        self.interface.configure()

    def newGame(self, widget):
        """ User choose to start a new game """
        self.__zeroPoints()
        self.__zeroFaults()
        bname,rname = FighterNames().run()
        blue = Fighter(bname)
        red = Fighter(rname)
        self.__runEvent(self.newGame,blue,red)

    def writeInfo(self,blue,red):
        """ Receive a Fighter class for blue and red fighters and print
        info about it """
        self.l_blue_name.set_text("<b>"+blue.getName()+"</b>")
        self.l_red_name.set_text("<b>"+red.getName()+"</b>")
        self.l_blue_name.set_use_markup(True)
        self.l_red_name.set_use_markup(True)

    def setTextPointToBlue(self, n):
        msg = '<span foreground="white" size="200000">%s</span>'%n
        self.l_f1p.set_label(msg)

    def setTextPointToRed(self, n):
        msg = '<span foreground="white" size="200000">%s</span>'%n
        self.l_f2p.set_label(msg)

    def setHalfFaultToBlue(self,n):
        self.l_f1mf.set_text(str(n))

    def setHalfFaultToRed(self, n):
        self.l_f2mf.set_text(str(n))

    def setFaultToBlue(self, n):
        self.l_f1f.set_text(str(n))

    def setFaultToRed(self, n):
        self.l_f2f.set_text(str(n))

    def gotHalfFaultToBlue(self, widget):
        self.__runEvent(self.gotHalfFaultToBlue)

    def gotHalfFaultToRed(self, widget):
        self.__runEvent(self.gotHalfFaultToRed)

    def gotFaultToBlue(self, widget):
        self.__runEvent(self.gotFaultToBlue)

    def gotFaultToRed(self, widget):
        self.__runEvent(self.gotFaultToRed)

    def __zeroPoints(self):
        self.setTextPoint(self.l_f1p, "0")
        self.setTextPoint(self.l_f2p, "0")

    def __zeroFaults(self):
        self.l_f1mf.set_text("0")
        self.l_f1f.set_text("0")
        self.l_f2mf.set_text("0")
        self.l_f2f.set_text("0")

    def quit(self, widget):
        try: self.interface.t_quit = True
        except: pass
        gtk.main_quit()

    def __runEvent(self,event, **args=None):
        if self.__eventManager:
            self.__eventManager.runEvent(event,args)


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




if __name__ == "__main__":
    gtk.gdk.threads_init()
    gtk.gdk.threads_enter()
    fight = Fight()
    gtk.gdk.threads_leave()
    gtk.main()
