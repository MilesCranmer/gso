## Currently Google no longer supports the SOAP API for search, so GSO will have to be recoded to work.
## I would like to rewrite this using the official [StackExchange API](https://api.stackexchange.com/), which should be a cleaner way to do things.

# GSO : Googling Stack Overflow

Much of the time you spend coding is Googling things, and dumping other's code into your editor. Wouldn't it be great if you could have that process integrated into your environment? Or even done automatically for you?

This is the goal of GSO.

## Devpost project [link](http://devpost.com/software/stack-of-py)

Working Python Script + Semi-working Sublime Text 2 plugin to quickly load stack overflow code from a google search, using a selection or user-entered query.

To install, install the library pygoogle to your path (eg. with pip).
standalone.py can be run from the command line with three args (a string, an integer>0 or real between 0 and 1, and a bool):
"search string" number_of_pages verbose
Enjoy it, send me questions, help improve

#Plugin specific:

Sublime 2:
Copy "stack.py" into your sublime packages folder (create new plugin to see where this goes).
Finally, create a new keyboard shortcut which calls the command "searchtext".

*Eventually, I would like to make a vim plugin to do all of this. It would seriously speed up the development process.*
