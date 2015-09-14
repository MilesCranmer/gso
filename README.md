# GSO : Googling Stack Overflow
Working Python Script + Semi-working Sublime Text 2 plugin to quickly load stack overflow code from a google search, using a selection or user-entered query.

This project is in pre-alpha/alpha stage, but with the correct configuration, can still get the job done!

To install, install the library pygoogle to your path (eg. with pip).
Next, copy this folder into your sublime packages folder (create new plugin to see where this goes).
Finally, create a new keyboard shortcut which calls the command "searchtext".
Enjoy it, send me questions, help improve!

#Plugin specific:

(plugins not complete)
Vim:

Add the following to your .vimrc to set F5 as your key to toggle GSO.

noremap <F5> :GSOToggle<CR>
