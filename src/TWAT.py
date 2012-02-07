#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os,sys,re
from GUI.FenetrePrincipale import *

class TWAT:
	options = []
	url = ""
	fichier = ""
	
	def __init__(self, fenetre):
		self.fenetre = fenetre
	
	#Reformate l'URL passée en paramètre -> si URL du type http://www.site.com ou http://site.com on ressort www.site.com
	def reformateURL(self, url):
		if(url.find("http://") != -1):
			print("url avec http://")
		else:
			print("url sans http://")
			
		return url
	
	#Fonction qui teste si l'URL est bien accessible
	def testURLAccessible(self, url):
		success = False
		urlReformate = self.reformateURL(url)
		
		regexReceived = re.compile(" received")
		ping = os.popen("ping -c1 -q " + urlReformate + " 2>/dev/null")
		while 1:
			responsePing = ping.readline()
			if not responsePing : break
			igot = re.findall(regexReceived, responsePing)
			if igot:
				success = True
	
		if(success == True): return True
		else: return False
	
	#Test le format du fichier
	def testFormatFichier(self, fichier):
		pass		
		
	#Fonction qui retourne les éléments passé en paramètres d'URL et retourne un dictionnaire qui les contient
	def recupGET(self, url):

		param = []
		dictio = {}

		if url.find("?") >= 0:
			page = url.split('?')[0]
			query = url.split('?')[1]
			params = query.split('&')
		if query.find("=") >= 0:
			for param in params:
				dictio[param.split('=')[0]] = param.split('=')[1]
			
		return dictio		
			
	#Récupère le ou les formulaires présents dans la page
	def recupPOST(self, url):
		pass
		
	def checkOptions(self, options):
		if(options == []):
			self.fenetre.setMessage("Veuillez choisir au moins une option")
		elif(options == ["post"]):
			self.fenetre.setMessage("Veuillez choisir une option en plus de POST")
		
	#Lancement de l'attaque
	def attack(self):
		self.options = self.fenetre.getOptions()
		url = self.fenetre.getURL()
		fichier = self.fenetre.getFile()		
		
		#Si une URL et un fichier sont entrés
		if(url and fichier):
			self.fenetre.setMessage("Vous ne pouvez pas mettre une URL et un fichier en même temps")
			
		#Si une URL est entrée mais pas de fichier, on lance l'attaque en blackbox
		elif(url and not fichier):
			#On test si l'URL est accessible
			if(self.testURLAccessible(url) == False):
				self.fenetre.setMessage("URL inaccessible")
			else:
				self.checkOptions(self.options)
				
		#Si un fichier est entré mais pas d'URL, on lance l'attaque en whitebox
		elif(fichier and not url):
			#On test si le fichier est supporté
			if(testFormatFichier == False):
				self.fenetre.setMessage("Type de fichier incorrect")
			#Sinon, fichier supporté, on continue
			else:
				pass
		else:
			self.fenetre.setMessage("Vous devez entrer soit une url soit un fichier")
		
if __name__ == '__main__':
	try:
		fenetreP = FenetrePrincipale()
		gtk.main()
	except KeyboardInterrupt:
		pass
