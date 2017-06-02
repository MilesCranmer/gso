""" This file organizes the different answers from each query result to load
"""

import os

import stackexchange
from pprint import pprint
from gso import search_google

SE_KEY = os.environ["SE_KEY"]

so = stackexchange.Site(
    stackexchange.StackOverflow,
    app_key=SE_KEY)

so.impose_throttling = True
so.throttle_stop = False

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

    Args:

        URL: string of the url for the question (https:...)

    Returns:

        List of [score, body], where the body is html
    """

    split_url = URL.split('/')
    site = split_url[3]
    question_id = split_url[4]
    answer_pointers = so.question(question_id).answers

    answer_pointers.sort(key=lambda x: x.score)
    answer_pointers = list(reversed(answer_pointers))

    answer_ids = [answer.id for answer in answer_pointers]
    if len(answer_ids) >= 3:
        answer_ids = answer_ids[:3]

    answer_objs = [
        so.answer(
            answer_id,
            body=True,
            score=True) for answer_id in answer_ids]

    answers = [
        [answer.score,
         answer.body] for answer in answer_objs]

    return answers

