#for reading and parsing the Google search data
import urllib
import simplejson

def get_urls(search, num):
    for x in range(int(num/4)):
        query = urllib.urlencode({'q':search})
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s'\
            % (query)
        url += '&start='+str(x*4)
        search_results = urllib.urlopen(url)
        json = simplejson.loads(search_results.read())
        results = json['responsedata']['results']
        for i in results:
            yield i['url']
    
print [x for x in get_urls("TEST",10)]
