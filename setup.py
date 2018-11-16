import os, sys
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Build.Dependencies import create_extension_list
version = '1.1.1'
README = os.path.join(os.path.dirname(__file__), 'README.md')
long_description = open(README).read() + '\n'

if sys.platform.startswith('linux'):
    source_files = ["thingking/pagefault.pyx"]
    extensions = [Extension("thingking.pagefault", source_files)]
    modules = cythonize(extensions)
else:
    modules = []

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
      packages=["thingking"],
      install_requires=["requests", "numpy"],
      ext_modules = cythonize(modules),
)
