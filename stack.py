import sublime, sublime_plugin
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__),"xgoogle"))#/site-packages/xgoogle-1.3-py2.7.egg/xgoogle')

from search import GoogleSearch, SearchError

class ExampleCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.insert(edit,0,"test")

class SearchtextCommand(sublime_plugin.TextCommand):
	def run(self,edit):
		language = self.view.settings().get('syntax').split('/')[1]
		sels = self.view.sel()
		#if some text selected:
		if sum([len(self.view.substr(sel)) for sel in sels]) > 0:
			words = language + ' '
			for sel in sels:
				words += self.view.substr(sel).replace('\n',' ').replace('\t','') + ' '
			self.view.window().show_input_panel('Search',words + ' how to ',
				self.searchtext,None,None)

		#no text selected:
		else:
			#get text from user
			self.view.window().show_input_panel('Search',language + ' ',
				self.searchtext,None,None)

	def searchtext(self, user_input):
		searchterms = user_input + ' site:stackoverflow.com'
		sublime.status_message("Searching: " + searchterms)
		try:
			sublime.status_message("searching...")
			gs = GoogleSearch(searchterms)
			gs.results_per_page = 50
			results = gs.get_results()
			for res in results:
				sublime.status_message(res.url.encode('utf8'))
				print
		except SearchError, e:
			 sublime.status_message("Search failed: %s" % e)



#class Search(sublime_plugin.TextCommand):
#	def run(self,edit):
