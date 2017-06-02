""" This file organizes the different answers from each query result to load
"""

from pprint import pprint
from gso import search_google

def load_up_questions(question, language='', answers=5):
    """ Load up stack overflow questions from a query

    Args:
        
        question: String question, what you would google for

        language: (optional) specific language inferred from filename

        answers: (optional, default 5) the number of answers to load
            
    Yields:
        
        lists of strings:
            0: URL to question
            1: Title of question
            2: Short description of question
    """
    query = search_google(question, language=language)
    results = query[u'items']
    for result in results:
        url = result[u'link']
        title = result[u'pagemap'][u'qapage'][0][u'title']
        description = result[u'pagemap'][u'qapage'][0][u'description']
        yield [url, title, description]

def load_up_answers(URL):
    """ Load answers from a stack overflow URL
    """

    # The API could follow the following format:
    # The ID is semicolon-delineated
    #/2.2/questions/895371/answers?pagesize=10&order=desc&sort=votes&site=stackoverflow&filter=!SWJ_BpAceOUGGWrzdf
    # This is from the following URL
    # https://api.stackexchange.com/docs/answers-on-questions
    return

""" Here is an example output (variable: results)
from google, accidentally in html formatting

{u'cacheId': u'j9LJ7AygfC4J',
  u'displayLink': u'stackoverflow.com',
  u'formattedUrl': u'stackoverflow.com/.../bubble-sort-in-python-not-sorting-properly',
  u'htmlFormattedUrl': u'stackoverflow.com/.../&lt;b&gt;bubble&lt;/b&gt;-&lt;b&gt;sort&lt;/b&gt;-in-&lt;b&gt;python&lt;/b&gt;-not-&lt;b&gt;sorting&lt;/b&gt;-properly',
  u'htmlSnippet': u'First, if I do not specify the -f parameter, the script never runs the usage() function, &lt;br&gt;n... I can, for example, see 3998 before 403 in the list.',
  u'htmlTitle': u'algorithm - &lt;b&gt;Bubble sort&lt;/b&gt; in &lt;b&gt;Python&lt;/b&gt; not sorting properly - Stack Overflow',
  u'kind': u'customsearch#result',
  u'link': u'http://stackoverflow.com/questions/21297886/bubble-sort-in-python-not-sorting-properly',
  u'pagemap': {u'answer': [{u'text': u'First, if I do not specify the -f parameter, the script never runs the usage() function, it only tells &quot;No such file or directory: ''&quot;. Why isn't my script running the usage() function? getopt()...',
                            u'upvotecount': u'5'}],
               u'cse_image': [{u'src': u'https://cdn.sstatic.net/Sites/stackoverflow/img/apple-touch-icon@2.png?v=73d79a89bded'}],
               u'cse_thumbnail': [{u'height': u'225',
                                   u'src': u'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcS889zvWMRNB8FCxUSpJI5ZA7EV4c8Y6CqAyVf9t5S1PPqLKpwl4XHB_Q3y',
                                   u'width': u'225'}],
               u'metatags': [{u'og:image': u'https://cdn.sstatic.net/Sites/stackoverflow/img/apple-touch-icon@2.png?v=73d79a89bded',
                              u'og:type': u'website',
                              u'og:url': u'https://stackoverflow.com/questions/21297886/bubble-sort-in-python-not-sorting-properly',
                              u'twitter:app:country': u'US',
                              u'twitter:app:id:googleplay': u'com.stackexchange.marvin',
                              u'twitter:app:id:ipad': u'871299723',
                              u'twitter:app:id:iphone': u'871299723',
                              u'twitter:app:name:googleplay': u'Stack Exchange Android',
                              u'twitter:app:name:ipad': u'Stack Exchange iOS',
                              u'twitter:app:name:iphone': u'Stack Exchange iOS',
                              u'twitter:app:url:googleplay': u'http://stackoverflow.com/questions/21297886/bubble-sort-in-python-not-sorting-properly',
                              u'twitter:app:url:ipad': u'se-zaphod://stackoverflow.com/questions/21297886/bubble-sort-in-python-not-sorting-properly',
                              u'twitter:app:url:iphone': u'se-zaphod://stackoverflow.com/questions/21297886/bubble-sort-in-python-not-sorting-properly',
                              u'twitter:card': u'summary',
                              u'twitter:description': u'I have to implement bubble sort as a homework and my python script has to look for 2 command line parameters:  -f  that specifies the file path of the input file that contains a number on each line...',
                              u'twitter:domain': u'stackoverflow.com',
                              u'twitter:title': u'Bubble sort in Python not sorting properly'}],
               u'qapage': [{u'description': u'I have to implement bubble sort as a homework and my python script has to look for 2 command line parameters: -f that specifies the file path of the input file that contains a number on each line...',
                            u'image': u'https://cdn.sstatic.net/Sites/stackoverflow/img/apple-touch-icon@2.png?v=73d79a89bded',
                            u'name': u'Bubble sort in Python not sorting properly',
                            u'primaryimageofpage': u'https://cdn.sstatic.net/Sites/stackoverflow/img/apple-touch-icon@2.png?v=73d79a89bded',
                            u'title': u'Bubble sort in Python not sorting properly'}],
               u'question': [{u'answercount': u'1',
                              u'image': u'https://cdn.sstatic.net/Sites/stackoverflow/img/apple-touch-icon.png?v=c78bd457575a',
                              u'name': u'Bubble sort in Python not sorting properly',
                              u'text': u'I have to implement bubble sort as a homework and my python script has to look for 2 command line parameters: -f that specifies the file path of the input file that contains a number on each...',
                              u'upvotecount': u'0'}]},
  u'snippet': u'First, if I do not specify the -f parameter, the script never runs the usage() function, n... I can, for example, see 3998 before 403 in the list.',
  u'title': u'algorithm - Bubble sort in Python not sorting properly - Stack Overflow'}]
"""
