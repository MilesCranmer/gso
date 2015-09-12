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