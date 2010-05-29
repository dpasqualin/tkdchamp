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

# Show window with a error message
def errorDlg(message):
    """ Show a error dialog """
    error_dlg = gtk.MessageDialog(type = gtk.MESSAGE_ERROR
                              , message_format = message
                              , buttons = gtk.BUTTONS_OK)
    error_dlg.run()
    error_dlg.destroy()

# Show window with a question message
def questionDlg(message):
    """ Show a question dialog and return a gtk.RESPONSE """
    question_dlg = gtk.MessageDialog(type = gtk.MESSAGE_QUESTION
                              , message_format = message
                              , buttons = gtk.BUTTONS_YES_NO)
    result = question_dlg.run()
    question_dlg.destroy()
    return result

# Show window with a info message
def infoDlg(message):
    """ Show a info dialog """
    info_dlg  = gtk.MessageDialog(type = gtk.MESSAGE_INFO
                                , message_format = message
                                , buttons = gtk.BUTTONS_OK)
    result = info_dlg.run()
    info_dlg.destroy()
    return result

# Show window with a warning message
def warningDlg(message):
    """ Show a info dialog """
    info_dlg  = gtk.MessageDialog(type = gtk.MESSAGE_WARNING
                                , message_format = message
                                , buttons = gtk.BUTTONS_OK)
    result = info_dlg.run()
    info_dlg.destroy()
    return result
