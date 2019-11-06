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

def run_tests(verbose=0,rtol=1.0000000000000001e-005,atol=1e-008,leg=False):
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
        leg : boolean
            Controls whether legacy functions should be tested.
    """
    from . import test
    testnum,testfail = test.distance(verbose)
    t = test.stats(verbose)
    testnum += t[0]
    testfail += t[1]
    t = test.hierarch(verbose)
    testnum += t[0]
    testfail += t[1]
    t = test.partition(verbose)
    testnum += t[0]
    testfail += t[1]
    if leg:
        t = test.legacy(verbose)
        testnum += t[0]
        testfail += t[1]
    print('Testing complete')
    print(('%i tests performed with %i failing' % (testnum,testfail)))
    print("Cluster package version %s" % (__version__))
    return
