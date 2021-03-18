# cluster
A python package of algorithms for cluster analysis.

This package is intended to be a completely BSD license compliant package of
clustering routines which duplicates and expands upon the functionality of
[Pycluster](http://bonsai.hgc.jp/~mdehoon/software/cluster/software.htm).  In 
particular, functions are modified with an eye towards the
inclusion of fuzzy clustering, which Pycluster doesn't do.

## Compatibility

This package is compatible with the Python 3.x series.

The most recent version which is compatible with Python 2.7 is available on the 
python27 branch.  As Python 2.7 support will ceased with Python 2.7's end of 
life (January 1, 2020), this version is unsupported.

## Dependencies

This package uses the `warnings` and `types` libraries which should have come 
with your standard Python installation.

This package depends on [Numpy](http://numpy.scipy.org/), [Scipy](
http://www.scipy.org/scipylib/index.html), and [Matplotlib](
http://matplotlib.org/) for many of its underlying calculation routines.  All 
three can be [obtained here](http://www.scipy.org/install.html).

The test suite (which is not yet complete) also depends on 
`pickle`(3.x), `sys`, and `os`, all of which should have come 
with your standard installation of Python.

## Installation

To install simply copy the files into a folder named `cluster` in your 
`site-pacakges` folder for Python.  If you wish to keep this folder in sync 
with your clone of the repository and are using a Unix based system (e.g. Mac 
OSX or Linux), you can create a symlink in `site-packages` which points to 
it.  Just be sure that the folder (or symlink to the folder) in 
`site-pacakges` is named `cluster`.

## Testing

There are two ways of testing the behavior of this package to make sure it
is working on your system:

  1) Run `test/__init__.py` (check to make sure it is executable and that you 
  have python3 somewhere on your PATH).  
  
     To control the verbosity of the output, use the `-v` or `--verbose` flags.  
     Available levels are:
  
      0) Only final results are printed to screen. (default)
      1) Tests which fail print a message to the screen.
      2) All tests report on pass/fail status to screen
    
     When a test raises an exception, it will halt the execution of the tests 
     unless the `-f` or `--force` option is given.

  2) In the Python interpreter, run the following commands:
     ```
     import cluster
     cluster.run_tests()
     ```

     Verbosity of the output can be controled by setting the `verbose` argument 
     to one of the values given above.
     
     To keep testing after a test raises an exception, set the `force` argument 
     to True.

