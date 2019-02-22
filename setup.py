import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

requires = [
    'pyparsing',
    'python-epo-ops-client',
    'dogpile.cache',
    'requests',
    'networkx',
    'pydot',
    'pygraphviz',
    'beautifulsoup4',
    'numpy',
    'matplotlib',
    'python-louvain',
    'jinja2',
    'lxml',
    'docopt',
    'jsonpointer',
    'attrs',
    'Pillow',
    'where',
    'docopt',
    'numpy'
]

test_requires = [
]

setup(name='patent2net',
  version='3.0.0-dev6',
  description='Patent2Net is a testbed for working on patent information processing and statistical analysis for education and science.',
  long_description=README,
  license="CeCILL-2.1",
  classifiers=[
    "Development Status :: 4 - Beta",
    "Environment :: Web Environment",
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "Intended Audience :: End Users/Desktop",
    "Intended Audience :: Information Technology",
    "Intended Audience :: Legal Industry",
    "Intended Audience :: Manufacturing",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)",
    "Natural Language :: English",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX :: Linux",
    "Environment :: Console",
    "Environment :: MacOS X",
    "Environment :: Web Environment",
    "Environment :: Win32 (MS Windows)",
    "Programming Language :: JavaScript",
    "Programming Language :: Python",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Scientific/Engineering",
  ],
  author='The Patent2Net Developers',
  url='https://github.com/Patent2net/P2N',
  keywords='patent information research '
           'patent patents patent-search patent-data information information-retrieval intellectual-property '
           'research researcher researchers research-data research-tool research-and-development '
           'epo-ops open-data opendata '
  ,
  packages=find_packages(),
  include_package_data=True,
  package_data={
  },
  zip_safe=False,
  install_requires=requires,
  tests_require=test_requires,
  extras_require={
      'test': test_requires,
  },

  entry_points={
    'console_scripts': [
      'p2n = p2n.command:run',
    ],

  },

)
