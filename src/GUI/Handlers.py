#!/usr/bin/python
# -*- coding: UTF-8 -*-

import gtk
from TWAT import *
from GUI.FenetrePrincipale import *

class Handlers():	

	def __init__(self, fenetre):
		self.fenetre = fenetre	
		self.twat = TWAT(self.fenetre)	
	
	#Destruction de la fenetre
	def on_window1_destroy(self, window1):
		gtk.main_quit()
		
	#Action à l'activation du bouton Start !
	def on_button1_clicked(self, button1):
		self.twat.attack()
		
	#Action pour activer/désactiver le test ping dans les options
	def on_imagemenuitem6_activate(self, imagemenuitem6):
		if(self.twat.ping == True):
			self.twat.ping = False
			imagemenuitem6.set_label("Activer test ping")
		else:
			self.twat.ping = True
			imagemenuitem6.set_label("Désactiver test ping")
