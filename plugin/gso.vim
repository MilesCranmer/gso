function! GSO(...)

let all_args=a:000

python << EOF

import vim
import os
from io import BytesIO
from lxml import etree
from gso import load_up_answers, load_up_questions

question = " ".join([str(word) for word in vim.eval("all_args")])
starting_line = vim.current.window.cursor[0]
current_line = starting_line

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
    known_text_tags = [
        u'pre', u'code', u'p', u'kbd',
        u'a', u'li', u'em', u'ol', u'strong'
    ]
    if elem.tag not in known_text_tags:
        continue
    inline_text_tags = [
        u'code', u'kbd', u'a', u'em', u'strong'
    ]
    if elem.tag not in inline_text_tags:
        vim.current.buffer.append('', current_line+1)
        current_line += 1

    if elem.tag == u'pre':
        inside_pre_tag = True
    for line in str(elem.text).split('\n'):
        if line != "None":
            vim.current.buffer[current_line] += line
	    if elem.tag == u'code' and inside_pre_tag == True:
                vim.current.buffer.append('', current_line+1)
                current_line += 1
    for line in str(elem.tail).split('\n'):
        if line != "None":
            vim.current.buffer[current_line] += line
    if elem.tag == u'code' and inside_pre_tag == True:
        inside_pre_tag = False

EOF

endfunction

command! -nargs=* GSO call GSO(<f-args>)

