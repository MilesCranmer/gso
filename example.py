import os
import pickle as pkl
from gso import load_up_answers, load_up_questions

#for result in load_up_questions("How to write a bubble sort", "python"):
    #print result
    #break

#question_url = 'https://stackoverflow.com/questions/895371/bubble-sort-homework'

#with open("html_dump.pkl", 'wb') as myfile:
    #pkl.dump(load_up_answers(question_url), myfile)

html_dump = []
with open("html_dump.pkl", 'rb') as myfile:
    html_dump = pkl.load(myfile)

print html_dump
