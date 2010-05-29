#!/usr/bin/env python

import sys, gtk, gtk.glade
try:
    import pygtk
    pygtk.require("2.0")
except:
    sys.stderr.write("ERROR: Module pygtk-2.0 not found.\n")
    sys.exit(1)

NAME = 'Teclado'

class Interface(object):

    def __init__(self, fight):
        self.map = {}
        self.fight = fight
        self.n_of_judges = 0

    def configure(self):
        gladefile = 'interfaces/keyboard.glade'
        MWindow = gtk.glade.XML(gladefile, 'main')

        signals = { 'on_field_key_press_event' : self.diag_key_grab }
        MWindow.signal_autoconnect(signals)

        w_MWindow = MWindow.get_widget('main')

        fields = {}
        for j in [1, 2, 3, 4]:
            fields[j] = {1:MWindow.get_widget('%d:1'%j),
                         2:MWindow.get_widget('%d:2'%j)}

        ok = False
        while not ok:
            result = w_MWindow.run()

            # O usuario selecionou OK
            if result == 0:
                for j in [1, 2, 3, 4]:
                    # TODO: identificar teclas repetidas para arbitros
                    # diferentes
                    if fields[j][1].get_text() != '':
                        if fields[j][2].get_text() != '':
                            self.n_of_judges += 1
                        else:
                            break
                if self.n_of_judges == 0:
                    continue
                else:
                    ok = True
            # O usuario selecionou Cancelar
            elif result == 1:
                ok = True
            # Usuario clicou em Limpar
            elif result == 2:
                self._clean_entries(fields)

        # Conecta sinal de tecla pressionado na janela principal ao
        # tratador de eventos
        if result == 0:
            signals = {'on_main_key_press_event': self.event_grab }
            self.fight.Main_Window.signal_autoconnect(signals)

        w_MWindow.destroy()
        return result

    def _clean_entries(self,entries):
        for item in entries.values():
            item[1].set_text('')
            item[2].set_text('')

    def diag_key_grab(self, field, event):
        wid_name = field.name
        judge = int(wid_name.split(':')[0])
        fighter = int(wid_name.split(':')[1])
        key = event.string
        self.map[key] = {'f':fighter, 'j': judge}

    def event_grab(self, x, event):
        key = event.string
        if self.map.has_key(key):
            f = self.map[key]['f']
            j = self.map[key]['j']
            self.fight.point_control(j, f)

