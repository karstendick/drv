#!/usr/bin/env python

from setuptools import setup

setup(name='drv',
      version='0.0.1',
      description='Library for working with discrete random variables',
      author='Joshua Karstendick',
      url='http://karstendick.com',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['drv'],
      install_requires=[
          'nose'
      ],
      entry_points='''
          [console_scripts]
          drv=drv:main
      ''',
      packages=['drv'],
)
