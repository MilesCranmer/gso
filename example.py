import pprint
import os
from googleapiclient.discovery import build

my_api_key = os.environ["GOOGLE_KEY"]
my_cse_id = "003962226882031433174:qk7rs-ca-bi"

def main():
    # Build a service object for interacting with the API. Visit
    # the Google APIs Console <http://code.google.com/apis/console>
    # to get an API key for your own application.
    service = build("customsearch", "v1",
            developerKey=my_api_key)

    res = service.cse().list(
            q='How to set up linux',
            cx=my_cse_id,
            ).execute()
    pprint.pprint(res)

if __name__ == '__main__':
    main()
