#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
from GUI.FenetrePrincipale import *

class TWAT:	
	
	#Test le format de l'URL passé en argument
	def testFormatURL(self, url):
		pass
	
	#Test si l'URL est accessible
	def testURLAccessible(self, url):
		pass
	
	#Test le format du fichier
	def testFormatFichier(self, fichier):
		pass

if __name__ == '__main__':
	try:
		fenetreP = FenetrePrincipale()
		gtk.main()
		texte = "TEST"
		fenetreP.affichageTest(texte)
	except KeyboardInterrupt:
		pass
