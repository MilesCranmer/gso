import sublime, sublime_plugin
import urllib2
from HTMLParser import HTMLParser
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__),"xgoogle"))#/site-packages/xgoogle-1.3-py2.7.egg/xgoogle')

from search import GoogleSearch, SearchError



class MyHTMLParser(HTMLParser):
	def starttag(self,tag,attrs):
		if tag == 'div':
			sublime.status_message(attrs)
		

class SearchtextCommand(sublime_plugin.TextCommand):
	def run(self,edit):
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
			myParser = MyHTMLParser()
			sublime.status_message("searching...")
			gs = GoogleSearch(searchterms)
			gs.results_per_page = 10
			results = gs.get_results()
			for res in results:
				url = res.url.encode('utf8')
				sublime.status_message(url)
				html = urllib2.urlopen(url).read()
				myParser.feed(html)
		except SearchError, e:
			 sublime.message_dialog("Search failed: %s" % e)



#class Search(sublime_plugin.TextCommand):
#	def run(self,edit):
