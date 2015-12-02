#for reading and parsing the Google search data
import urllib
import simplejson
import sys

while len(sys.argv) < 2:
    sys.argv.append('Example search')


query = urllib.urlencode({'q':sys.argv[1]})
url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s'\
    % (query)
search_results = urllib.urlopen(url)
json = simplejson.loads(search_results.read())
results = json['responseData']['results']
for i in results:
    print i['title'] + ': ' + i['url']
