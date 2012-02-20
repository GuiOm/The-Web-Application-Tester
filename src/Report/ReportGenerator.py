#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os,sys,time

class ReportGenerator:
	def __init__(self, name):
		self.name = name		
		nbFile = 1
		
		for f in os.walk("Rapports"+os.sep): 
			nbFile += len(f[2])
		
		#Chemin du rapport
		#self.fileName = "Rapports"+os.sep+str(nbFile)+"-"+str(int(time.time()))+".log"
		self.fileName = "Rapports"+os.sep+str(nbFile)+"-"+self.name+".log"
		
		#Crée le fichier dans lequel sera stocké le rapport
		initFile = open(self.fileName, "w")
		initFile.close()

	#Ajoute une vulnérabilité au rapport
	def addVulnerability(self, typeVulnerability, line, info):
		fileReport = open(self.fileName, "a")
		fileReport.write("Faille "+typeVulnerability+" ligne "+line+" : "+info+"\n")
		fileReport.close()
		
	def openReport(self):
		fileReport = open(self.fileName, "r")
		reportText = fileReport.readlines()				
		text = ""
		
		for i in reportText:
			text += i
			
		fileReport.close()		
		
		if(text == ""):
			text = "Pas de faille trouvée"
		return text
