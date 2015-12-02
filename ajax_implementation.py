#for reading and parsing the Google search data
import urllib
import simplejson

def get_urls(search):
    query = urllib.urlencode({'q':search})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s'\
    % (query)
    search_results = urllib.urlopen(url)
    json = simplejson.loads(search_results.read())
    results = json['responseData']['results']
    for i in results:
        yield i['url']
    

