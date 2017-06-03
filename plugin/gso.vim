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

vim.current.buffer.append('')
for elem in root.iter():
    #if elem.tag == u'p' or elem.tag == u'code':
    for line in str(elem.text).split('\n'):
        if line != "None":
            vim.current.buffer[-1] += line
    for line in str(elem.tail).split('\n'):
        if line != "None":
            vim.current.buffer[-1] += (line)

EOF

endfunction

command! -nargs=1 GSO call GSO(question)

