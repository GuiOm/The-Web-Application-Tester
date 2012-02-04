#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os,sys
from GUI.FenetrePrincipale import *

class TWAT:	
	def __init__(self):
		self.options = []
		self.url = ""
		self.fichier = ""
		#self.fenetreP = FenetrePrincipale()
	
	#Test le format de l'URL passé en argument
	def testFormatURL(self, url):
		pass
	
	#Test si l'URL est accessible
	def testURLAccessible(self, url):
		pass
	
	#Test le format du fichier
	def testFormatFichier(self, fichier):
		pass
		
	#Lancement de l'attaque
	def attack(self):
		pass
		
if __name__ == '__main__':
	try:
		fenetreP = FenetrePrincipale()
		#twat = TWAT()
		gtk.main()
	except KeyboardInterrupt:
		pass
