#!/usr/bin/evn python
"""Installation script for GooglingStackOverflow python API
"""

from distutils.core import setup

setup(name='GooglingStackOverflow',
      version='0.0',
      description='Scrape stack overflow for answers',
      author='MilesCranmer',
      author_email='miles.cranmer@gmail.com',
      url='github.com/MilesCranmer/GooglingStackOverflow.vim',
      packages=['gso'],
      package_dir={'gso':'gso'})
