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
for result in load_up_questions(str(question), "python"):
    results.append(result)
    i += 1
    if i > 1:
        break

question_url = results[0][0]
answers = load_up_answers(question_url)

def wrap_with_root_tag(xml_string):
    xml_string = u"<root>"+xml_string+u"</root>"
    return xml_string

root = etree.iterparse(BytesIO(wrap_with_root_tag(answers[0][1]).encode('utf-8')))
for action, elem in root:
    if elem.tag == u'p' or elem.tag == u'code':
        for line in str(elem.text).split('\n'):
            vim.current.buffer.append(line)

EOF

endfunction

" command! -nargs=1 GSO call GSO(question)

