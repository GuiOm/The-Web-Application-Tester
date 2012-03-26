#!/usr/bin/python
# -*- coding: UTF-8 -*-


############################	TODO LIST	##########################
#	- Injection Blind  SQL
######################################################################

import os, urllib, urllib2, re, random
import BeautifulSoup
from Report.ReportGenerator import ReportGenerator

class Blackbox:
	def __init__(self, url, options, site, report):
		if url[:4] != "http":
			self.url = "http://"+url
		else:
			self.url = url
		self.options = options
		self.site = site		
		self.soup = BeautifulSoup.BeautifulSoup(self.getHTML(self.url, None, None))
		self.report = report
		
		
	#Récupération html avec envoie de données
	#typeRequete = get ou post
	def getHTML(self, url, data, typeRequete):		
		if typeRequete == "post" and data != None:
			encodedData = urllib.urlencode(data)
			response = urllib2.urlopen(url, encodedData)
		elif typeRequete == "get" and data != None:
			encodedData = urllib.urlencode(data)
			url = self.url.split("?")[0]+"?"+ encodedData
			response = urllib2.urlopen(url)
		else:
			response = urllib2.urlopen(url)
			
		return response.read()
		
		
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
		
	#Retire les retours chariots
	def cleanPayload(self, payload):
		if payload[-2:] == '\r\n':
			return payload[:-2]
		elif payload[-1:] == '\r' or payload[-1:] == '\n':
			return payload[:-1]
		else:
			return payload
			
		
	#Fonction principale qui lance l'attaque en blackbox
	def attack(self):
		if ("post" in self.options):
			#On récupère les champ POST à injecter
			post = self.recupPost(self.url)
		else:
			post = False
		
		if("?" in self.url):
			#On récupère les paramètres GET en URL
			get = self.recupGET(self.url)
		else:
			get = False
			
		if("xss" in self.options):
			xss = Xss(self.url, self.options, self.site, self.report)
			xss.attack(get, post)
		if("sqli" in self.options):
			sqli = Sqli(self.url, self.options, self.site, self.report)
			sqli.attack(get, post)
		if("lfi" in self.options):
			lfi = Lfi(self.url, self.options, self.site, self.report)
			lfi.attack(get, post)
	
	
											#################################
											####			CLASSE LFI
											#######__________________________
			
class Lfi(Blackbox):
	def __init__(self, url, options, site, report):
		Blackbox.__init__(self, url, options, site, report)
		self.payloads = open("attack"+os.sep+"BlackBox"+os.sep+"Payloads"+os.sep+"lfi.txt").readlines()
		self.report = report

	def attack(self, get, post):
		if get != False:
			self.attackGet(get)
	
	def attackGet(self, get):		
		for param, valeur in get.items():
			if valeur == "TEST":
				data = get.copy()
				for payload in self.payloads:
					payload = self.cleanPayload(payload)
					data[param] = payload
					response = self.getHTML(self.url, data, "get")
					if(re.findall("root:x:", response)):
						self.report.addVulnerabilityBlackBox("LFI", "GET", "dans le paramètre : "+param+" avec l'injection : "+payload)
						break
						
	def attackPost(self, post):
		data = {}
		#On injecte tous les champs d'un coup
		for payload in self.payloads:
			payload = self.cleanPayload(payload)
			for key in post:
				data[key] = payload
			#On récupère la réponse
			response = self.getHTML(self.url, data, "post")
			if(re.findall("root:x:", response)):
				self.report.addVulnerabilityBlackBox("LFI", "GET", "dans la page : "+self.url+" avec l'injection : "+payload)
				break
				
		#On injecte champ par champ
		for payload in self.payloads:
			payload = self.cleanPayload(payload)
			for key in post:
				data = {}						
				data[key] = payload
				#On récupère la réponse
				response = self.getHTML(self.url, data, "post")
				if(re.findall("root:x:", response)):
					self.report.addVulnerabilityBlackBox("LFI", "GET", "dans le paramètre : "+param+" avec l'injection : "+payload)

							
											#################################
											####		CLASSE SQLI
											#######__________________________
class Sqli(Blackbox):
	def __init__(self, url, options, site, report):
		Blackbox.__init__(self, url, options, site, report)
		self.payloads = open("attack"+os.sep+"BlackBox"+os.sep+"Payloads"+os.sep+"sqli.txt").readlines()
		self.report = report
		self.databaseError = {
    "MySQL": (r"SQL syntax.*MySQL", "Warning.*mysql_.*", r"valid MySQL result", r"MySqlClient\."),
    "PostgreSQL": (r"PostgreSQL.*ERROR", r"Warning.*\Wpg_.*", r"valid PostgreSQL result", r"Npgsql\."),
    "Microsoft SQL Server": (r"Driver.* SQL[\-\_\ ]*Server", r"OLE DB.* SQL Server", r"(\W|\A)SQL Server.*Driver", r"Warning.*mssql_.*", r"(\W|\A)SQL Server.*[0-9a-fA-F]{8}", r"(?s)Exception.*\WSystem\.Data\.SqlClient\.", r"(?s)Exception.*\WRoadhouse\.Cms\."),
    "Microsoft Access": (r"Microsoft Access Driver", r"JET Database Engine", r"Access Database Engine"),
    "Oracle": (r"ORA-[0-9][0-9][0-9][0-9]", r"Oracle error", r"Oracle.*Driver", r"Warning.*\Woci_.*", r"Warning.*\Wora_.*")
}
		
	def attack(self, get, post):			
		if post != False:
			self.attackPost(post)
		if get != False:
			self.attackGet(get)
			
	def attackPost(self, post):	
		data = {} #Données à envoyer dans la page
		
		#On injecte tous les champs d'un coup
		for payload in self.payloads:
			payload = self.cleanPayload(payload)
			for key in post:
				data[key] = payload
				
			responseHtml = self.getHTML(self.url, data, "post")
			
			#On test si une injection sql est présente : recherche de message d'erreur lié à la base de données
			for databaseName in self.databaseError:
				for regex in self.databaseError[databaseName]:
					if re.search(regex, responseHtml):
						self.report.addVulnerabilityBlackBox("Injection SQL", "POST", "dans la page : "+self.url+" avec l'injection : "+payload)
		
		#On injecte champ par champ
		for payload in self.payloads:
			payload = self.cleanPayload(payload)
			for key in post:
				data = {}						
				data[key] = payload

				responseHtml = self.getHTML(self.url, data, "post")

				#On test si une injection sql est présente : recherche de message d'erreur lié à la base de données
				for databaseName in self.databaseError:
					for regex in self.databaseError[databaseName]:
						if re.search(regex, responseHtml):
							self.report.addVulnerabilityBlackBox("Injection SQL", "POST", "Dans le champ : "+key+", avec l'injection : "+payload)

	
	def attackGet(self, get):
		#On fait une copie du dictionnaire des données get
		data = get.copy()
		for payload in self.payloads:
			payload = self.cleanPayload(payload)
			for param, valeur in get.items():
				if valeur == "TEST":
					data[param] = payload
							
			response = self.getHTML(self.url, data, "get")
			
			for databaseName in self.databaseError:
				for regex in self.databaseError[databaseName]:
					if re.search(regex, response):
						self.report.addVulnerabilityBlackBox("Injection SQL", "GET", "avec l'injection : "+payload+" - Données envoyées : "+str(data))							
										
														
											#################################
											####		CLASSE XSS
											#######__________________________

class Xss(Blackbox):
	def __init__(self, url, options, site, report):
		Blackbox.__init__(self, url, options, site, report)
		self.payloads = open("attack"+os.sep+"BlackBox"+os.sep+"Payloads"+os.sep+"xss.txt").readlines()
		self.report = report
		self.scriptOk = ["alert('__XSS__')", "alert(\"__XSS__\")", "String.fromCharCode(0,__XSS__,1)"]
		
	def attack(self, get, post):
		self.attackGet(get)
		
		if post != False:
			self.attackPost(post)		
		
	def attackGet(self, get):
		"""
		Tout d'abord, on génère un "flag" qui est une chaine de 10 caractères aléatoires
		On injecte ce flag dans la page, on analyse la réponse
		Si dans la réponse, on retrouve le flag, alors les données envoyées par l'utilisateur sont réaffichées à l'écran -> une injection XSS est peut être possible
		On génére alors des payloads en fonction de l'endroit où les données sont injectées
		Puis on cherche si il y a une injection XSS ou non	
		"""
		url = self.url
		
		if url[-1] != "/":
			url = url+"/"
			
		#Si pas de parametres GET en URL
		if get == False:	
			#Génération du flag unique
			flag = self.generateFlag()
			#On injecte le flag
			response = self.getHTML(url+flag, None, None)
			#On regarde s'il apparait dans la réponse HTML
			if flag in response:
				#On génére les payloads en fonction de l'endroit dans la page de l'injection
				payloads = self.generatePayloads(response, flag)
				if payloads != []:
					#On recherche une XSS
					self.findXSS(url, {}, "", flag, "get", payloads)
					
		#Si il y a des paramètres GET
		else:
			for key in get:
				#On fait une copie du dictionnaire contenant les informations GET pour le garder intact
				data = get.copy()
				if value == "TEST":					
					flag = self.generateFlag()
					data[param] = flag				
					response = self.getHTML(url, data, "get")
				
					if flag in response:
						payloads = self.generatePayloads(response, flag)
						if payloads != []:
							self.findXSS(url, data, key, flag, "get", payloads)
			
	def attackPost(self, post):
		for key in post:
			data = post.copy()
			flag = self.generateFlag()
			data[key] = flag
			response = self.getHTML(self.url, data, "post")
			
			if flag in response:
				payloads = self.generatePayloads(response, flag)
				if payloads != []:
					self.findXSS(self.url, data, key, flag, "post", payloads)
			
	def generateFlag(self):
		return "".join([random.choice("0123456789abcdefghijklmnopqrstuvwxyz") for i in range(0,10)])
		
	def generatePayloads(self, data, flag):
		soup = BeautifulSoup.BeautifulSoup(data)
		e = []
		self.study(soup, keyword=flag, entries=e)
		
		payloads = []
		
		for element in e:
			payload = ""
			
			if element['type'] == "attrval":
				i0 = data.find(flag)
				try:
					i1 = data[:i0].rfind(element['name'])
				except UnicodeDecodeError:
					continue
					
				start = data[i1:i0].replace(" ", "")[len(element['name']):]
				if start.startswith("='"): payload = "'"
				if start.startswith('="'): payload = '"'
				if element['tag'].lower() == "img":
					payload += "/>"
				else:
					payload += "></"+element['tag']+">"
					
				for xss in self.payloads:
					payloads.append(payload + xss.replace("__XSS__", flag))
					
			elif element['type'] == "attrname":
				if code == element['name']:
					for xss in self.payloads:
						payloads.append('>' + xss.replace("__XSS__",flag))

			elif element['type'] == "tag":
				if elem['value'].startswith(code):
					for xss in self.payloads:
						payloads.append(xss.replace("__XSS__", flag)[1:])
				else:
					for xss in self.payloads:
						payloads.append("/>" + xss.replace("__XSS__", flag))

			elif element['type'] == "text":
				payload = ""
				if element['parent'] == "title": 
					payload = "</title>"

				for xss in self.payloads:
					payloads.append(payload + xss.replace("__XSS__", flag))
				return payloads

			data = data.replace(flag, "none", 1)
			
		return payloads			
			
			
	def study(self, soup, parent=None, keyword="", entries=[]):
		#if parent==None:
			#print "Keyword is:",flag
		if str(soup).find(keyword)>=0:
			if isinstance(soup,BeautifulSoup.Tag):
				if str(soup.attrs).find(keyword)>=0:
					for tagName, value in soup.attrs:
						if value.find(keyword)>=0:
							#print "Found in attribute value ",tagName,"of tag",soup.name
							entries.append({"type":"attrval", "name":str(tagName), "tag":str(soup.name)})
						if tagName.find(keyword)>=0:
							#print "Found in attribute name ",tagName,"of tag",soup.name
							entries.append({"type":"attrname", "name":str(tagName), "tag":str(soup.name)})
				elif soup.name.find(keyword)>=0:
					#print "Found in tag name"
					entries.append({"type":"tag", "value":str(soup.name)})
				else:
					for x in soup.contents:
						self.study(x, soup, keyword, entries)
			elif isinstance(soup,BeautifulSoup.NavigableString):
				if str(soup).find(keyword)>=0:
					#print "Found in text, tag", parent.name
					entries.append({"type":"text", "parent":str(parent.name)})
					
	def validXSS(self, response, flag):
		if response == "" or response == None:
			return False
		soup = BeautifulSoup.BeautifulSoup(response)
		for element in soup.findAll("script"):
			if element.string != None and element.string in [t.replace("__XSS__", flag) for t in self.scriptOk]:
				return True
			elif element.has_key("src"):
				if element["src"] == "http://__XSS__/x.js".replace("__XSS__", flag):
					return True
		return False
		
		
	def findXSS(self, page, args, var, flag, typeRequete, payloads):
		param = args.copy()
		url = page
		
		for payload in payloads:
			payload = self.cleanPayload(payload)
			if param == {}:
				responseHtml = self.getHTML(url+"?"+urllib.quote(payload), None, None)
			else:
				param[var] = payload
				
				if typeRequete == "post":
					responseHtml = self.getHTML(url, param, "post")
				elif typeRequete == "get":
					responseHtml = self.getHTML(url, param, "get")
			
			if self.validXSS(responseHtml, flag):
				if param == {}:
					self.report.addVulnerabilityBlackBox("XSS", typeRequete.upper(), "dans la page : "+url+" avec l'injection : "+payload)
					break
				else: 
					self.report.addVulnerabilityBlackBox("XSS", typeRequete.upper(), "dans le paramètre : "+var+" avec l'injection : "+payload)
					break
				
			#Cette fois ci on injecte nos payloads sans les encoder	
			if param == {}:
				responseHtml = urllib2.urlopen(url+"?"+payload)
			else:
				param[var] = payload
				
				if typeRequete == "post":
					responseHtml = urllib2.urlopen(url, param)
				elif typeRequete == "get":
					responseHtml = urllib2.urlopen(url, param)
			
			if self.validXSS(responseHtml, flag):
				if param == {}:
					self.report.addVulnerabilityBlackBox("XSS", typeRequete.upper(), "dans la page : "+url+" avec l'injection : "+payload)
					break
				else: 
					self.report.addVulnerabilityBlackBox("XSS", typeRequete.upper(), "dans le paramètre : "+var+" avec l'injection : "+payload)
					break
