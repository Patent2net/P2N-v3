import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

requires = [
    'pyparsing==2.1.10',
    'python-epo-ops-client==2.3.1',
    'dogpile.cache==0.6.4',
    'requests==2.13.0',
    'networkx==1.11',
    'pydot==1.2.3',
    'pygraphviz==1.3.1',
    'beautifulsoup4==4.5.3',
    'numpy==1.12.0',
    'matplotlib==2.0.0',
    'python-louvain==0.5',
    'jinja2==2.10',
    'lxml==3.8.0',
    'docopt==0.6.2',
    'jsonpointer==1.12',
    'attrs==17.3.0',
    'Pillow==5.0.0',
    'where==1.0.2',
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
