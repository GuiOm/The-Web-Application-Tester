#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re,os
from Report.ReportGenerator import ReportGenerator

class Whitebox:
	def __init__(self, fileName, options):
		self.fileName = fileName
		self.report = ReportGenerator(fileName.split(os.sep)[-1])
		self.options = options
		
	def xss(self, line, nbLine):
		match = re.search("echo \$_SERVER\['PHP_SELF'\]", line)
		
		if(match != None):
			self.report.addVulnerability("XSS", str(nbLine), "xss de type reflected, dû à une mauvaise utilisation de $_SERVER['PHP_SELF']")
		
	#Fonction principale qui lance l'attaque en whitebox
	def attack(self):
		fichier = open(self.fileName, "r")
		source = fichier.readlines()

		i = 0
		for line in source:
			i+=1
			if("xss" in self.options):
				self.xss(line, i)
		
		fichier.close()
