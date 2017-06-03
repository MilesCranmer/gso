python << EOF

import sys
import vim

sys.path.insert(0, vim.eval("expand('<sfile>:p:h')"))

if "gso" in sys.modules:
    gso = reload(gso)
else:
    import gso
EOF

function! GSO(...)

let all_args=a:000

python << EOF

import vim
import os
from io import BytesIO
from lxml import etree
from gso import load_up_answers, load_up_questions

all_args = vim.eval("all_args")

"""Load up what language to scrape code from"""
lang_flag = "--lang="

if len(all_args[0]) >= len(lang_flag) and \
        all_args[0][:len(lang_flag)] == lang_flag:

    curr_lang = all_args[0][9:]
    question = " ".join([str(word) for word in all_args[1:]])

else:
    curr_lang = ""
    try:
        curr_lang = vim.current.buffer.vars['current_syntax']
    except:
        pass
    question = " ".join([str(word) for word in all_args])

starting_line = vim.current.window.cursor[0]
current_line = starting_line

results = []
i = 0
for result in load_up_questions(str(question), curr_lang):
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

# Make some space if working at end of file
vim.current.buffer.append('', current_line)

for elem in root.iter():
    known_tags = [
        u'pre', u'code', u'p', u'kbd',
        u'a', u'li', u'em', u'ol', u'strong'
    ]
    if elem.tag not in known_tags:
        continue
    inline_tags = [
        u'code', u'kbd', u'a', u'em', u'strong'
    ]
    if elem.tag not in inline_tags:
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
