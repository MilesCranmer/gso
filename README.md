# GSO : Googling Stack Overflow

Much of the time you spend coding is Googling things, and dumping
other's code into your editor. Wouldn't it be great if you could have
that process integrated into your environment? Or even done
automatically for you?

This is the goal of GSO.

[![Screencast](http://i.imgur.com/pbqMMjh.gif)](https://asciinema.org/a/123242)
(click to view the asciinema screencast)

## Installation

Install python dependencies:

```` 
pip install google-api-python-client Cython py-stackexchange lxml
````

Get API keys for [Google Custom Search](https://developers.google.com/custom-search/json-api/v1/overview)
(scroll to API key), and [Stack Apps](https://stackapps.com/apps/oauth/register). Put these into
environment variables `GOOGLE_KEY` and
`SE_KEY`, respectively.

(Vundle) Add this repo to your vimrc file:

````
Plugin 'MilesCranmer/GooglingStackOverflow.vim'
````

Then, just `:PluginInstall` in vim.

Usage
-----

Inside vim, run:

````
:GSO Do a bubble sort in python
````

And watch the code get dumped below your cursor.

Docker
------

To pull and run (with your Google and Stack apps API keys):

```` 
docker run -it -e GOOGLE_KEY=$GOOGLE_KEY -e SE_KEY=$SE_KEY mcranmer/gso
````

Then, inside vim:

```` 
:GSO Do a bubble sort in python
````

And it will dump the first answer to below your cursor.

## Similar Projects

-   StackAnswers.vim - <https://github.com/james9909/stackanswers.vim>
    -   Almost exactly what I want, but it doesn't paste answers
        automatically, and I can't seem to get it working on Mac.

## Original Devpost project at MHacks 6 (Sept, 2015)** [link](http://devpost.com/software/stack-of-py)

(Didn't win anything, though!)
