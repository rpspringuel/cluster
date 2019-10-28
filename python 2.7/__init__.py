"""A package of clustering routines for use with numpy.

This is the package header that handles the importation of all package 
components.

This package is intended to be a completely BSD license compliant package of
clustering routines which duplicates and expands upon the functionality of
Pycluster.  In particular, functions are modified with an eye towards the
inclusion of fuzzy clustering, which Pycluster doesn't do.
"""

##########################
## Liscense Information ##
##########################

###############################################################################
#Copyright (c) 2007-2010, R. Padraic Springuel                                #
#All rights reserved.                                                         #
#                                                                             #
#Redistribution and use in source and binary forms, with or without           #
#modification, are permitted provided that the following conditions are met:  #
#                                                                             #
#    * Redistributions of source code must retain the above copyright notice, #
#      this list of conditions and the following disclaimer.                  #
#    * Redistributions in binary form must reproduce the above copyright      #
#      notice, this list of conditions and the following disclaimer in the    #
#      documentation and/or other materials provided with the distribution.   #
#    * Neither the name of the University of Maine nor the names of its       #
#      contributors may be used to endorse or promote products derived from   #
#      this software without specific prior written permission.               #
#                                                                             #
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"  #
#AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE    #
#IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE   #
#ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE     #
#LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR          #
#CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF         #
#SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS     #
#INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN      #
#CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)      #
#ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE   #
#POSSIBILITY OF SUCH DAMAGE.                                                  #
###############################################################################

#######################
## Necessary imports ##
#######################

from distances import distance,distancesversion
import stats
import partition
import hierarch
import hierarch.plot

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
    import test
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
    print 'Testing complete'
    print '%i tests performed with %i failing' % (testnum,testfail)
    test.testversion()
    return

def clusterversion():
    print 'cluster/__init__.py'
    print 'Created 14 November, 2007'
    print 'by R. Padraic Springuel'
    print 'Version %s modified %s' % (clusterversionnum,clustermodified)
    print 'Most recent modification by %s' % clustermodifier
    print ''
    distancesversion()
    print ''
    stats.statsversion()
    print ''
    partition.partitionversion()
    print ''
    hierarch.hierarchcersion()
    return
