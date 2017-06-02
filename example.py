import pprint
import os
from googleapiclient.discovery import build

my_api_key = os.environ["GOOGLE_KEY"]
my_cse_id = "003962226882031433174"

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

results = google_search(
            'How to set up linux',
            my_api_key,
            my_cse_id,
            num=10)

for result in results:
    pprint.pprint(result)
