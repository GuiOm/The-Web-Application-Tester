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
		
		#Message de bienvenue
		boiteInfo = builder.get_object("textview1")
		bufferTexte = boiteInfo.get_buffer()
		bufferTexte.set_text("Bienvenue dans The Web Application Tester\n\n"
		+"Pour utiliser cet outil vous avez le choix entre 2 modes :\n\n"
		+"- Soit en entrant une URL (le test se fera alors en blackbox),\n"
		+"- Soit en entrant un fichier (le test se fera en whitebox).\n\n"
		+"Choisissez les différentes vulnérabilités que vous voulez tester en cochant les cases.")
		
	def affichageTest(self, texte):
		info = builder.get_object("textview1")
		buffertexte = info.get_buffer()
		buffertexte.set_text(texte)
		
	#Définit le texte dans la boite d'informations
	def setMessage(self, texte):
		pass
