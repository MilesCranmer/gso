import os
import pickle as pkl
from lxml import etree
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

def wrapper_tag(xml_string):
    xml_string = "<root>"+xml_string+"</root>"
    return xml_string

root = etree.fromstring(wrapper_tag(html_dump[0][1]))
print etree.tostring(root)
