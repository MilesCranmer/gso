import urllib2
from HTMLParser import HTMLParser
from search import GoogleSearch, SearchError

class MyHTMLParser(HTMLParser):
	code_flag = 0
	curr_snip = ''
	snips = []
	def handle_starttag(self,tag,attrs):
		if tag == 'div':
			for attr in attrs:
				if attr == ('class','answer accepted-answer'):
					self.code_flag = 1
				elif attr == ('class','answer'):
					self.code_flag = 0
		if self.code_flag==1 and tag == 'pre':
			self.code_flag = 2
		if self.code_flag==2 and tag == 'code':
			self.code_flag = 3
	def handle_data(self,data):
		if self.code_flag>2:
			self.curr_snip += data
			#print data
	def handle_endtag(self,tag):
		if tag == 'code':
			if len(self.curr_snip) > 0:
				self.snips.append(self.curr_snip)
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
	searchterms = user_input + ' site:stackoverflow.com'
	myParser = MyHTMLParser()
	print "searching "+ user_input
	try:
		print("searching...")
		gs = GoogleSearch(searchterms)
		gs.results_per_page = 50
		results = gs.get_results()
		for res in results:
			url = res.url.encode('utf8')
			print(url)
			req = urllib2.Request(url,headers=hdr)
			try:
				page = urllib2.urlopen(req)
				html = page.read()
				html_fixed = html.replace('&gt;',' ')
				html_fixed = html.replace('...',' ')
				myParser.feed(html_fixed)
			except urllib2.HTTPError,e:
				print e.fp.read()
	except SearchError, e:
		 print("Search failed: %s" % e)
	for x in myParser.snips:
		print x


search("python how to basic for loop")