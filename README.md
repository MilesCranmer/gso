# GSO
*Googling Stack Overflow*
[![Screencast](http://i.imgur.com/feBUqnJ.gif)](https://asciinema.org/a/123375)

Thank you [Daniel](https://stackoverflow.com/a/35754890/2689923),
[Brionius](https://stackoverflow.com/a/18262384/2689923),
and [bytecode77](https://stackoverflow.com/a/29915909/2689923)!

*(The newest version of GSO now also prints the answer URL.)*

## Installation

*(If you just want to try,
there are demo keys at the bottom of this page.
They are shared, so play nice.)*

Make sure your vim supports python scripting (`vim --version | grep +python` should return something). 
If this doesn't work, the `vim-nox-py2` package on ubuntu has this (`sudo apt-get install vim-nox-py2`),
else, look to [SO](https://vi.stackexchange.com/questions/10242/vim-8-0-python-support).

Then, install python dependencies:

```` 
pip install google-api-python-client Cython py-stackexchange lxml
````

If there are issues with installing `lxml`, it's probably to do with a missing `libxml` library.
The [`lxml`](http://lxml.de/installation.html) site has some help for this.

Get API keys for [Google Custom Search](https://developers.google.com/custom-search/json-api/v1/overview)
(scroll to API key), and [Stack Apps](https://stackapps.com/apps/oauth/register). 
This is free, don't be intimidated by the forms!
Enter *whatever* in the boxes, and the key generated for you will be compatible with this app.
Trust me, it's worth it.

Put these into
environment variables `GOOGLE_KEY` and
`SE_KEY`, respectively (e.g., `export GOOGLE_KEY="......"`).

(Vundle) Add this repo to your `.vimrc` file:

````
Plugin 'MilesCranmer/gso'
````

Then, just `:PluginInstall` in vim.

**(optional)** Map Ctrl-E to type ":GSO " for you, by putting the following in your `.vimrc`:
```vim
nnoremap <C-e> :GSO 
```

Usage
-----

````
:GSO [(-l | --language) <language>] [-n | --no-text] [<search>...]
````


For example, in a file `sort.py`, run:

````
:GSO Do a bubble sort
````

And watch the python code get dumped below your cursor.
GSO will append the language to your query by the file extension, but you can set it explicitly by:

````
:GSO -l haskell Generate a fibonacci sequence
````

FAQ
---

- The Python compiled into my vim is saying it can't see googleapi-client, what do I do?

I have a similar problem and made a hack around it. Your gso should be installed into ~/.vim/gso. Edit the file ~/.vim/gso/plugin/gso.vim, and after each `python << EOF`, paste the following lines:

```
import sys
sys.path.append('....')
```

Replace the inside of the string with the "site-packages" directory where googleapi-client is installed. Make sure you use python2.7 to install the packages, or optionally replace the `python << EOF` with `python3 << EOF`.

## Tools

There is a shell utility in `tools`. It simply calls the GSO command and dumps the result to the /dev/stdout.
Copy it to `/usr/bin/gso` (or anywhere on the `PATH`), then call it as you normally would:

```bash
➜  gso How to change the url of a git remote

GSO>>>
You can
git remote set-url origin git://new.url.here


(see git help remote) or you can just edit .git/config and change the 
URLs there. You're not in any danger of losing history unless you do 
something very silly (and if you're worried, just make a copy of your 
repo, since your repo is your history.)
<<<GSO
```

Docker
------

To pull and run (with your Google and Stack apps API keys, or the demo ones at the bottom):

```` 
docker run -it -e GOOGLE_KEY=$GOOGLE_KEY -e SE_KEY=$SE_KEY mcranmer/gso
````

Then, inside vim:

```` 
:GSO Flatten a list of lists
````

And it will dump the highest score answer to below your cursor.

# TODO/Ideas

- Unit tests. Apparently these are uncommon among vim plugins, so there is little built-in testing functionality, but since I am using a lot of python, I could just write regular python `unittests` on the `gso` module.
- Automatic reading of code, triggered by a flag, so that you can dump the current line of code to the search query to help your results. This way, it's a little bit like an advanced `man` function.
- Automatic piping of error messages to GSO, have it dump a solution to your error in the code. This might have to be linked to the build command, e.g., make. Then, if make produces a nonzero error message, you activate GSO at the cursor position. This could be something you toggle on and off. It could also just be called, e.g., by an empty :GSO command after an error. You could also add functionality to turn specific errors off if they are too basic (e.g., forgetting a semi-colon), or too common (e.g., generic seg fault).
- (#1 TODO) **Multi answer/multi question, as well as easy keystroke swapping. This would have GSO load up a bunch of answers/questions to the quickfix list, then you could use unimpaired.vim to quickly replace the pasted text below your cursor.**
- Answer preview, so you can see answers in a new pane, and swipe between them until you like one. Then you could hit some keystroke to dump it in.
- General speedups (though this isn't really needed on an AWS instance, so I might not work on this for a while).
- Comments for more languages built-in.
- Improve the shell utility so it doesn't have to open vim, it just calls the python functions.
- (crazy idea) Have something that recognizes what variables you are dealing with, tries to guess which ones to use in the dumped code, then does a search and replace. This could be so you can just rapid fire dump code without thinking much. It wouldn't be a negative, as you likely have to replace some variables manually anyway. The initial implementation could do simple things, such as seeing if you are inside a loop, then taking the looped over variable, and maybe replacing the most common variable in the pasted text with your looped one... But again, this is a crazy idea.

## Other

This is the custom search engine that GSO uses: https://cse.google.com/cse/publicurl?cx=003962226882031433174:qk7rs-ca-bi

Currently, it searches the stackoverflow, superuser, tex, and unix forums.

SE: "NExeVkJzlom8ZUagXLcHQA(("

GOOGLE: "AIzaSyAk7sxnY_yHAP2OIdSOrgf9JysO8E_xJRo"
