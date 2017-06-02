function! GSO()

python << EOF

import vim

import os
import pickle as pkl
from io import BytesIO
from lxml import etree
from gso import load_up_answers, load_up_questions

#for result in load_up_questions("How to write a bubble sort", "python"):
    #print result
    #break

#question_url = 'https://stackoverflow.com/questions/895371/bubble-sort-homework'

#with open("html_dump.pkl", 'wb') as myfile:
    #pkl.dump(load_up_answers(question_url), myfile)

html_dump = []
with open("../html_dump.pkl", 'rb') as myfile:
    html_dump = pkl.load(myfile)

def wrap_with_root_tag(xml_string):
    xml_string = u"<root>"+xml_string+u"</root>"
    return xml_string

root = etree.iterparse(BytesIO(wrap_with_root_tag(html_dump[0][1]).encode('utf-8')))
for action, elem in root:
    if elem.tag == u'p' or elem.tag == u'code':
	for line in str(elem.text).split('\n'):
            vim.current.buffer.append(line)

EOF

endfunction
