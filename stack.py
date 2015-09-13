import sublime, sublime_plugin
import urllib2
from HTMLParser import HTMLParser
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__),"xgoogle"))#/site-packages/xgoogle-1.3-py2.7.egg/xgoogle')
sys.path.append(os.path.join(os.path.dirname(__file__),"easygui"))#/site-packages/xgoogle-1.3-py2.7.egg/xgoogle')
#from easygui import msgbox
from search import GoogleSearch, SearchError
#from Tkinter import *
#print sys.builtin_module_names
#sys.argv = ['mine']
#root = Tk()
#from easygui import msgbox

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
		if self.code_flag > 2:
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
		


class SearchtextCommand(sublime_plugin.TextCommand):
	snips = ["lele"]
	myParser = MyHTMLParser()
	editor = 0
	me = 1
	def run(self,edit):
		self.editor = edit
		language = self.view.settings().get('syntax').split('/')[1]
		sels = self.view.sel()
		#if some text selected:
		if sum([len(self.view.substr(sel)) for sel in sels]) > 0:
			words = language + ' '
			for sel in sels:
				words += self.view.substr(sel).replace('\n',' ').replace('\t','') + ' '
			self.view.window().show_input_panel('Search',words + ' ',
				self.search,None,None)

		#no text selected:
		else:
			#get text from user
			self.view.window().show_input_panel('Search',language + ' how to ',
				self.search,None,None)

	def search(self, user_input):
		searchterms = user_input + ' site:stackoverflow.com'
		sublime.status_message("Searching: " + searchterms)
		try:
			sublime.status_message("searching...")
			gs = GoogleSearch(searchterms)
			gs.results_per_page = 30
			results = gs.get_results()
			sublime.status_message("downloading html")
			for res in results:
				url = res.url.encode('utf8')
				req = urllib2.Request(url,headers=hdr)
				try:
					page = urllib2.urlopen(req)
					html = page.read()
					html_fixed = html.replace('&gt;',' ')
					html_fixed = html_fixed.replace('...',' ')
					self.myParser.feed(html_fixed)
					self.snips = self.myParser.snips
					for x in self.snips:
						answer = sublime.ok_cancel_dialog(x)
						if answer == 1:
							#msgbox('lololol')
							self.view.insert(self.editor,
								self.view.sel()[0].begin(),x)
							self.myParser.snips = []
							break
					else:
							self.myParser.snips = []

				except urllib2.HTTPError,e:
					print e.fp.read()
		except SearchError, e:
			sublime.message_dialog("Search failed: %s" % e)
			sublime.status_message("")



#class Search(sublime_plugin.TextCommand):
#	def run(self,edit):
