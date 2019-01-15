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

so_superuser = stackexchange.Site(
    stackexchange.SuperUser,
    app_key=SE_KEY)

so_unix = stackexchange.Site(
    stackexchange.UnixampLinux,
    app_key=SE_KEY)

so_tex = stackexchange.Site(
    stackexchange.TeXLaTeX,
    app_key=SE_KEY)

for site in [so, so_superuser, so_unix, so_tex]:
    site.impose_throttling = True
    site.throttle_stop = False

def load_up_questions(question, language='', answers=5):
    """ Load up stack overflow questions from a query

    Args:
        
        question: String question, what you would google for

        language: (optional) specific language inferred from filename

        answers: (optional, default 5) the number of answers to load
            
    Yields:
        
        lists of strings:
            0: URL to question
    """
    query = search_google(question, language=language)
    results = query[u'items']
    for result in results:
        url = result[u'link']
        yield [url]

def load_up_answers(URL):
    """ Load answers from a stack overflow URL

    Args:

        URL: string of the url for the question (https:...)

    Returns:

        List of [score, body], where the body is html
    """

    split_url = URL.split('/')
    domain = split_url[2]
    site = {
        'unix.stackexchange.com': so_unix,
        'tex.stackexchange.com': so_tex,
        'superuser.com': so_superuser,
        'stackoverflow.com': so}[domain]
    question_id = split_url[4]
    answer_pointers = site.question(question_id).answers

    answer_pointers.sort(key=lambda x: x.score)
    answer_pointers = list(reversed(answer_pointers))

    answer_ids = [answer.id for answer in answer_pointers]
    # Only look at the first answer
    answer_ids = [answer_ids[0]]

    answer_objs = [
        site.answer(
            answer_id,
            body=True,
            score=True) for answer_id in answer_ids]

    answers = [
        [answer.score,
         answer.body] for answer in answer_objs]

    return answers

