"""A package of clustering routines for use with numpy.

This is the package header that handles the importation of all package 
components.

This package is intended to be a completely BSD license compliant package of
clustering routines which duplicates and expands upon the functionality of
Pycluster.  In particular, functions are modified with an eye towards the
inclusion of fuzzy clustering, which Pycluster doesn't do.
"""

#######################
## Necessary imports ##
#######################

from .distances import distance
from . import stats
from . import partition
from . import hierarch
from .hierarch import plot
from .version import __version__

######################
## Optional imports ##
######################
#Uncomment the following import statements to access certian functions directly
#without going through their disambiguation function.

#import distances  ## Distance functions disambiguated by the dist flag

######################
## Module Functions ##
######################

def run_tests(verbose=0,rtol=1.0000000000000001e-005,atol=1e-008,image_hash_size=8,image_hash_diff=5,force=False):
    """Tests to see if cluster is working properly.
    
    Parameters:
        verbose : int
            Controls amount of output to screen:
                0 : Only final results are printed to screen.
                1 : Tests which fail print a message to the screen.
                2 : All tests report on pass/fail status to screen.
        rtol : float
            The allowable relative error between calculated values and known
            results.
        atol : float
            The allowable absolute error in levs between calculated values and 
            known results.  If (rtol*known)+atol < abs(known-calc) then test
            passes.
        image_hash_size : int
            The size of the hash used to compare images (roughly the level of
            detail considered).
        image_hash_diff : int
            The amount of difference allowed between image hashes before the
            test image is considered to fail the test.
        force : Boolean
            Whether or not to keep testing when a test raises an exception.
    """
    from . import test
    import numpy
    test_distance = numpy.array(test.distance(verbose,rtol,atol,force))
    test_stats = numpy.array(test.stats(verbose,rtol,atol,force))
    test_hierarch = numpy.array(test.hierarch(verbose,rtol,atol,force))
    test_images = numpy.array(test.images(verbose,image_hash_size,image_hash_diff,force))
    test_partition = numpy.array(test.partition(verbose,rtol,atol,force))
    test_results = test_distance + test_stats + test_hierarch + test_images + test_partition
    print('Testing complete')
    print('%3i tests performed\n%3i exceptions were raised\n%3i exact tests failed\n%3i inexact tests were outside tolerance\n%3i image tests showed significant differences' % tuple(test_results))
    print("Cluster package version %s" % (__version__))
    return
