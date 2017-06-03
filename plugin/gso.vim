function! GSO(question)

let firstarg=a:question

python << EOF

import vim

import os
import pickle as pkl
from io import BytesIO
from lxml import etree
from gso import load_up_answers, load_up_questions

question = vim.eval("firstarg")
vim.current.buffer.append(question)

results = []
i = 0
for result in load_up_questions(str(question)):
    results.append(result)
    i += 1
    if i > 1:
        break

question_url = results[0][0]
answers = load_up_answers(question_url)

def wrap_with_root_tag(xml_string):
    xml_string = u"<root>"+xml_string+u"</root>"
    return xml_string

parser = etree.XMLParser(recover=True)
root = etree.parse(
    BytesIO(wrap_with_root_tag(answers[0][1]).encode('utf-8')),
    parser=parser)

inside_pre_tag = False

for elem in root.iter():
    vim.current.buffer.append('')
    if elem.tag == u'pre':
        inside_pre_tag = True
    for line in str(elem.text).split('\n'):
        if line != "None":
            vim.current.buffer[-1] += line
	    if elem.tag == u'code' and inside_pre_tag == True:
                vim.current.buffer.append('')
    for line in str(elem.tail).split('\n'):
        if line != "None":
            vim.current.buffer[-1] += (line)
    if elem.tag == u'code' and inside_pre_tag == True:
        inside_pre_tag = False

EOF

endfunction

command! -nargs=1 GSO call GSO(question)

