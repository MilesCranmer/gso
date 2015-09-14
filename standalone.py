#This file was originally created by Miles Cranmer (miles.cranmer@gmail.com)
#This sublime plugin googles stack overflow, and implements the code at 
#the user's direction. 
#The code here is licensed under the MIT license. API's referenced here
#have their own licenses.
#sublime plugin api
import sys
#load web pages
import urllib2
#get google search results
from pygoogle import pygoogle
#parse stackoverflow page
from HTMLParser import HTMLParser

#parses stack overflow page
class MyHTMLParser(HTMLParser):
	code_flag = 0
	curr_snip = ''
	curr_snips = []
	curr_comment = ''
	snips = []
	answers = 0
	#look for tag
	def handle_starttag(self,tag,attrs):
		#if td tag and we are not close to the code yet
		if self.code_flag == 0 and tag == 'td':
			for attr in attrs:
				#make sure max 2 answers per page
				if self.answers < 2:
					#only load answer
					if attr == ('class','answercell'):
						self.answers += 1
						self.code_flag = 1
		if self.code_flag > 0 and tag == 'div':
			for attr in attrs:
				#may have tags...
				if attr == ('class', 'post-menu'):
					self.code_flag = 0
					if len(self.curr_snips) > 0:
						self.snips.append([self.curr_snips,self.curr_comment])
					self.curr_snips = []
					self.curr_comment = ''
					self.curr_snip = ''
		#close to code
		if self.code_flag==1 and tag == 'pre':
			self.code_flag = 2
		#in the code
		if self.code_flag==2 and tag == 'code':
			self.code_flag = 3
	def handle_data(self,data):
		#in the answer
		if self.code_flag > 0:
			#add bulk answer code
			self.curr_comment += data
		#in the code
		if self.code_flag > 2:
			#add only the code
			self.curr_snip += data
			#print data
	def handle_endtag(self,tag):
		if self.code_flag > 0 and tag == 'code':
			if len(self.curr_snip) > 0:
				self.curr_snips.append(self.curr_snip)
				self.curr_snip = ''
			self.code_flag = 1

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def IDsIn (sof_html):
	x = sof_html.replace('&gt;', '3cmr93iwm0c9ri3w0')
	x = x.replace('&lt;','98jdsf98j3oisdf')
	x = x.replace('&amp;','dksljf9w8ejfosidjf')
	return x

def IDsOut (string):
	x = string.replace('98jdsf98j3oisdf','<')
	x = x.replace('3cmr93iwm0c9ri3w0','>')
	x = x.replace('dksljf9w8ejfosidjf','&')
	return x

def getNPages(searchterms, N):
	myParser = MyHTMLParser()
	len_modifer = 0
	searchterms += ' site:stackoverflow.com'
	print "Searching:", searchterms
	g = pygoogle(searchterms)
	modifer = 0
	if N < 1:
		g.pages = 1
	else:
		g.pages = N
	urls = g.get_urls()
	#can do less than a page too!
	if N < 1:
		urls = urls[:max([int(len(urls)*N),1])]
	#go through search results
	for url in urls:
		req = urllib2.Request(url, headers = hdr)
		try:
			myParser.answers = 0
			page = urllib2.urlopen(req)
			html = page.read()
			#IDs for unusual characters
			myParser.feed(IDsIn(html))
			snips = myParser.snips
			#print snips
			for x in snips:
				comment = IDsOut(x[1])
				for y in x[0]:
					yield [IDsOut(y),comment,url]
			
			myParser.code_flag = 0
			myParser.curr_snip = ''
			myParser.curr_snips = []
			myParser.curr_comment = ''
			myParser.snips = []
			myParser.answers = 0
		except urllib2.HTTPError,e:
			print e.fp.read()

c = [x for x in getNPages("C++ how to make a linked list",0.25)]
print c[1][2]
print c[1][1]