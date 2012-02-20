#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Report.ReportGenerator import ReportGenerator

class Blackbox:
	def __init__(self, url, options, site):
		self.url = url
		self.options = options
		self.report = ReportGenerator(site)
		
	#Récupération html
	def getHTML(self, url):
		req = urllib2.Request(url)
		reponse = urllib2.urlopen(req)
		return reponse
		
	def xss(self, post):
		pass
		
	def sqli(self, post):
		pass
		
	def lfi(self, post):
		pass
		
		
	#Fonction principale qui lance l'attaque en blackbox
	def attack(self):
		if ("post" in self.options):
			doPost = True
		else:
			doPost = False
		
		self.report.addVulnerability("xss", "12", "test info de la faille")

