# cluster
A python package of algorithms for cluster analysis.

This package is intended to be a completely BSD license compliant package of
clustering routines which duplicates and expands upon the functionality of
[Pycluster](http://bonsai.hgc.jp/~mdehoon/software/cluster/software.htm).  In 
particular, functions are modified with an eye towards the
inclusion of fuzzy clustering, which Pycluster doesn't do.

## Compatibility

This package is compatible with both the Python 2.7 and 3.7 series.  Python 
2.7 support will cease with Python 2.7's end of life (January 1, 2020).  The 
Python 3.7 version should be compatible with other versions of Python 3.x, 
but this has not been tested.

## Dependencies

This package uses the `warnings` and `types` libraries which should have come 
with your standard Python installation.

This package depends on [Numpy](http://numpy.scipy.org/), [Scipy](
http://www.scipy.org/scipylib/index.html), and [Matplotlib](
http://matplotlib.org/) for many of its underlying calculation routines.  All 
three can be [obtained here](http://www.scipy.org/install.html).

The test suite (which is not yet complete) also depends on 
`cPickle`(2.7)/`pickle`(3.x), `sys`, and `os`, all of which should have come 
with your standard installation of Python.

## Installation

To install simply copy the files in `python 2.7` or `python 3.7` (as 
appropriate for your version) into a folder named `cluster` in your 
`site-pacakges` folder for Python.  If you wish to keep this folder in sync 
with your clone of the repository and are using a Unix based system (e.g. Mac 
OSX or Linux), you can create a symlink in `site-packages` which points to 
it.  Just be sure that the folder (or symlink to the folder) in 
`site-pacakges` is named `cluster`.
