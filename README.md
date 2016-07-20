****Currently Google no longer supports the SOAP API for search, so GSO is being recoded

# GSO : Googling Stack Overflow

Devpost project [link](http://devpost.com/software/stack-of-py)


Working Python Script + Semi-working Sublime Text 2 plugin to quickly load stack overflow code from a google search, using a selection or user-entered query.

To install, install the library pygoogle to your path (eg. with pip).
standalone.py can be run from the command line with three args (a string, an integer>0 or real between 0 and 1, and a bool):
"search string" number_of_pages verbose
Enjoy it, send me questions, help improve

#Plugin specific:

(plugins not complete)

Sublime 2:
Copy "stack.py" into your sublime packages folder (create new plugin to see where this goes).
Finally, create a new keyboard shortcut which calls the command "searchtext".
