""" This file defines the base query to Google.
"""
import pprint
import os
from googleapiclient.discovery import build

my_api_key = os.environ["GOOGLE_KEY"]

# A Custom Search Engine for StackOverflow, SuperUsers, TeX, and
# Unix/Linux
my_cse_id = "003962226882031433174:qk7rs-ca-bi"

def query_google(question, language=''):
    """ Search google with a question, for a language (optional)

    Args:
        
        question: String question, what you would google for

        language: (optional) specific language inferred from filename
            
    Returns:
        
        res: JSON of the query result
    """
    service = build("customsearch", "v1",
            developerKey=my_api_key)

    res = service.cse().list(
            q=question + ' ' + language,
            cx=my_cse_id,
            ).execute()
    return res
