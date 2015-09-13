#This file was originally created by Miles Cranmer (miles.cranmer@gmail.com)
#This sublime plugin googles stack overflow, and implements the code at 
#the user's direction. 
#The code here is licensed under the MIT license. API's referenced here
#have their own licenses.
import sublime, sublime_plugin
import sys
sys.path.append('/Library/Python/2.7')
sys.path.append('/Library/Python/2.7/site-packages')
sys.path.append('/Library/Python/2.7/site-packages/pygoogle-0.1-py2.7.egg-ingo')
import urllib2
from pygoogle import pygoogle
from HTMLParser import HTMLParser

starter = {'C++':'/*','Python':'\"\"\"','Haskell':'{-','Java':'/*','Ruby':'=begin'}
ender = {'C++':'*/','Python':'\"\"\"','Haskell':'-}','Java':'*/','Ruby':'=end'}

#parses stack overflow page
class MyHTMLParser(HTMLParser):
	code_flag = 0
	curr_snip = ''
	curr_snips = []
	curr_comment = ''
	snips = []
	divs = 0
	answers = 0
	def handle_starttag(self,tag,attrs):
		if self.code_flag == 0 and tag == 'td':
			for attr in attrs:
				if self.answers < 2:
					if attr == ('class','answercell'):
						self.answers += 1
						self.code_flag = 1
						self.divs = 1
		if self.code_flag > 0 and tag == 'a':
			for attr in attrs:
				if attr == ('class', 'suggest-edit-post'):
					self.code_flag == 0
					if len(self.curr_snips) > 0:
						self.snips.append([self.curr_snips,self.curr_comment])
					self.curr_snips = []
					self.curr_comment = ''
					self.curr_snip = ''
					self.divs = 0
		if self.code_flag > 0 and tag == 'div' and self.divs > 0:
			self.divs += 1
		#close to code
		if self.code_flag==1 and tag == 'pre':
			self.code_flag = 2
		#in the code
		if self.code_flag==2 and tag == 'code':
			self.code_flag = 3
	def handle_data(self,data):
		#in the answer
		if self.code_flag > 0:
			self.curr_comment += data
		#in the code
		if self.code_flag > 2:
			self.curr_snip += data
			#print data
	def handle_endtag(self,tag):
		if self.code_flag > 0 and tag == 'code':
			if len(self.curr_snip) > 0:
				self.curr_snips.append(self.curr_snip)
				self.curr_snip = ''
			self.code_flag = 1
		if self.code_flag > 0 and tag == 'div' and self.divs > 0:
			self.divs -= 1

			if self.divs == 0:
				#done answer
				self.code_flag = 0
				if len(self.curr_snips) > 0:
					self.snips.append([self.curr_snips,self.curr_comment])
				self.curr_snips = []
				self.curr_comment = ''
				self.curr_snip = ''

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

class ExampleCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.insert(edit, 0, "Hello, World!")

class SearchtextCommand(sublime_plugin.TextCommand):
	snips = ["lele"]
	myParser = MyHTMLParser()
	editor = 0
	me = 1
	language = 0
	def run(self, edit):
		self.language = self.view.settings().get('syntax').split('/')[1]
		self.editor = edit
		language = self.language
		sels = self.view.sel()
		#if some text selected:
		if sum([len(self.view.substr(sel)) for sel in sels]) > 0:
			words = language + ' '
			for sel in sels:
				words += self.view.substr(sel).replace('\n',' ').replace('\t','') + ' '
			self.view.window().show_input_panel('Search',words + ' how to ',
				self.searchtext,None,None)
		else:
			self.view.window().show_input_panel('Search',language+' how to ',
				self.searchtext,None,None)

	def searchtext(self, user_input):
		searchterms = user_input + ' site:stackoverflow.com'
		print "Searching:", searchterms
		g = pygoogle(searchterms)
		g.pages = 1
		urls = g.get_urls()
		for url in urls[:int(len(urls)/4+0.5)]:
			req = urllib2.Request(url, headers = hdr)
			try:
				self.myParser.answers = 0
				page = urllib2.urlopen(req)
				html = page.read()
				html_fixed = html.replace('&gt;',' ')
				html_fixed = html_fixed.replace('...',' ')
				self.myParser.feed(html_fixed)
				self.snips = self.myParser.snips
				#print self.snips
				for x in self.snips:
					for y in x[0]:
						answer = sublime.ok_cancel_dialog(y)
						if answer == 1:
							self.view.insert(self.editor,
								self.view.sel()[0].begin(),y)
							if self.language in starter:
								self.view.insert(self.editor,
									self.view.sel()[0].begin(),"\n\n"+starter[self.language]+x[1].replace('\t',' ').replace('\n','').replace(starter[self.language],' ').replace(ender[self.language],' ')+\
									ender[self.language]+"\n\n")
							else:
								self.view.insert(self.editor,
									self.view.sel()[0].begin(),"/*"+x[1].replace('\t',' ').replace('\n','')+\
									'*/'+"\n\n")

							self.myParser.snips = []
							break
					else: 
						continue
					break
				else:
						self.myParser.snips = []
						continue
				break
			except urllib2.HTTPError,e:
				print e.fp.read()

