#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os,sys,re
from GUI.FenetrePrincipale import *
from attack.BlackBox.Blackbox import *
from attack.WhiteBox.Whitebox import *

class TWAT:	
	def __init__(self, fenetre):
		self.fenetre = fenetre
		self.authorizedExtension = ("php", "php3")
		self.options = []
		self.url = ""
		self.fichier = ""
		self.ping = True
		self.dirReport = "Rapports"
	
	#Reformate l'URL passée en paramètre -> si URL du type http://www.site.com ou http://site.com on ressort www.site.com
	def reformateURL(self, url):
		#Si l'adresse commence par http://, on le retire, sinon le ping ne fonctionne pas
		if(url.find("http://") != -1):
			return url.split("http://")[-1]
		else:
			return url
	
	#Récupère le nom du site d'une URL : http://www.google.fr/page.php?ex=1 -> google.fr
	def recupNomSite(self, url):
		urlReformate = self.reformateURL(url)
		return urlReformate.split("/")[0]
	
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
		
	#Retourne le nom du fichier choisi par l'utilisateur	
	def getFileName(self, fichier):
		nomFichier = fichier.split(os.sep)
		return nomFichier[len(nomFichier)-1]
		
	#Retourne l'extension du fichier
	def getExtensionFile(self, fichier):
		return fichier.split(".")[-1]
	
	#Test le format du fichier
	#Le paramètre fichier est un string qui contient le chemin vers le fichier
	def testFormatFichier(self, fichier):
		if(self.getExtensionFile(fichier) in self.authorizedExtension):
			return True		
		else:
			return False		
	
	#Récupère le ou les formulaires présents dans la page
	def recupPOST(self, url):
		pass
		
	def checkOptions(self, options):
		if(options == []):
			self.fenetre.setMessage("Veuillez choisir au moins une option")
		elif(options == ["post"]):
			self.fenetre.setMessage("Veuillez choisir une option en plus de POST")
			
	#Fonction pour activer ou non le ping de test
	def setTestPing(self, boolean):
		self.ping = boolean
		
	#Fonction pour supprimer les rapports générés
	def removeReports(self):
		for f in os.walk(self.dirReport+os.sep):
			for fileName in f[2]:
				if(fileName.find(".log") != -1):
					os.remove(self.dirReport+os.sep+fileName)

	#Lancement de l'attaque
	def attack(self):
		continu = True
		self.options = self.fenetre.getOptions()
		url = self.fenetre.getURL()
		fichier = self.fenetre.getPathToFile()
		site = self.recupNomSite(url)
		
		#Si une URL et un fichier sont entrés
		if(url and fichier):
			self.fenetre.setMessage("Vous ne pouvez pas mettre une URL et un fichier en même temps")
			
		#Si une URL est entrée mais pas de fichier, on lance l'attaque en blackbox
		elif(url and not fichier):
			#Si l'option test ping est activée, on test si l'URL est accessible
			if(self.ping == True):
				if(self.testURLAccessible(url) == False):
					self.fenetre.setMessage("URL inaccessible")
					continu = False
				else:
					self.fenetre.setMessage("URL accessible")
					continu = True
					
			if(continu == True):				
				self.checkOptions(self.options)
				blackbox = Blackbox(url, self.options, site)
				blackbox.attack()
				self.fenetre.setMessage(blackbox.report.openReport())
				
		#Si un fichier est entré mais pas d'URL, on lance l'attaque en whitebox	
		elif(fichier and not url):
			#On test si le fichier est supporté
			if(self.testFormatFichier(fichier) == False):
				self.fenetre.setMessage("Type de fichier incorrect")
			#Sinon, fichier supporté, on continue
			else:
				self.checkOptions(self.options)
				whitebox = Whitebox(fichier, self.options)
				whitebox.attack()
				self.fenetre.setMessage(whitebox.report.openReport())
		else:
			self.fenetre.setMessage("Vous devez entrer soit une url soit un fichier")
		
if __name__ == '__main__':
	try:
		fenetreP = FenetrePrincipale()
		gtk.main()
	except KeyboardInterrupt:
		pass
