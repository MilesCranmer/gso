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
import argparse
from io import BytesIO
from lxml import etree
from gso import load_up_answers, load_up_questions

# ["___", "____"] - interpreted as block comment
# "___" - interpreted as single-line comment
comments = {
    'python': ["\"\"\"", "\"\"\""],
    'haskell': ["{-", "-}"],
    'cpp': ["/*", "*/"],
    'c': ["/*", "*/"],
    'java': ["/*", "*/"],
    'rust': ["/*", "*/"],
    'php': ["/*", "*/"],
    'javascript': ["/*", "*/"],
    'ruby': ["=begin", "=end"],
    'perl': ["=begin", "=cut"],
    'tex': "%",
    'plaintex': "%",
    'latex': "%",
    'html': ["<!--", "-->"]
}

# Some filetypes from vim 
# should be searched with a different
# name.
search_mapping = {
    'cpp': 'C++'
}


"""Load up options"""

all_args = vim.eval("all_args")

"""Get default language"""
curr_lang = ""
try:
    curr_lang = vim.current.buffer.vars['current_syntax']
except:
    pass

"""Text turned on?"""
no_text = False

"""Create parser for args"""
parser = argparse.ArgumentParser(description="Process a search query")

parser.add_argument(
    '-l', '--lang', default=curr_lang, help="Set the language explicitly")
parser.add_argument(
    '-n', '--no-text', action='store_true', default=False,
    help="Don't print the answer text")
parser.add_argument('search', nargs='+', help="The search keywords")

"""Parse!"""
gso_command = vars(parser.parse_args(all_args))

curr_lang = gso_command['lang']
no_text = gso_command['no_text']
question = gso_command['search']

"""Now all the options are loaded"""

starting_line = vim.current.window.cursor[0]
current_line = starting_line

results = []
i = 0

# Should we search it with a different name?
search_lang = curr_lang
if curr_lang in search_mapping:
    search_lang = search_mapping[curr_lang]

for result in load_up_questions(str(question), search_lang):
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


# Inside a code block
inside_pre_tag = False
# Inside a comment block
inside_comment = False

block_comments_enabled = False
if curr_lang in comments and len(comments[curr_lang]) == 2:
    block_comments_enabled = True

#Mark the start of input
if block_comments_enabled:
    vim.current.buffer.append(
        comments[curr_lang][0]+"GSO>>>"+comments[curr_lang][1],
        current_line)
elif curr_lang in comments:
    vim.current.buffer.append(
        comments[curr_lang]+"GSO>>>",
        current_line)
else:
    vim.current.buffer.append(
        "GSO>>>", current_line)

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

    if elem.tag == u'pre':
        inside_pre_tag = True
    elif not inside_pre_tag and no_text:
        """No printing out text of answer"""
        continue

    if inside_comment == False and inside_pre_tag == False:
        """Do some block commenting"""
        if block_comments_enabled:
            vim.current.buffer[current_line] += comments[curr_lang][0]
            inside_comment = True
    if inside_comment == True and inside_pre_tag == True:
        """Do some block commenting"""
        if block_comments_enabled:
            vim.current.buffer.append(
                comments[curr_lang][1], current_line+1)
            current_line += 1
            inside_comment = False

    if elem.tag not in inline_tags:
        if curr_lang in comments and not block_comments_enabled:
            """Do a single line comment"""
            vim.current.buffer.append(comments[curr_lang], current_line+1)
        else:
            vim.current.buffer.append('', current_line+1)
        current_line += 1

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

if inside_comment == True:
    if block_comments_enabled:
        vim.current.buffer.append(
            comments[curr_lang][1], current_line+1)
        current_line += 1
        inside_comment = False

#Mark the end of input
if block_comments_enabled:
    vim.current.buffer.append(
        comments[curr_lang][0]+"<<<GSO"+comments[curr_lang][1],
        current_line+1)
elif curr_lang in comments:
    vim.current.buffer.append(
        comments[curr_lang]+"<<<GSO",
        current_line+1)
else:
    vim.current.buffer.append(
        "<<<GSO", current_line+1)

EOF

endfunction

command! -nargs=* GSO call GSO(<f-args>)
