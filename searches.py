import urllib2
from HTMLParser import HTMLParser
from search import GoogleSearch, SearchError
from easygui import msgbox

class MyHTMLParser(HTMLParser):
	code_flag = 0
	curr_snip = ''
	curr_snips = []
	curr_comment = ''
	snips = []
	divs = 0
	answers = 0
	def handle_starttag(self,tag,attrs):
		if tag == 'div':
			if self.divs > 0:
				self.divs += 1
			for attr in attrs:
				if attr == ('class','answer accepted-answer'):
					self.divs = 1
					self.code_flag = 1
					self.answers += 1
				elif self.answers < 2 and attr == ('class', 'answer'):
					self.divs = 1
					self.code_flag = 1
					self.answers += 1
		#if self.code_flag == 1 and tag == 'td' and\
		#	attrs[0] ==('class','answercell'):
		if self.code_flag==1 and tag == 'pre':
			self.code_flag = 2
		if self.code_flag==2 and tag == 'code':
			self.code_flag = 3
	def handle_data(self,data):
		if self.divs>0:
			self.curr_comment += data
		if self.code_flag>2:
			self.curr_snip += data
			#print data
	def handle_endtag(self,tag):
		if tag == 'div' and self.divs > 0:
			self.divs -= 1
			#done!
			if self.divs == 0:
				if len(self.curr_snips) > 0:
					self.snips.append([self.curr_snips,self.curr_comment])
				self.curr_comment = ''
				self.curr_snips = []
				self.curr_snip = ''
				self.code_flag = 0
		if tag == 'code':
			if len([x for x in self.curr_snip if x.isalpha()])>=4:
				self.curr_snips.append(self.curr_snip)
			self.curr_snip = ''
			self.code_flag = 1

#headers for page request
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def search(user_input):
	myParser = MyHTMLParser()
	searchterms = user_input + ' site:stackoverflow.com'
	print("Searching: " + searchterms)
	try:
		print("searching...")
		gs = GoogleSearch(searchterms)
		gs.results_per_page = 20
		results = gs.get_results()
		for res in results:
			url = res.url.encode('utf8')
			print "downloading html from", url
			req = urllib2.Request(url,headers=hdr)
			try:
				page = urllib2.urlopen(req)
				html = page.read()
				html_fixed = html.replace('&gt;',' ')
				html_fixed = html_fixed.replace('...',' ')
				myParser.answers = 0
				myParser.feed(html_fixed)
				snips = myParser.snips
				for x in snips:
					msgbox(x[0][0])
				myParser.snips = []

			except urllib2.HTTPError,e:
				print e.fp.read()
	except SearchError, e:
		print("Search failed: %s" % e)


search("haskell how to convert string to integer")
