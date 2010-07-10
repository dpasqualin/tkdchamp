#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import pygtk
    pygtk.require("2.0")
except:
    sys.stderr.write("ERROR: Module pygtk-2.0 not found.\n")
    sys.exit(1)

try:
    import gtk, gtk.glade
except:
    sys.stderr.write("ERROR: Module python-gtk not found.\n")
    sys.exit(1)

# Show window with a info message
def infoDlg(message):
    """ Show a info dialog """
    info_dlg  = gtk.MessageDialog(type = gtk.MESSAGE_INFO
                                , message_format = message
                                , buttons = gtk.BUTTONS_OK)
    result = info_dlg.run()
    info_dlg.destroy()
    return result

# Show window with a error message
def errorDlg(message):
    """ Show a error dialog """
    error_dlg = gtk.MessageDialog(type = gtk.MESSAGE_ERROR
                              , message_format = message
                              , buttons = gtk.BUTTONS_OK)
    error_dlg.run()
    error_dlg.destroy()

class GUI(object):
    def __init__(self, wiimoteCtrl):

        gladefile = 'gtk.glade'
        MWindow = gtk.glade.XML(gladefile, 'main')

        signals = { 'on_bu_connect_clicked' : self.connectWiimote }
        MWindow.signal_autoconnect(signals)
        w_MWindow = MWindow.get_widget('main')

        self.h_box_not_sensitive = []
        for i in ['2', '3', '4']:
            self.h_box_not_sensitive.append(MWindow.get_widget("hbox"+i))

        self.wmdict = {1:None,2:None,3:None,4:None}

        result = w_MWindow.run()
        w_MWindow.destroy()

    def connectWiimote(self, widget):

        # Connect controller
        try:
            msg = "Clique em OK e mantenha pressionado simultaneamente os "
            msg += "botões 1 e 2 do wiimote que deseja associar ao juiz."
            infoDlg(msg)
            wm = wiimoteCtrl.connect()
        except:
            msg = "Ocorreu um erro enquanto o emparelhamento era feito, "
            msg += "tente novamente ou clique em cancelar para sair."
            errorDlg(msg)
            return False

        # Set next hbox as sensitive
        self.h_box_not_sensitive.pop(0).set_sensitive(True)
