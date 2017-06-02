import os
from gso import load_up_answers, load_up_questions

#for result in load_up_questions("How to write a bubble sort", "python"):
    #print result
    #break

question_url = 'https://stackoverflow.com/questions/895371/bubble-sort-homework'


print load_up_answers(question_url)

