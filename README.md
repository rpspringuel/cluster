# cluster
A python package of algorithms for cluster analysis.

This package is intended to be a completely BSD license compliant package of
clustering routines which duplicates and expands upon the functionality of
[Pycluster](http://bonsai.hgc.jp/~mdehoon/software/cluster/software.htm).  In particular, functions are modified with an eye towards the
inclusion of fuzzy clustering, which Pycluster doesn't do.

## Compatibility

This package is compatible with the Python 2.7 series.  While there are plans to make a version which is compatible with the 3.x series, this has not yet been implemented.

## Dependencies

This package uses the `warnings` and `types` libraries which should have come with your standard Python installation.

This package depends on [Numpy](http://numpy.scipy.org/), [Scipy](http://www.scipy.org/scipylib/index.html), and [Matplotlib](http://matplotlib.org/) for many of its underlying calculation routines.  All three can be [obtained here](http://www.scipy.org/install.html).

The test suite (which is not yet complete) also depends on `cPickle`, `sys`, and `os`, all of which should have come with your standard installation of Python.

## Installation

To install simply copy the files in `python 2.7` into a folder named `cluster` in your `site-pacakges` folder for Python 2.7.  If you wish to keep this folder in sync with your clone of the repository and are using a Unix based system (e.g. Mac OSX or Linux), you can create a symlink in `site-packages` which points to it.  Just be sure that the folder (or symlink to the folder) in `site-pacakges` is named `cluster`.
