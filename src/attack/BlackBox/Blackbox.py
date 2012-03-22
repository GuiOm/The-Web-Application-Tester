#!/usr/bin/python
# -*- coding: UTF-8 -*-

###### REQUETE POST EN PYTHON -> RECUP champ input BeautifulSoup
#	http://www.puyb.net/index.php/2009/12/11/139-open-wifi-auto-connect
#	http://www.voidspace.org.uk/python/articles/urllib2.shtml
#

############################	TODO LIST	##########################
#	- Injection Blind  SQL
#	- Fonction xss
#	- Refactoring envoi de requete (avec et sans données (GET/POST))
######################################################################

import os, urllib, urllib2, re
from BeautifulSoup import BeautifulSoup
from Report.ReportGenerator import ReportGenerator

class Blackbox:
	def __init__(self, url, options, site):
		if url[:4] != "http":
			self.url = "http://"+url
		else:
			self.url = url
		self.options = options
		self.site = site
		self.report = ReportGenerator(site)
		self.soup = BeautifulSoup(str(self.getHTML(self.url)))
		
		
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

		if dictio == {}:
			return False
		else:
			return dictio
	"""	
	#Récupère les noms des formulaires présent sur une page
	#Retourne un tableau contenant les noms des formulaires présents sur la page
	def recupForm(self, url):
		formNames = []
		form = self.soup.findAll("form")
		if not form:
			return False
		else:
			for formName in form:
				formNames.append(str(formName['name']))
			
			return formNames
	"""
	
	#Retourne un tableau qui contient les noms des champs input de type text et password
	def recupPost(self, url):
		inputs = {}
		#On stocke toutes les balises input dans un dictionnaire s'ils sont de type text ou password
		for tagInput in self.soup.findAll("input"):
			if tagInput.has_key("name") and (tagInput.has_key("type") and (tagInput["type"] == "text" or tagInput["type"] == "password")):
				inputs[str(tagInput["name"])] = ""
			
		if inputs == {}:
			return False
		else:
			return inputs		
		
	def loadPayload(self, payload):
		pass
	
	#Retire les retours chariots
	def cleanPayload(self, payload):
		if payload[-2:] == '\r\n':
			return payload[:-2]
		elif payload[-1:] == '\r' or payload[-1:] == '\n':
			return payload[:-1]
		else:
			return payload
			
			
	# La variable get est un dictionnaire qui contient tous les paramètres get et leur valeur
	# La variable post est un booléen pour savoir si on teste les formulaires ou pas
	
	def xss(self, get, post):
		pass
		
	def sqli(self, get, post):
		url = self.url
		databaseError = {
    "MySQL": (r"SQL syntax.*MySQL", "Warning.*mysql_.*", r"valid MySQL result", r"MySqlClient\."),
    "PostgreSQL": (r"PostgreSQL.*ERROR", r"Warning.*\Wpg_.*", r"valid PostgreSQL result", r"Npgsql\."),
    "Microsoft SQL Server": (r"Driver.* SQL[\-\_\ ]*Server", r"OLE DB.* SQL Server", r"(\W|\A)SQL Server.*Driver", r"Warning.*mssql_.*", r"(\W|\A)SQL Server.*[0-9a-fA-F]{8}", r"(?s)Exception.*\WSystem\.Data\.SqlClient\.", r"(?s)Exception.*\WRoadhouse\.Cms\."),
    "Microsoft Access": (r"Microsoft Access Driver", r"JET Database Engine", r"Access Database Engine"),
    "Oracle": (r"ORA-[0-9][0-9][0-9][0-9]", r"Oracle error", r"Oracle.*Driver", r"Warning.*\Woci_.*", r"Warning.*\Wora_.*")
}
		data = {}
		#On charge les payloads
		payloads = open("attack"+os.sep+"BlackBox"+os.sep+"Payloads"+os.sep+"sqli.txt").readlines()
	
		#On injecte les paramètres POST si un formulaire se trouve dans la page
		if post == True:
			tabPost = self.recupPost(url)
			#Si un formulaire est présent dans la page
			if tabPost != False:
			
				#On injecte tous les champs d'un coup
				for payload in payloads:
						payload = self.cleanPayload(payload)
						for key in tabPost:
							data[key] = payload
						
						encodedData = urllib.urlencode(data)
							
						response = urllib2.urlopen(url, encodedData)
						responseHtml = response.read()
						
						#On test si une injection sql est présente : recherche de message d'erreur lié à la base de données
						for databaseName in databaseError:
							for regex in databaseError[databaseName]:
								if re.search(regex, responseHtml):
									self.report.addVulnerabilityBlackBox("Injection SQL", "POST", "dans la page : "+self.url+" avec l'injection : "+payload)
				
				#On injecte champ par champ
				for payload in payloads:
					payload = self.cleanPayload(payload)
					for key in tabPost:
						data = {}						
						data[key] = payload
						encodedData = urllib.urlencode(data)
						response = urllib2.urlopen(url, encodedData)
						responseHtml = response.read()

						#On test si une injection sql est présente : recherche de message d'erreur lié à la base de données
						for databaseName in databaseError:
							for regex in databaseError[databaseName]:
								if re.search(regex, responseHtml):
									self.report.addVulnerabilityBlackBox("Injection SQL", "POST", "Dans le champ : "+key+", avec l'injection : "+payload)
									#break
											
						
		#Si il y a des paramètres GET à tester, on les injecte
		if get != False:
			#On fait une copie du dictionnaire des données get
			data = get.copy()
			for payload in payloads:
				payload = self.cleanPayload(payload)
				for param, valeur in get.items():
					if valeur == "TEST":
						data[param] = payload						
				
				encodedData = urllib.urlencode(data)
				encodedUrl = self.url.split("?")[0]+"?"+encodedData
				response = self.getHTML(encodedUrl)
				
				for databaseName in databaseError:
					for regex in databaseError[databaseName]:
						if re.search(regex, str(response)):
							self.report.addVulnerabilityBlackBox("Injection SQL", "GET", "avec l'injection : "+payload+" - Données envoyées : "+encodedData)
		
		
		
	def lfi(self, get, post):
		site = self.site
		payloads = open("attack"+os.sep+"BlackBox"+os.sep+"Payloads"+os.sep+"lfi.txt").readlines()
		
		if site[:4] != "http":
			site = "http://"+site
		if get != False:
			for param, valeur in get.items():	
				if valeur == "TEST":	
					for payload in payloads:
						payload = self.cleanPayload(payload)				
						response = self.getHTML(self.url.split("?")[0]+"?"+param+"="+payload)
						if(re.findall("root:x:", str(response))):
							self.report.addVulnerabilityBlackBox("LFI", "GET", "dans le paramètre : "+param+" avec l'injection : "+payload)
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
		else:
			get = False
			
		if("xss" in self.options):
			self.xss(get, doPost)
		if("sqli" in self.options):
			self.sqli(get, doPost)
		if("lfi" in self.options):
			self.lfi(get, doPost)
