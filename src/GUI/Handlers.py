#!/usr/bin/python
# -*- coding: UTF-8 -*-

import gtk
from TWAT import *
from GUI.FenetrePrincipale import *

class Handlers():	

	def __init__(self, fenetre):
		self.fenetre = fenetre		
	
	#Destruction de la fenetre
	def on_window1_destroy(self, window1):
		gtk.main_quit()
		
	#Action à l'activation du bouton Start !
	def on_button1_clicked(self, button1):
		#options = getOptions()
		twat = TWAT(self.fenetre)
		twat.attack()
