#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re,os
from Report.ReportGenerator import ReportGenerator

class Whitebox:
	def __init__(self, fileName, options, report):
		self.fileName = fileName
		self.report = report
		self.options = options
		self.xss = {
		"echo \$_SERVER\['PHP_SELF'\]":["Faille","xss de type reflected, dû à une mauvaise utilisation de $_SERVER['PHP_SELF']"],
		"echo\(?(.*)(?<!\()(\$_POST|\$_GET)":["Faille","Réaffichage de données utilisateur non filtrées"]
		}
		self.lfi = {
		"include\ ?\(?(\$_GET|\$_POST)":["Faille","Inclusion de données utilisateur"]
		}
		self.sqli = {
		"(SELECT|UPDATE)(.*)(\'(\"\.)?|\\\"|\"\.)\ ?(\$_POST|\$_GET)":["Faille", "Utilisation de donnée utilisateur non filtrée dans une requête SQL"],
		"=\ ?addslashes\(":["Warning", "La fonction addslashes n'échappe pas tous les caractères spéciaux"]
		}
		
	#Fonction qui lance l'attaque en whitebox
	def attack(self):
		variables = []
		fichier = open(self.fileName, "r")
		source = fichier.readlines()
		
		i = 0
		for line in source:
			i+=1
			
			#Si on affecte une variable utilisateur (GET/POST) à une autre variable sans la filtrer
			match = re.search("(\$[a-zA-Z0-9]{0,50})\ ?=\ ?(\$_GET|\$_POST)", line)
			if match != None:
				if match.group(1) not in variables:
					variables.append(match.group(1))
					
			#Si la valeur d'une variable stockée dans le tableau est remodifiée après dans le script, il faut la retirer du tableau
			for var in variables:
				match = re.search("\\"+var+"\ ?=\ ?[a-z_]{0,40}\(\\"+var, line)
				if match != None:
					variables.remove(var)
				
			if("xss" in self.options):
				for regex, info in self.xss.items():
					match = re.search(regex, line)
					if match != None:
						self.report.addVulnerabilityWhiteBox(info[0], "XSS", str(i), info[1])
					else:
						for var in variables:
							match = re.search(regex.replace("(\$_POST|\$_GET)", "\\"+var), line)
							if match != None:
								self.report.addVulnerabilityWhiteBox(info[0], "XSS", str(i), info[1]+" - variable "+var)
			if("lfi" in self.options):
				for regex, info in self.lfi.items():
					match = re.search(regex, line)
					if match != None:
						self.report.addVulnerabilityWhiteBox(info[0], "LFI", str(i), info[1])
					else:
						for var in variables:
							match = re.search(regex.replace("(\$_POST|\$_GET)", "\\"+var), line)
							if match != None:
								self.report.addVulnerabilityWhiteBox(info[0], "LFI", str(i), info[1]+" - variable "+var)
			if("sqli" in self.options):
				for regex, info in self.sqli.items():
					match = re.search(regex, line, re.I)
					if match != None:
						self.report.addVulnerabilityWhiteBox(info[0], "Injection SQL", str(i), info[1])
					else:
						for var in variables:
							match = re.search(regex.replace("(\$_POST|\$_GET)", "\\"+var), line, re.I)
							if match != None:
								self.report.addVulnerabilityWhiteBox(info[0], "Injection SQL", str(i), info[1]+" - variable "+var)

		fichier.close()
