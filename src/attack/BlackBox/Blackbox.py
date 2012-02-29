#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os,urllib2,re
from Report.ReportGenerator import ReportGenerator

class Blackbox:
	def __init__(self, url, options, site):
		self.url = url
		self.options = options
		self.site = site
		self.report = ReportGenerator(site)
		
	#Récupération html
	def getHTML(self, url):
		req = urllib2.Request(url)
		reponse = urllib2.urlopen(req)
		return reponse.readlines()
		
	#Fonction qui retourne les éléments passé en paramètres d'URL et retourne un dictionnaire qui les contient
	def recupGET(self, url):
		param = []
		dictio = {}

		if(url.find("?") >= 0):
			page = url.split('?')[0]
			query = url.split('?')[1]
			params = query.split('&')
		if(query.find("=") >= 0):
			for param in params:
				dictio[param.split('=')[0]] = param.split('=')[1]
			
		return dictio	
		
	def loadPayload(self, payload):
		pass
	
	#Retire les retours chariots
	def cleanPayload(self, payload):
		if payload[-2:] == '\r\n':
			return payload[:-2]
		elif payload[-1:] == '\r' or payload[-1:] == '\n':
			return payload[:-1]
			
			
	# La variable get est un dictionnaire qui contient tous les paramètres get et leur valeur
	# La variable post est un booléen pour savoir si on teste les formulaires ou pas
	
	def xss(self, get, post):
		pass
		
	def sqli(self, get, post):
		pass
		
	def lfi(self, get, post):
		site = self.site
		payloads = open("attack"+os.sep+"BlackBox"+os.sep+"Payloads"+os.sep+"lfi.txt").readlines()
		
		if site[:4] != "http":
			site = "http://"+site
			
		for param, valeur in get.items():	
			if valeur == "TEST":	
				for payload in payloads:			
					payload = self.cleanPayload(payload)				
					response = self.getHTML("http://"+self.url.split("?")[0]+"?"+param+"="+payload)
					if(re.findall("root:x:", str(response))):
						self.report.addVulnerabilityBlackBox("LFI", "dans le paramètre GET : "+param+" avec l'injection : "+payload)
						break
		
		
	#Fonction principale qui lance l'attaque en blackbox
	def attack(self):
		if ("post" in self.options):
			doPost = True
		else:
			doPost = False
		
		if("?" in self.url):
			#On récupère les paramètres GET en URL
			get = self.recupGET(self.url)
			
		if("xss" in self.options):
			self.xss(get, doPost)
		if("sqli" in self.options):
			self.sqli(get, doPost)
		if("lfi" in self.options):
			self.lfi(get, doPost)
