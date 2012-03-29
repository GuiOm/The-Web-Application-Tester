#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
import os
from Handlers import *

class FenetrePrincipale:
	builder = gtk.Builder()
	builder.add_from_file("GUI"+os.sep+"interface.glade")
			
	######################################################
	##			INITIALISATION DE LA FENETRE			##
	####__________________________________________________	
	
	def __init__(self):
		self.builder.connect_signals(Handlers(self))
		
		window = self.builder.get_object("window1")
		window.show_all()
		
		#Message de bienvenue
		welcomeMessage = "Bienvenue dans The Web Application Tester\n\n[+] Pour utiliser cet outil vous avez le choix entre 2 modes :\n\t- Soit en entrant une URL (le test se fera alors en blackbox),\n\t- Soit en entrant un fichier (le test se fera en whitebox).\n\n[+] Choisissez les différentes vulnérabilités que vous voulez tester en cochant les cases.\n\n[+] Pour tester les paramètres GET en url, donnez leur la valeur TEST\n\tExemple : localhost/votre_site/index.php?page=TEST\n\n[+] Pour avoir un meilleur résultat, utilisez le fichier de configuration PHP fourni.\n\n[+] Pendant vos tests, pour repérer au mieux les injections SQL, affichez les erreurs des vos requêtes.\n\tPar exemple avec MySQL : $result = mysql_query($requete, $connexion) or die(mysql_error());\n\n[+] Pensez à retirer cet affichage des erreurs à la mise en production de vos pages web !"
		self.setMessage(welcomeMessage)
		
		
	######################################################
	##		DEFINITION DES FONCTIONS SUR LA FENETRE		##
	####__________________________________________________	
	
	
	#Définit le texte dans la boite d'informations
	def setMessage(self, text):
		info = self.builder.get_object("textview1")
		buffertexte = info.get_buffer()
		buffertexte.set_text(text)
	
	#Modifie le label en dessous du choix de l'URL à tester	
	def setMessageLabelURL(self, text):
		label = self.builder.get_object("label3")
		label.set_text(text)
	
	#Modifie le label en dessous du sélecteur de fichier	
	def setMessageLabelFile(self, text):
		label = self.builder.get_object("label2")
		label.set_text(text)
		
	def cleanScreen(self):
		self.setMessage("")
		
	#Récupère les options cochées par l'utilisateur et retourne une liste des options
	def getOptions(self):
		options = []
		
		if(self.builder.get_object("checkbutton1").get_active()):
			options = ["xss", "sqli", "lfi", "post"]
		else:
			if(self.builder.get_object("checkbutton2").get_active()):
				options.append("xss")
			if(self.builder.get_object("checkbutton3").get_active()):
				options.append("sqli")
			if(self.builder.get_object("checkbutton4").get_active()):
				options.append("lfi")
			if(self.builder.get_object("checkbutton5").get_active()):
				options.append("post")
			
		return options
		
	#Retourne le chemin du fichier choisi par l'utilisateur
	def getPathToFile(self):
		fichier = self.builder.get_object("filechooserbutton1")
		nomFichier = fichier.get_filename()
		return nomFichier
		
	#Retourne l'URL entrée par l'utilisateur
	def getURL(self):
		url = self.builder.get_object("entry1")
		return url.get_text()
