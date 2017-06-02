GSO : Googling Stack Overflow
=============================

This app used to exist as a working plugin for sublime text.
That code exists on the `/sublime-text` branch. The library which
was used for googling things was deprecated, and I switched
to using vim. Therefore I am rewriting this as a vim plugin to use
a different plugin.

*This plugin is not currently working\*, but when it does, it will be*
**awesome**. I plan to use it quite frequently, so that should
force me to maintain it and make it better.
Help is very welcome.

\* Actually, it started working in the most basic use! It might
even be useful.

Usage
-----

I haven't set this up to work with Vundle or any other managers yet.
I would recommend you use my docker container to try this out, then
once things are formatted, you can actually install it.

**You need the Google custom search API key**

*You can optionally also get a Stack Exchange key, or else be limited to 300 queries per day* (which seems fine for trying this out)

To pull:

.. code::

    docker pull mcranmer/gso

To run (with your google and optionally stack exchange keys):

.. code::

    docker run -it -e GOOGLE_KEY=$GOOGLE_KEY -e SE_KEY=$SE_KEY mcranmer/gso

Then, inside vim:

.. code::
    
    :source plugin/gso.vim
    :call GSO("Do a bubble sort in python")

And it will dump it at the bottom of the file.

Description
-----------

Much of the time you spend coding is Googling things,
and dumping other's code into your editor.
Wouldn't it be great if you could have that process
integrated into your environment? Or even done automatically for you?

This is the goal of GSO.

Original Devpost project at MHacks 6 (Sept, 2015) [link_]
---------------------------------------------------------

.. _link: http://devpost.com/software/stack-of-py

(Didn't win anything, though!)

Similar Projects
----------------

- StackAnswers.vim - https://github.com/james9909/stackanswers.vim

  - Almost exactly what I want, but it doesn't paste answers automatically,
    and I can't seem to get it working on Mac.
