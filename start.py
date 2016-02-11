#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, re, sys, traceback
from bs4 import BeautifulSoup

def writeToFile (email):
	f = open("results", "a")
	f.write(email.lower() + "\n")
	print "Writing email to results file: " + email.lower() + ""

def cleanFile():
	lines = open("results", "r").readlines()
	f  = open("results", "w")
	for line in set(lines):
		if line.strip != "":
			f.write(line)
	return "\nRemoving duplicates from results file."

#def raw_input_need (question):
#	answer = ""
#	while not answer: answer = raw_input(question)
#	return answer

def getEmails (url):
	emails = list(set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", urllib2.urlopen(url).read())))
	return [s for s in emails if not "@academicwork" in s and not "@proffice.se" in s and not "@stockholm.se" in s]

def getMode(searchMode, pageNumber):
	if searchMode == "flow":
		return "\nContinuous search (page " + pageNumber + ") ...\n"
	else:
		return "\nSingle page search...\n"

def startSearch (searchPage):
	try:
		soup = BeautifulSoup(urllib2.urlopen(searchPage).read(), "html5lib")

		try:
			nextPage	= "http://www.arbetsformedlingen.se" + soup.findAll("a", {"title": "Gå till nästa sida"})[0]["href"]
			pageNumber	= str(int(nextPage.split("sida%28")[1].split("%")[0]) - 1)
		except: nextPage, pageNumber = "", ""

		print getMode(searchMode, pageNumber)

		for link in soup.findAll("a", { "shape": "rect", "href": True, "style": True, "title": True, "id": True }):
			if "ctl00_mainCPH_ResultatlistaVy_Resultatlista_ct" in link["id"]:
				for email in getEmails("http://www.arbetsformedlingen.se" + link["href"]): writeToFile(email)

		print cleanFile()
		if searchMode == "flow" and nextPage:
			startSearch(nextPage)
		else:
			print "\nFinished! Thank you. All results saved to 'results'."
#	except: traceback.print_exc() # Debug
	except Exception, e:
		print "Something broke: %s" % e
		getSettings()

def getSettings():
	global searchPage, searchMode
	keyWords	= raw_input("\nWrite some keywords for jobs you are looking for (elektriker, diskare, etc):\n")
	keyWords	= keyWords.replace(" ", "%2B").replace("å", "%2525c3%2525a5").replace("ä", "%2525c3%2525a4").replace("ö", "%2525c3%2525b6")
	searchPage	= "http://www.arbetsformedlingen.se/For-arbetssokande/Lediga-jobb.html?url=-123388378%2FNy%2FSokPlatsannonser%2FSokPlatsannonser.aspx%3Fq%3Ds(sn(" + keyWords + ")utl(1)go(1)ao(180))%26ps%3D&sv.url=12.237ec53d11d47b612d78000171"
	searchMode	= raw_input("\nType 'flow' to search continuously, or hit enter to search a single page (20 ads per page):\n") or "once"
	startSearch(searchPage)

getSettings()
