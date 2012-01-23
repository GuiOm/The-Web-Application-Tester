#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade

class FenetrePrincipale:
	def __init__(self):
		builder = gtk.Builder()
		builder.add_from_file("GUI/interface.glade")		
		
		#Définition des events à appliquer 
		handlers = {
			#listener : fonction,
			"onDeleteWindow": gtk.main_quit,
		}
		builder.connect_signals(handlers)
		
		window = builder.get_object("window1")
		window.show_all()		

if __name__ == '__main__':
	app = FenetrePrincipale()
	gtk.main()
