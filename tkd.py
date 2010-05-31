#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, math, pango, gtk, gtk.glade
import threading, imp, sys
from interfaces import keyboard, wiimote
from time import time as gettime
from misc import FighterNames
Semaphore = threading.Semaphore

sys.path.append(os.path.abspath('.')+'/interfaces')

try:
    import pygtk
    pygtk.require("2.0")
except:
    sys.stderr.write("ERROR: Module pygtk-2.0 not found.\n")
    sys.exit(1)

class PointCounter(object):
    """ Contador de pontos.
            fight: luta para controlar
            n_of_judge: numero de juizes """
    def __init__(self, fight, n_of_judge=0):
        self.n_of_judge = n_of_judge
        self.Fight = fight
        self.sem = Semaphore(1)
        self.stopcounting = True

        # Intervalo de tempo aceitável entre comandos de juizes diferentes
        # Caso esse tempo seja excedido o ponto não é contabilizado
        self.timeout = 1.3 # X segundos

        # control list of fight
        # fighter:{list_of_judges,first entry time}
        self.flist = {1:{'j':[],'t':0}, 2:{'j':[],'t':0}}

    def set_number_of_judge(self,n):
        """ Adiciona um novo juiz ao jogo """
        self.n_of_judge = n

    def stop_counting(self):
        """ Quando uma luta acabou, nao eh mais preciso fazer
            contagem de pontos """
        self.stopcounting = True

    def start_counting(self):
        self.stopcounting = False

    def point_control(self, j, f):
        """Responsável por descobrir quando aconteceu um ponto, de acordo
        com a quantidade de juízes que estão de acordo com o mesmo """

        if self.stopcounting == True or self.n_of_judge == 0:
            return True

        # Descobre o momento em que o clique ocorreu
        time = gettime()

        # Calcula numero de juizes necessarios para que o ponto seja valido
        j_to_ok = int(math.log(self.n_of_judge,2))+1

        self.sem.acquire()

        # Se jogada eh valida
        if j not in self.flist[f]['j']:

            if self.flist[f]['t'] == 0:
                self.flist[f]['t'] = time

            self.flist[f]['j'].append(j)

            # Se nao estourou tempo limite...
            if time - self.flist[f]['t'] <= self.timeout:
                # Se o numero necessario de juizes foi atingido, ponto
                # para o lutador f!
                if len(self.flist[f]['j']) >= j_to_ok:
                    self.Fight.point_to(f)
                    self.flist[f]['j'] = []
                    self.flist[f]['t'] = 0
                else:
                    self.flist[f]['j'].append(j)
            # Se o tempo limite estourou considera esse como outro ponto
            else:
                self.flist[f]['j'] = [j]
                self.flist[f]['t'] = time

        self.sem.release()


class Fight(object):

    def __init__(self):
        gladefile = 'gui/tkd.glade'
        self.Main_Window = gtk.glade.XML(gladefile, 'main')

        w_Main_Window = self.Main_Window.get_widget('main')
        w_Main_Window.show_all()

        buttons = { "on_main_destroy" : self.quit,
                    "on_newgame_activate": self.new_game,
                    "on_b_f1mf_clicked":self.b_f1mf_clicked,
                    "on_b_f1f_clicked":self.b_f1f_clicked,
                    "on_b_f2mf_clicked":self.b_f2mf_clicked,
                    "on_b_f2f_clicked":self.b_f2f_clicked,
               }

        self.Main_Window.signal_autoconnect(buttons)

        # Semaforo para escrita de pontos dos lutadores
        # Necessario porque podem haver pontos e faltas ao mesmo tempo
        self.sem_points = Semaphore(1)

        # Connect widgets
        # Label de escrita dos pontos
        self.l_f1p = self.Main_Window.get_widget('l_f1p')
        self.l_f2p = self.Main_Window.get_widget('l_f2p')

        # Label de escrita das faltas
        self.l_f1mf = self.Main_Window.get_widget('l_f1mf')
        self.l_f1f = self.Main_Window.get_widget('l_f1f')
        self.l_f2mf = self.Main_Window.get_widget('l_f2mf')
        self.l_f2f = self.Main_Window.get_widget('l_f2f')

        # Caixa de eventos, necessaria para pintar fundo de azul/vermelho
        ebox_blue = self.Main_Window.get_widget('ebox_blue')
        ebox_red = self.Main_Window.get_widget('ebox_red')
        # Botoes de falta
        b_f1mf = self.Main_Window.get_widget('b_f1mf')
        b_f1f = self.Main_Window.get_widget('b_f1f')
        b_f2mf = self.Main_Window.get_widget('b_f2mf')
        b_f2f = self.Main_Window.get_widget('b_f2f')
        # Nomes dos lutadores
        self.l_blue_name = self.Main_Window.get_widget("l_fighter_blue_name")
        self.l_red_name = self.Main_Window.get_widget("l_fighter_red_name")

        # Seta cor de fundo das caixas onde aparecem os pontos
        ebox_blue.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("blue"))
        ebox_red.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("red"))

        self.interfaces = self.get_interfaces()

        # Menu item 'interface selecion'
        menu_is = self.Main_Window.get_widget('menu_is')

        self._create_interfaces_menu(menu_is)

        # Inicializa sistema de contagem de pontos.
        self.PointCounter = PointCounter(self)

        # Start the game
        self.new_game(None)

        # Stop counting until the number of judges be set
        self.PointCounter.stop_counting()

        # Define interface dos juizes com o jogo
        # TODO: descobrir através de menu ou .conf qual interface o
        # usuário deseja para seu jogo. Posteriormente permitir mescla
        # de interfaces
        #self.interface = keyboard.Interface(self)
        #self.interface = wiimote.Interface(self)
        #self.interface.configure()

        # Set number of judges and enable counting
        #self.PointCounter.set_number_of_judge(self.interface.n_of_judges)
        #self.PointCounter.start_counting()

    def _create_interfaces_menu(self,menu):
        group = gtk.RadioMenuItem()
        for i in self.interfaces:
            self._append_item_to_menu(menu,group,i)

    def _append_item_to_menu(self, menu, group, title):
        item = gtk.RadioMenuItem(group=group, label=title)
        item.set_name(title)
        item.connect("activate", self.set_interface)
        item.show()
        menu.append(item)

    def get_interfaces(self):
        dir_interfaces = "interfaces"
        interfaces = {}

        interfacesList = [ os.path.splitext(fname)[0]
        for fname in os.listdir(dir_interfaces)
        if os.path.splitext(fname)[1] ==".py" and fname[0] != '_' and
            fname != 'common.py' ]

        for file in interfacesList:
            # path to interfaces
            file = os.path.join(dir_interfaces, file)
            # important data
            fp, path, desc = imp.find_module(file)
            # load interfaces
            try:
                interface = imp.load_module(file, fp, path, desc)
            finally:
                if fp: fp.close()

            # add the new interfaces
            interfaces[interface.NAME] = { 'module':interface }

        return interfaces

    def set_interface(self, ikey):
        self.PointCounter.stop_counting()
        interface = self.interfaces[ikey.name]['module']
        self.interface = interface.Interface(self)
        self.interface.configure()
        self.PointCounter.set_number_of_judge(self.interface.n_of_judges)
        self.PointCounter.start_counting()

    def new_game(self, widget):
        self._zera_pontos()
        self._zera_faltas()
        blue_name,red_name = FighterNames().run()
        self.write_names(blue_name,red_name)
        self.PointCounter.start_counting()

    def write_names(self,blue,red):
        """ Escreve o nome dos lutadores na tela """
        self.l_blue_name.set_text("<b>"+blue.title()+"</b>")
        self.l_red_name.set_text("<b>"+red.titlet()+"</b>")
        # Aceitar marcacao
        self.l_blue_name.set_use_markup(True)
        self.l_red_name.set_use_markup(True)

    def set_text_point(self, widget, n):
        self.sem_points.acquire()
        msg = '<span foreground="white" size="200000">%s</span>'%n
        widget.set_label(msg)
        self.sem_points.release()

    def point_control(self, j,f):
        self.PointCounter.point_control(j,f)

    def point_to(self, f):
        """ Jogo acaba quando diferenca de pontos entre os lutadores for
            maior ou igual a 7 ou um dos lutadores alcancar 12 pontos """
        if f == 1:
            self.f1p += 1
            if self.f1p - self.f2p >= 7 or self.f1p >= 12:
                self.set_text_point(self.l_f1p, "%d!"%self.f1p)
                self.PointCounter.stop_counting()
            else:
                self.set_text_point(self.l_f1p,str(self.f1p))
        elif f == 2:
            self.f2p += 1
            if self.f2p - self.f1p >= 7 or self.f2p >= 12:
                self.set_text_point(self.l_f2p, "%d!"%self.f2p)
                self.PointCounter.stop_counting()
            else:
                self.set_text_point(self.l_f2p,str(self.f2p))

    def b_f1mf_clicked(self, widget):
        """ Atualiza meia falta lutar 1 """
        faltas = int(self.l_f1mf.get_text())
        self.l_f1mf.set_text(str(faltas + 1))

    def b_f1f_clicked(self, widget):
        """ Atualiza falta inteira lutar 1 """
        faltas = int(self.l_f1f.get_text())
        self.l_f1f.set_text(str(faltas + 1))

    def b_f2mf_clicked(self, widget):
        """ Atualiza meia falta lutador 2 """
        faltas = int(self.l_f2mf.get_text())
        self.l_f2mf.set_text(str(faltas + 1))

    def b_f2f_clicked(self, widget):
        """ Atualiza falta inteira lutar 2 """
        faltas = int(self.l_f2f.get_text())
        self.l_f2f.set_text(str(faltas + 1))

    def _zera_pontos(self):
        self.f1p = 0
        self.f2p = 0
        self.set_text_point(self.l_f1p, "0")
        self.set_text_point(self.l_f2p, "0")

    def _zera_faltas(self):
        self.l_f1mf.set_text("0")
        self.l_f1f.set_text("0")
        self.l_f2mf.set_text("0")
        self.l_f2f.set_text("0")

    def quit(self, widget):
        try: self.interface.t_quit = True
        except: pass
        gtk.main_quit()

if __name__ == "__main__":
    gtk.gdk.threads_init()
    gtk.gdk.threads_enter()
    fight = Fight()
    gtk.gdk.threads_leave()
    gtk.main()

