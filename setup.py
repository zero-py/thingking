import os
from setuptools import setup, find_packages
version = '1.0.1'
README = os.path.join(os.path.dirname(__file__), 'README.md')
long_description = open(README).read() + 'nn'
setup(name='thingking',
      version=version,
      description=("A memory map for the World Wide Web"),
      long_description=long_description,
      classifiers=[
          "Programming Language :: Python",
          ("Topic :: Software Development :: Libraries :: Python Modules"),
      ],
      keywords='data',
      author='Matthew Turk <matthewturk@gmail.com>, Samuel Skillman <samskillman@gmail.com>, Michael S. Warren <mswarren@gmail.com>',
      license='BSD',
      packages=find_packages(),
      install_requires=["requests", "numpy", "functools32"],
      )
