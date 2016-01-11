#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# JavaScript booklet to find links based on CSS:
# p=[];
# var et=prompt("Type in css selector for links you wish to scrape for emails. Defaults to Arbetsf\u00f6rmedlingen.",'[id^="ctl00_mainCPH_ResultatlistaVy_Resultatlista_ct"][shape="rect"]');
# for (var i in $(et)) {p.push($(et)[i].href);}console.log(p.join(','));
#

import yagmail, re, urllib2, getpass, sys
from HTMLParser import HTMLParser

def bolder(text): return '\033[1m' + text + '\033[0m'

def question(query, default):
	if not default: raw_input(query + ': ') or sys.exit('Please write something valid.')
	else: return raw_input(query + " [" + default + "]: ") or default

print """Lets begin! To get this working, we need to know some things. Default values are in brackets []. Hit enter to use them."""

# Some of these bug unless you use raw_input without "or" statement
gmailUsername		= raw_input('Gmail username: ')
gmailPassword		= getpass.getpass('Gmail password: ')
yag = yagmail.SMTP(gmailUsername, gmailPassword)

cvLocation		= raw_input('Full file location for your CV in PDF/image format: ')
subjectContent		= question('Subject line for emails sent to employers', 'Jobb')
defaultLink		= raw_input('To find emails you have to tell us what you are looking for. Open Arbetsformedlingen, search for the jobs you want and paste the link here: ')
searchMode		= question("""Type 'once' to only search once, or type 'flow' to keep searching and sending""", 'once')


def getBody():
	with open('./email-content', 'r') as body:
		body = body.read().replace('\n', '<br>')
		if "{full-name}" in body:
			sys.exit("You have not finished the setup. First edit the file called 'email-content' and change it to suit you.")
		else:
			return body

if searchMode == 'once': print "This program will only run once."
elif searchMode == 'flow': print "This program will run until you turn it off."

allLinks, newPage, goToPage = [], '', ''

goToPage = defaultLink
class MyHTMLParser(HTMLParser):
	# Find pages to parse, and find link to next page when finished
	def handle_starttag(self, tag, attrs):
		global allLinks
		global newPage
		if tag == "a":
			for name, value in attrs:
				if name == "shape" and value == 'rect' and re.search('ctl00_mainCPH_ResultatlistaVy_Resultatlista_ct', attrs[1][1]):
					newLink = str('http://www.arbetsformedlingen.se' + attrs[3][1])
					allLinks.append(newLink)
			for name, value in attrs:
				if name == 'title' and re.search('sida', value) and re.search('till\sn', value):
					newPage = attrs[1][1]

def blacklist(email):
	contact = email.lower()
	with open('./blacklist', 'r+') as blacklist:
		if not contact in blacklist.read().splitlines():
			blacklist.write(contact + '\n')
			sendemail(email)
			print "Email sent to: " + email + " and added to blacklist."
		else:
			print "Email was already blacklisted: " + email

def sendemail(toEmail):
	body = str(getBody())
	yag.send(to = toEmail, subject = subjectContent, contents = [body, cvLocation])

def visitURL(url):
	a = urllib2.urlopen(url)
	b = a.read(a)
	return b

def getEmailsFromURL(url):
	a = visitURL(url)
	b = list(set(re.findall(r'[\w\.-]+@[\w\.-]+\.[\w]+',  a)))
	if len(b): print "..."
	return b

def findEmails():
	emailList, emailResults = [], []
	global goToPage
	del allLinks[:] # Start from scratch on every page
	
	parser = MyHTMLParser()
	parser.feed(visitURL(goToPage))

	for website in allLinks:
		emailList = getEmailsFromURL(website)
		emailResults = emailResults + emailList

	emailResults = list(set(emailResults)) # Remove dupes
	print "These are all the emails found " + "(" + str(len(emailResults)) + "): " + ", ".join(emailResults)

	for email in emailResults: blacklist(email)

	if searchMode == 'flow':
		goToPage = 'http://www.arbetsformedlingen.se/' + newPage
		print "Searching new page..."
		findEmails()
	else: print "Finished with everything, I will quit now."

testFirst = raw_input('Do you want to test that your email looks OK by emailing yourself once? If so, write your email here, or hit enter to continue anyway: ')
if testFirst:
	sendemail(testFirst)
	print "Please check your email before continuing"

a = raw_input('Please confirm that you want to start sending emails, by writing YES in capital letters: ')
if a == "YES": findEmails()
else: sys.exit('Okay. Bye!')
