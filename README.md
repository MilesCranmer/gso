****Currently Google no longer supports the SOAP API for search, so GSO is being recoded!

# GSO : Googling Stack Overflow

Devpost project [link](http://devpost.com/software/stack-of-py)


Working Python Script + Semi-working Sublime Text 2 plugin to quickly load stack overflow code from a google search, using a selection or user-entered query.

This project is in pre-alpha/alpha stage, but with the correct configuration, can still get the job done!

To install, install the library pygoogle to your path (eg. with pip).
standalone.py can be run from the command line with three args (a string, an integer>0 or real between 0 and 1, and a bool):
"search string" number_of_pages verbose?
Enjoy it, send me questions, help improve!

#Plugin specific:

(plugins not complete)
Vim:

Add the following to your .vimrc to set F5 as your key to toggle GSO.

noremap <F5> :GSOToggle<CR>

Sublime 2:
Next, copy "stack.py" into your sublime packages folder (create new plugin to see where this goes).
Finally, create a new keyboard shortcut which calls the command "searchtext".
