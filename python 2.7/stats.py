"""Cluster _support which are method independant.

Routines which calculate _support for data and clustering results.
_support in this package do not care what the particluar clustering
methodology is.

A complete version history and licence and copyright information are located
in the source code.
"""

#####################
## Version History ##
#####################

statsversionnum = '0.0'
statsmodified = '14 November, 2007'
statsmodifier = 'R. Padraic Springuel'
#Initial creation date.
#Started work on distancematrix.

statsversionnum = '1.0'
statsmodified = '15 November, 2007'
statsmodifier = 'R. Padraic Springuel'
#Finished distancematrix.
#Wrote full distancematrix.
#Ported silhouette, members from ClusterStats.

statsversionnum = '1.1'
statsmodified = '16 November, 2007'
statsmodifier = 'R. Padraic Springuel'
#Started singleclustercentroid.  Still need to figure out how to find medians.

statsversionnum = '1.1.1'
statsmodified = '26 Novemeber, 2007'
statsmodifier = 'R. Padraic Springuel'
#Worked out how to find medians.

statsversionnum = '1.1.2'
statsmodified = '28 Novemeber, 2007'
statsmodifier = 'R. Padraic Springuel'
#Debugging singleclustercentroid.

statsversionnum = '1.2'
statsmodified = '29 November, 2007'
statsmodifier = 'R. Padraic Springuel'
#Wrote clustercentroids.
#Ported SSE from ClusterStats.

statsversionnum = '1.3'
statsmodified = '3 December, 2007'
statsmodifier = 'R. Padraic Springuel'
#Wrote weightedmedian.

statsversionnum = '1.4'
statsmodified = '4 December, 2007'
statsmodifier = 'R. Padraic Springuel'
#Wrote fuzzy_singleclustercentroid.

statsversionnum = '1.5'
statsmodified = '5 Decemver, 2007'
statsmodifier = 'R. Padraic Springuel'
#Debugging weightedmedian and fuzzy_singleclustercentroid.
#Wrote levels, fuzzy_clustercentroids, levscheck.

statsversionnum = '1.5.1'
statsmodified = '6 December, 2007'
statsmodifier = 'R. Padraic Springuel'
#Debugging weightedmedian, levels, fuzzy_clustercentroids, & levscheck.
#Renamed singleclustercentroid to old_singleculstercentroid.
#Renamed clustercentroids to old_clutercentroids.
#Renamed fuzzy_singleclustercentroid to singleclustercentroid.
#Renamed fuzzy_culstercentroids to clutercentroids.

statsversionnum = '1.5.2'
statsmodified = '11 December, 2007'
statsmodifier = 'R. Padraic Springuel'
#Cleanup of old_singleclustercentroid to use scipy.stats.stats.nanmedian and scipy.stats.stats.nanmean

statsversionnum = '1.6'
statsmodified = '30 December, 2007'
statsmodifier = 'R. Padraic Springuel'
#Documentation update and reformat to docstring standards.
#Removed weightedmedian definition in favor of using _support.median.
#Renamed SSE to old_SSE.
#Wrote SSE that employs the levs array.

statsversionnum = '1.7'
statsmodified = '16 January, 2008'
statsmodifier = 'R. Padraic Springuel'
#Edited singleclustercentroid, clustercentroids, & SSE to contain an exponent which determines the influence of the weights in levs.  This brings those functions into line with formulas 9.1 & 9.2 in Tan, Steinbach, & Kumar (2006), Data Mining, Pearson Education Inc., Boston.
#Updated silhouette's documentation to explain why it uses clusterid instead of levs.

statsversionnum = '1.7.1'
statsmodified = '23 January, 2008'
statsmodifier = 'R. Padraic Springuel'
#Revised calls of _support.median to take advantage of new axis control.

statsversionnum = '1.8'
statsmodified = '24 January, 2008'
statsmodifier = 'R. Padraic Springuel'
#Added full range of averaging type functions from _support for finding the cluster centroid in singleclustercentroid.

statsversionnum = '1.9'
statsmodified = '28 January, 2008'
statsmodifier = 'R. Padraic Springuel'
#Added point_SSE and debugged SSE.

statsversionnum = '1.10'
statsmodified = '31 January, 2008'
statsmodifier = 'R. Padraic Springuel'
#Wrote levscompare.

statsversionnum = '1.10.1'
statsmodified = '6 February, 2008'
statsmodifier = 'R. Padraic Springuel'
#Documentation revisions.

statsversionnum = '1.11'
statsmodified = '20 February, 2009'
statsmodifier = 'R. Padraic Springuel'
#Changed singleclustercentroid and clustercentroids to allow for the passing of the distance matrix to them when using medoid methods rather than forcing a recalculation of it.

statsversionnum = '1.12'
statsmodified = '25 February, 2009'
statsmodifier = 'R. Padraic Springuel'
#Wrote SEmatrix.

statsversionnum = '1.13'
statsmodified = '27 February, 2009'
statsmodifier = 'R. Padraic Springuel'
#Added mode to the list of available measures of central tendancy for singleclustercentroid.  This required some rewrite of clustercentroids and still requires some reworking of SEmatrix.

statsversionnum = '1.13.1'
statsmodified = '4 March, 2009'
statsmodifier = 'R. Padraic Springuel'
#Modified SEmatirx to handle multi-modal centroids.

statsversionnum = '1.14'
statsmodified = '6 March, 2009'
statsmodifier = 'R. Padraic Springuel'
#Updated to handle the new axis functioning of _support.mode.

statsversionnum = '1.15'
statsmodified = '28 March, 2009'
statsmodifier = 'R. Padraic Springuel'
#Added verbose option to distancematrix and fulldistancematrix.

statsversionnum = '2'
statsmodified = '2 June, 2009'
statsmodifier = 'R. Padraic Springuel'
#Eliminated transpose argument from functions.  This behavior can be duplicated by use of numpy's transpose function on arguments and the results.  The follwoing functions were not updated because they are considered legacy: old_singleclustercentroid, old_clustercentroids, old_SSE, SSE, point_SSE

statsversionnum = '2.1'
statsmodified = '23 May, 2010'
statsmodifier = 'R. Padraic Springuel'
#Modified levscheck to include a test for values greater than 1 or less than 0 and made the rounding percision a user accessible variable.
#Renamed levels to clusterid_to_levs and created levs_to_clusterid.
#First pass at writing fuzzy_silhouette.
#Modified silhouette to make its inputs conform to the preference for levs over clusterid and to fix inappropirate use of weight.

statsversionnum = '2.1.1'
statsmodified = '25 May, 2010'
statsmodifier = 'R. Padraic Springuel'
#Rewriting fuzzy_silhouette based on some precieved problems in the original ideas.  Came up with a better idea for calculating a, but still need to come up with an equivalent idea for calculating b.

statsversionnum = '2.1.2'
statsmodified = '26 May, 2010'
statsmodifier = 'R. Padraic Springuel'
#More rewriting of fuzzy_silhouette.  Preliminary tests show silhouette and fuzzy_silhouette disagreeing.  Need to figure out why.

statsversionnum = '2.2'
statsmodified = '27 May, 2010'
statsmodifier = 'R. Padraic Springuel'
#Finished rewriting and testing fuzzy_silhouette.  Renamed silhouette to old_silhouette, restored its use of clusterid, and labeled it a legacy function.  Renamed fuzzy_silhouette to silhouette.

statsversionnum = '2.3'
statsmodified = '28 May, 2010'
statsmodifier = 'R. Padraic Springuel'
#Added deprecation warnings.

statsversionnum = '2.3.1'
statsmodified = '21 June, 2010'
statsmodifier = 'R. Padraic Springuel'
#Updated error statements.

statsversionnum = '2.3.2'
statsmodified = '25 June, 2010'
statsmodifier = 'R. Padraic Springuel'
#Removed Statisitcs dependencies.

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

import numpy
import distances
import scipy
import _support
import warnings

def distancematrix(data,weights=None,dist='e',verbose=False):
    """Computes the distance matrix for a given data set.
    
    The distance matrix indicates the distance between each data point in the
    data set.  Each entry is a distance, with it's indicies indicating which
    data points are seperated by that distance, much like the distance chart
    you might find on a map that lists the distance between cities. Thus the
    matrix is symetric and all diaganol elements are 0.  This function reduces
    needed memory by only storing the lower half matrix, excluding the main
    diaganol.
    
    While the transpose parameter has been removed, the behavior formerly
    obtained by setting transpose to True can be duplicated by the command
    distancematrix(numpy.transpose(data),...).
    
    Parameters:
        data : ndarray
            Rank 2 array. Each row is assumed to represent a single data point.
        weights : ndarray
            Optional.  If given, a rank 1 array with length equal to the number
            of columns in data.  Entries specify the weight for each dimension
            in the distance function.
        dist : string
            Specifies the desired distance function by it's alias.
        verbose : boolean
            If true periodic updates on progress will be printed to the screen.
    Returns:
        dm : list of ndarray
            Returns only the lower left half of the matrix, not including the 
            main diaganol.  Upper right half elements are a mirror of the lower
            left half and main diaganol elements are all zero.  Thus, each row
            has one more element than the one above, and the first row has no
            elements.
    See Also:
        distances.distance
    """
    dm = []
    if verbose:
        N = len(data)*(len(data)-1)/2
        current = 0
        n = 0
    for i in range(len(data)):
        row = []
        for j in range(i):
            row.append(distances.distance(data[i],data[j],weights,dist))
            if verbose:
                n += 1
                if n*100/N > current:
                    current = n*100/N
                    print '%i%% complete' % current
        dm.append(numpy.array(row))
    return dm

def fulldistancematrix(data,weights=None,dist='e',verbose=False):
    """Computes the distance matrix for a given data set.
    
    Same as distancematrix but retruns the full distance matrix.  Requires more
    memory as a result, but can be easier to work with.
    
    While the transpose parameter has been removed, the behavior formerly
    obtained by setting transpose to True can be duplicated by the command
    fulldistancematrix(numpy.transpose(data),...).
    
    Parameters:
        data : ndarray
            Rank 2 array. Each row is assumed to represent a single data point.
        weights : ndarray
            Optional.  If given, a rank 1 array with length equal to the number
            of columns in data.  Entries specify the weight for each dimension
            in the distance function.
        dist : string
            Specifies the desired distance function by it's alias.
        verbose : boolean
            If true periodic updates on progress will be printed to the screen.
    Returns:
        dm : ndarray
            Returns the distance matrix for the data.  This matrix is symmetric
            and with all main diaganol elements equal to 0.
    See Also:
        distancematrix    
    """
    dm = numpy.zeros((len(data),len(data)))
    if verbose:
        N = len(data)*(len(data)-1)/2
        current = 0
        n = 0
    for i in range(len(data)):
        for j in range(i):
            dm[j][i] = dm[i][j] = distances.distance(data[i],data[j],weights,dist)
            if verbose:
                n += 1
                if n*100/N > current:
                    current = n*100/N
                    print '%i%% complete' % current
    return dm

def old_silhouette(point,clusterid,dm=None,data=None,weight=None,dist='e'):
    """Calculates the silhouette coefficient for a given data point.
    
    The silhouette coefficient is calculated by the following algorithm:
    1. For point, calculate its average distance to all other points in its
    cluster.  Call this value a.
    2. For point and any cluster not containing point, calculate point's
    average distance to all points in the given cluster.  Find the minimum such
    value with respect to all clusters; call this value b.
    3. For point, the silhouette coefficient is s = (b-a)/max(a,b).
    Because of this definition, the silhouette coefficeint cannot be applied to
    a fuzzy clustering solution.  Use of levs instead of clusterid is thus
    inappropriate.
    The normal range for the silhouette coefficient is -1 to 1 with higher 
    values indicating better clustering.  A nan result indicates two things: 
    (1) that the specified point is currently in a cluster consisting soley of 
    other identical points (if any) and (2) there is another cluster which also
    consists soley of points identical to the point in question.
    The function runs faster if it is given the distance matrix (called dm here
    to avoid confusion with the distancematrix function call).  This is 
    especially important when calculating the average silhouette coefficent for
    an entire data set.  The arguments data, mask, weight, and dist only come 
    into play when the distance matrix is not given.

    While the transpose parameter has been removed, the behavior formerly
    obtained by setting transpose to True can be duplicated by the command
    silhouette(...,data=numpy.transpose(data),...).
    
    The silhouette coefficient was originally defined in P. J. Rousseeuw,
    Silhouettes: a graphical aid to the interpretation and validation of cluster
    analysis, Journal of Computatonal and Applied Mathematics 20, 53 (1987), URL
    http://dx.doi.org/10.1016/0377-0427(87)90125-7.
    
    This is a legacy function and is kept primarily to aid in conversions to
    and from PyCluster.
    
    Parameters:
        point : integer
            Indicates the row index within data for the point the 
            silhouette coefficent is being calculated for.
        clusterid : ndarray
            Rank 1 array listing the cluster each data point belongs to.
        dm : list of ndarray or ndarray
            Optional.  The distance matrix for the data (i.e. the results of a 
            distancematrix or fulldistancematrix call).  If not provided data is
            required.
        data : ndarray
            Optional.  The data set.  Not required if dm is provided.
        weight : ndarray
            Optional.  If given, a rank 1 array with length equal to the number
            of columns in data.  Entries specify the weight for each dimension
            in the distance function.  Not required if dm is provided.
        dist : string
            Optional.  Specifies the distance function to use.  Not required if
            dm is provided.
    Returns:
        sil : float
            The silhouette coefficient for the given point in the data set.
    """
    warnings.warn('old_silhouette is a legacy fucntion and is kept primarily to aid in conversions to and from PyCluster.  If you are not using PyCluster it is recommended that you modify your program to use silhouette instead.',DeprecationWarning,stacklevel=2)
    if dm is None:
        d = []
        for i in range(len(data)):
            d.append(distances.distance(data[point],data[i],weight,dist))
        d = numpy.array(d)
    elif type(dm) is list:
        d = []
        for i in range(len(dm)):
            if i == point:
                d.append(0)
            else:
                d.append(dm[max([i,point])][min([i,point])])
        d = numpy.array(d)
    else:
        d = dm[point]
    t = list(numpy.zeros(max(clusterid)+1))
    length = list(numpy.zeros(max(clusterid)+1))
    for i in range(len(clusterid)):
        if point != i:
            t[clusterid[i]] += d[i]
            length[clusterid[i]] += 1
    for i in range(len(t)):
        if length[i] == 0:
            t[i] = 0
        else:
            t[i] = t[i]/length[i]
    a = t[clusterid[point]]
    t.remove(t[clusterid[point]])
    b = min(t)
    try:
        sil = (b-a)/max([a,b])
    except ZeroDivisionError:
        sil = numpy.nan
    return sil

def silhouette(point,levs,dm=None,data=None,weight=None,dist='e'):
    """Variation on the silhouette coefficient that works for fuzzy clustering.
    
    The fuzzy silhouette coefficient is calculated by the following algorithm:
    1. Convert the distances from the point to similarities.
    2. Calculate the average similarity between the point and each cluster,
    weighting by the probability of each point being in that cluster.  Call the
    set of these values s.
    3. Multiply the values in s by the probability that the point is in that
    cluster.  Call these values a.
    4. Multiply the values in s by the probability that the point is in each
    cluster.  For each cluster choose the maximum such value that cooresponds to
    a different cluster.  Call these values b.
    5. The silhouette coefficients for each cluster is defined as
    (a-b)/(1-min(a,b)) for the a and b value which corresponds to that cluster.
    
    Note that in cases where the levs array represents an exclusive clustering
    (i.e. each row has only one non-zero entry and that entry is 1) the
    silhouette coefficients for clusters which the point is not a member of
    should be 0 while for the cluster which the point is a member of should be
    the normal silhouette coefficient. As a result, for exclusive clustering
    solutions: sum(silhouette(...)) = old_silhouette(...).
    
    Since the probability of two points is being in the same cluster is high
    when the product of the appropriates levs entries is high, but when the
    distance between those two points is low, we have to convert distances to
    similarities to avoid messing up the max function built-in to the
    definition of the silhouette coefficient.  We do this by assuming that 
    s = 1 - d.  However, we are still computing the distance version of the
    silhouette coefficient.  As a result, it is essential that normalized
    distances be used.
    
    The silhouette coefficient was originally defined in P. J. Rousseeuw,
    Silhouettes: a graphical aid to the interpretation and validation of cluster
    analysis, Journal of Computatonal and Applied Mathematics 20, 53 (1987), 
    URL http://dx.doi.org/10.1016/0377-0427(87)90125-7.  The generalization here
    to fuzzy clustering was made by R. P. Springuel and is unpublished.
    
    Parameters:
        point : integer
            Indicates the row index within data for the point the 
            silhouette coefficent is being calculated for.
        levs : ndarray
            Rank 2 array contianing entries indicating the membership level of
            each point in each cluster. levs[i][j] is the level to which the 
            ith data point belongs to the jth cluster.
        dm : list of ndarrays or ndarray
            Optional.  The distance matrix for the data (i.e. the results of a 
            distancematrix or fulldistancematrix call).  If not provided data is
            required.
        data : ndarray
            Optional.  The data set.  Not required if dm is provided.
        weight : ndarray
            Optional.  If given, a rank 1 array with length equal to the number
            of columns in data.  Entries specify the weight for each dimension
            in the distance function.  Not required if dm is provided.
        dist : string
            Optional.  Specifies the distance function to use.  Not required if
            dm is provided.
    Returns:
        sil : float
            The silhouette coefficient for the given point in the data set.
    """
    if dm is None:
        d = []
        for i in range(len(data)):
            d.append(distances.distance(data[point],data[i],weight,dist))
        d = numpy.array(d)
    elif type(dm) is list:
        d = []
        for i in range(len(dm)):
            if i == point:
                d.append(0)
            else:
                d.append(dm[max([i,point])][min([i,point])])
        d = numpy.array(d)
    else:
        d = dm[point]
    s = 1 - d
    lev = levs[point].copy()
    levs[point] = 0
    s = numpy.sum(levs*s.reshape(len(s),1),axis=0)/numpy.sum(levs,axis=0)
    s = numpy.outer(lev,s)
    a = numpy.diagonal(s)
    s = s - numpy.identity(len(s)) * numpy.diagonal(s)
    b = s.max(axis=1)
    sil = (a-b)/numpy.array([a,b]).max(axis=0)
    sil = (a-b)/(1-numpy.array([a,b]).min(axis=0))
    levs[point] = lev
    return sil

def members(clusterid):
    """Convert a clusterid to a members list.
    
    Takes the clusterid list and converts it to a list of the members of each 
    cluster.  Members are specified by their index number in data.  mems[i][j] 
    is the jth member of the ith cluster.  Since there is no guaruntee that 
    each cluster has the same number of members the return is a list of lists 
    instead of an array.
    
    This is a legacy function and is kept primarily to aid in conversions to
    and from PyCluster.
    
    Parameters:
        clusterid : ndarray
            Rank 1 array listing the cluster each data point belongs to.
    Returns:
        mems : list of list
            List of members in each cluster.  Each row is for a different
            cluster with the entires on each row indicating the indecies of
            the data points in that cluster.
    """
    warnings.warn('members is a legacy fucntion and is kept primarily to aid in conversions to and from PyCluster.  If you are not using PyCluster it is recommended that you modify your program to use levs arrays.',DeprecationWarning,stacklevel=2)
    mems = []
    for i in range(max(clusterid)+1):
        c = list(clusterid)
        mems.append([])
        for j in range(c.count(i)):
            mems[i].append(c.index(i)+j)
            c.remove(i)
    return mems
    
def clusterid_to_levs(clusterid):
    """Takes the clusterid list and converts it to an array of levels.
    
    While the transpose parameter has been removed, the behavior formerly
    obtained by setting transpose to True can be duplicated by the command
    numpy.transpose(levels(...)).

    This is a legacy function and is kept primarily to aid in conversions to
    and from PyCluster.
    
    Parameters:
        clusterid : ndarray
            Rank 1 array listing the cluster each data point belongs to.
    Returns:
        levs : ndarray
            Rank 2 array containing 0s and 1s indicating the membership level
            of each data point in each cluster. levs[i][j] is the level to 
            which the ith data point belongs to the jth cluster.  Since 
            clusterid assumes each point belongs to only one cluster, each row
            should have only one non-zero entry which should be 1.
    """
    warnings.warn('clusterid_to_levs is a legacy fucntion and is kept primarily to aid in conversions to and from PyCluster.  If you are not using PyCluster it is recommended that you modify your program to use levs arrays instead of clusterid arrays.',DeprecationWarning,stacklevel=2)
    levs = numpy.zeros((len(clusterid),max(clusterid)+1),float)
    for i in range(len(clusterid)):
        levs[i][clusterid[i]] = 1.
    return levs

def levs_to_clusterid(levs):
    """Takes a levs array and converts it to a clusterid list.
    
    This is a legacy function and is kept primarily to aid in conversions to
    and from PyCluster.
    
    Parameters:
        levs : ndarray
            Rank 2 array contianing entries indicating the membership level of
            each point in each cluster. levs[i][j] is the level to which the 
            ith data point belongs to the jth cluster.  Since clusterid assumes
            each point belongs to only one cluster, each row should have only
            one non-zero entry which should be 1.
    Returns:
        clusterid : ndarray
            Rank 1 array listing the cluster each data point belongs to.
    """
    warnings.warn('levs_to_clusterid is a legacy fucntion and is kept primarily to aid in conversions to and from PyCluster.  If you are not using PyCluster it is recommended that you modify your program to use levs arrays instead of clusterid arrays.',DeprecationWarning,stacklevel=2)
    test1 = levs == 0
    test2 = levs == 1
    test = numpy.all(test1+test2)
    if not test:
       raise ValueError('levs array does not represent exclusive clustering.')
    clusterid = numpy.argmax(levs,axis=1)
    return clusterid
    
def levscheck(levs,percision=15):
    """Check to see if a levs array is legal.
    
    Checks to make sure that full list of weights for each data point in each
    cluster has no values greater than 1 or less than 0, is properly normalized,
    and that each cluster has at least one member but doesn't contain all data
    points with weight 1.
    
    While the transpose parameter has been removed, the behavior formerly
    obtained by setting transpose to True can be duplicated by the command
    levscheck(numpy.transpose(levs),...).

    Parameters:
        levs : ndarray
            Rank 2 array contianing entries indicating the membership level of
            each point in each cluster. levs[i][j] is the level to which the 
            ith data point belongs to the jth cluster.
        percision : integer
            Number of decimal digits for the normalization test.
            It was found during testing that excessive percision in levs could
            lead to a false normalization error.  I.e. even when the elements of
            levs were defined by d/numpy.sum(d) for a particular data point, 
            this function would say that that data point was not normalized 
            under some circumstances.  To alleviate this problem, a data point
            is considered normalized when the sum of its levs values round to 1
            at percision decimal places.
    Returns:
        result : boolean
            True if levs is legal, False if it isn't
        normal : list of integers
            List of data points identified by their index in levs which do not 
            have normalized weights.
        empty : list of integers
            List of clusters identified by their index in levs which do not
            have any members.
        full : list of integers
            List of clusters identified by their index in levs which contain
            all data points with weight 1.
    """
    test1 = numpy.round(numpy.sum(levs,axis=1),percision) == 1
    test2 = numpy.sum(levs,axis=0)
    test3 = numpy.all(0 <= levs) and numpy.all(levs <= 1)
    normal = []
    empty = []
    full = []
    if not all(test1):
        for i in range(len(test1)):
            if not test1[i]:
                normal.append(i)
    if not all(test2 > 0):
        for i in range(len(test2)):
            if test2[i] <= 0:
                empty.append(i)
    if not all(test2 < len(test1)):
        for i in range(len(test2)):
            if test2[i] >= len(test1):
                full.append(i)
    result = test3 and (len(normal) == 0) and (len(empty) == 0) and (len(full) == 0)
    return result,normal,empty,full

def old_singleclustercentroid(data,mem=None,method='a',transpose=False):
    """Calculates the centroid of a cluster.
    
    The old prefix is used because of the use of mem to specify which data
    points are in the cluster.  For exclusive clustering, mem works fine, but
    fuzzy clustering requires a levs array.  Since a levs array can also be
    used in exclusive clustering, it is more general and thus the prefered way
    of identifying cluster membership in this package.
    
    This is a legacy function and is kept primarily to aid in conversions to
    and from PyCluster.
    
    Parameters:
        data : ndarray
            Rank 2 array containing the data set.
        mem : list
            The list of cluster members. If mem is None (default) then all 
            member of data are assumed to be in the same cluster.  Entries
            refer to the indecies of the data points.
        method : string
            Method specifies whether the arithmetic mean (a, default) or the
            median (m) is to be used to find the centroid.
        transpose : boolean
            sets whether data points are columns (True) or rows (False, 
            default) of data.
    Returns:
        result : ndarray
            Rank 1 array containing the centroid.
    """
    warnings.warn('old_singleclustercentroid is a legacy fucntion and is kept primarily to aid in conversions to and from PyCluster.  If you are not using PyCluster it is recommended that you modify your program to use singleclustercentroid instead.',DeprecationWarning,stacklevel=2)
    if mem is None:
        if transpose:
            mem = range(len(data[0]))
        else:
            mem = range(len(data))
    d = []
    if transpose:
        for i in range(len(data[0])):
            if i in mem:
                d.append(list(data[:,i]))
    else:
        for i in range(len(data)):
            if i in mem:
                d.append(list(data[i]))
    d = numpy.array(d)
    if method == 'a':
        result = scipy.stats.stats.nanmean(d,axis=0)
    elif method == 'm':
        result = scipy.stats.stats.nanmedian(d,axis=0)
    else:
        raise ValueError('Method type unsupported.')
    return result

def singleclustercentroid(data,lev,p=1.,method='a',weights=None,distancematrix=None):
    """Calculates the centroid of a cluster.
    
    While the transpose parameter has been removed, the behavior formerly
    obtained by setting transpose to True can be duplicated by the command
    singleclustercentroid(numpy.transpose(data),...).

    Parameters:
        data : ndarray
            Rank 2 array containing the data set.
        lev : ndarray
            Rank 1 array that contains the list of weights that specify how 
            important a particular point is in determining the location of the
            centroid.  0 means that the data point should have no impact, while
            1 means that it should have maximal impact.
        p : float
            Determines the influence of the weights.  Should be between 1 and
            infinity.  Values closer to 1 yield more distinct centroids.
            Larger values lead to centroids which approach the global centroid.
            Should always be 1 for exclusive clustering.
        method : string
            Specifies the method to be used for amalgamating the various
            observations into a single value.  Supported methods are:
            a - arithmetic mean (default)
            m - median 
            s - absolute mean
            g - geometric mean
            h - harmonic mean
            q - quadratic mean
            d - mode (results may be multivalued along some dimensions)
            o* - medoid (point with smallest average distance to other points)
            When specifying a medoid method the wildcard (*) should be one of
            the available distance functions and weights should be given (if
            appropriate).  If distancematrix is given, then 'o' should be given
            by itself (the wildcard will be ignored).
        weights : ndarray
            Optional.  If given, a rank 1 array with length equal to the number
            of rows in data.  Entries specify the weight for each dimension in 
            the distance function.  Only needed if a medoid method is being 
            used and dimensions are not equally weighted.
        distancematrix : ndarray
            Optional.  Used to save time when calculating centroids using a
            medoid (o) method.  Passing distancematrix prevents this function
            from calculating it and thus this option is mostly useful when
            running several functions that require knowledge of the distance
            matrix and would otherwise have to calculate it themselves.
    Returns:
        centroid : ndarray
            Rank 1 array containing the centroid.  If method = 'd' then dtype 
            for this array is object.  Otherwise it is the same as dtype of 
            data or float, whichever is of higher order.
    Notes:
        Because this function only deals with one cluster (i.e. only one 
        row/column of the full levs matrix) it has no way of knowing if the 
        values in lev have been properly normalized (i.e. assigned so so that a
        particular data point has a total weight of 1 when summed over all 
        clusters.
    See Also:
        distances.distance
    """
    lev = lev[:,numpy.newaxis]
    if method == 'a':
        centroid = _support.mean(data,lev**p,axis=0,NN=False)
    elif method == 'm':
        centroid = _support.median(data,lev**p,axis=0,NN=False)
    elif method == 's':
       centroid = _support.absmean(data,lev**p,axis=0,NN=False)
    elif method == 'g':
       centroid = _support.geomean(data,lev**p,axis=0,NN=False)
    elif method == 'h':
       centroid = _support.harmean(data,lev**p,axis=0,NN=False)
    elif method == 'q':
       centroid = _support.quadmean(data,lev**p,axis=0,NN=False)
    elif method == 'd':
        centroid = _support.mode(data,lev**p,axis=0,NN=False)
    elif method[0] == 'o':
        if distancematrix is None:
            d = fulldistancematrix(data,weights,method[1:])
        else:
            d = distancematrix
        d = list(_support.mean(d,lev**p,axis=0,NN=False))
        i = d.index(min(d))
        centroid = data[i]
    else:
        raise ValueError('Method type unsupported.')
    return centroid

def old_clustercentroids(data,mems=None,clusterid=None,method='a',transpose=False):
    """Calculates the centroid of all clusters.  
    
    The old prefix is used because of the use of mems/clusterid to specify 
    which data points are in the cluster.  For exclusive clustering, 
    mems/clusterid work fine, but fuzzy clustering requires a levs array.  
    Since a levs array can also be used in exclusive clustering, it is more 
    general and thus the prefered way of identifying cluster membership in this
    package.
    
    This is a legacy function and is kept primarily to aid in conversions to
    and from PyCluster.
    
    Parameters:
        data : ndarray
            Rank 2 array containing the data set.
        mems : list of lists
            Each list centains the indecies of the data points in that cluster.
            Either mems or clusterid must be provided. mems will override
            clusterid if both are provided.
        clusterid : ndarray
            Rank 1 array with length equal to the number of data points.  
            Elements of clusterid should be integers identifying the cluster to
            which each data point belongs. Either clusterid or mems must be
            provided.  If both are provided, mems is used and clusterid is 
            ignored.
        method : character
            Specifies whether the arithmetic mean (a, defualt) of the median 
            (m) is to be used to find the centroid.
        transpose : boolean
            Sets whether data points are columns (True) or rows (False, 
            default) of data and how the output is arranged (same conditions).
    Returns:
        cdata : ndarray
            Rank 2 array containing the centroids.  If transpose is True, then
            each column corresponds to a centroid.  If False, then each row is
            a centroid.
    """
    warnings.warn('old_clustercentroids is a legacy fucntion and is kept primarily to aid in conversions to and from PyCluster.  If you are not using PyCluster it is recommended that you modify your program to use clustercentroids instead.',DeprecationWarning,stacklevel=2)
    if mems is None:
        mems = members(clusterid)
    cdata = []
    for mem in mems:
        cdata.append(list(old_singleclustercentroid(data,mem,method,transpose)))
    if transpose:
        cdata = numpy.array(numpy.transpose(cdata))
    else:
        cdata = numpy.array(cdata)
    return cdata

def clustercentroids(data,levs,p=1.,method='a',weights=None,distancematrix=None):
    """Calculates the centroid of all clusters.
    
    While the transpose parameter has been removed, the behavior formerly
    obtained by setting transpose to True can be duplicated by the command
    numpy.transpose(clustercentroids(numpy.transpose(data),...).

    Parameters:
        data : ndarray
            Rank 2 array containing the data set.
        levs : ndarray
            Rank 2 array indicating the membership level of each data point in
            each cluster. levs[i][j] is the level to which the ith data point
            belongs to the jth cluster.
        p : float
            Determines the influence of the weights.  Should be between 1 and
            infinity.  Values closer to 1 yield more distinct centroids.
            Larger values lead to centroids which approach the global centroid.
            Should always be 1 for exclusive clustering.
        method : character
            Specifies the method used to find the centroid.  See
            singleclustercentroid for options.
        weights : ndarray
            Optional.  If given, a rank 1 array with length equal to the number
            of columns in data.  Entries specify the weight for each dimension
            in the distance function.  Only needed if a medoid method is being 
            used and dimensions are not equally weighted.
        distancematrix : ndarray
            Optional.  Used to save time when calculating centroids using a
            medoid (o) method.  Passing distancematrix prevents this function
            from calculating it and thus this option is mostly useful when
            running several functions that require knowledge of the distance
            matrix and would otherwise have to calculate it themselves.
    Returns:
        cdata : ndarray or list of list of ndarray and ndarray
            Rank 2 array containing the centroids.  Each row is a centroid.
    See Also:
        singleclustercentroid
    """
    cdata = []
    check = levscheck(levs)
    if not check[0]:
        if len(check[1]) > 0:
            warnings.warn('levs is not properly normalized.',UserWarning,stacklevel=2)
        if len(check[2]) > 0:
            warnings.warn('levs has empty clusters.',UserWarning,stacklevel=2)
        if len(check[3]) > 0:
            warnings.warn('levs has overfull clusters.',UserWarning,stacklevel=2)
    if distancematrix is None and method[0] == 'o':
        distancematrix = fulldistancematrix(data,weights,method[1:])
    for i in range(len(levs[0])):
        cdata.append(singleclustercentroid(data,levs[:,i],p,method,weights,distancematrix))
    cdata = numpy.array(cdata)
    return cdata
    

def old_SSE(data,clusterid,method='a',dist='e',transpose=False):
    """Calculates the Sum of Squared Error for a given clustering solution.
    
    The old prefix is used because of the use of clusterid to specify which 
    data points belong to which clusters.  For exclusive clustering, clusterid 
    works fine, but fuzzy clustering requires a levs array.  Since a levs array
    can also be used in exclusive clustering, it is more general and thus the 
    prefered way of identifying cluster membership in this package.
    
    This is a legacy function and is kept primarily to aid in conversions to
    and from PyCluster.
    
    Parameters:
        data : ndarray
            Rank 2 array containing the data set.
        clusterid : ndarray
            Rank 1 array with length equal to the number of data points.  
            Elements of clusterid should be integers identifying the cluster to
            which each data point belongs. Either clusterid or mems must be
            provided.  If both are provided, mems is used and clusterid is 
            ignored.
        method : character
            Method specifies whether the arithmetic mean (a, default) or the
            median (m) is to be used to find the centroid.
        dist : string
            Specifies the distance function to use.
        transpose : boolean
            Sets whether data points are columns (True) or rows (False, 
            default) of data.
    Returns:
        sse : float
            The sum of squared error.  Lower values indicate a better
            clustering solution, all other factors being equal.
    See Also:
        singleclustercentroid, distances.distance.
    """
    warnings.warn('old_SSE is a legacy fucntion and is kept primarily to aid in conversions to and from PyCluster.  If you are not using PyCluster it is recommended that you modify your program to use SEmatrix instead.',DeprecationWarning,stacklevel=2)
    cdata = old_clustercentroids(data,clusterid=clusterid,method=method,transpose=transpose)
    sse = 0.
    if transpose:
        for i in range(len(data[0])):
            sse += (distances.distance(data[:,i],cdata[:,clusterid[i]],dist=dist))**2
    else:
        for i in range(len(data)):
            sse += (distances.distance(data[i],cdata[clusterid[i]],dist=dist))**2
    return sse

def SSE(data,levs,p=1.,method='a',dist='e'):
    """Calculates the sum of squared error for a given clustering solution.
    
    This is the equivalent of summing the SEmatrix result into a single value.
    Does not work for cdata in which a multivalued mode warning was raised.
    There are no plans to update it to do so.
    
    This is a legacy function.

    Parameters:
        data : ndarray
            Rank 2 array containing the data set.
        levs : ndarray
            Rank 2 array indicating the membership level of each data point in
            each cluster. levs[i][j] is the level to which the ith data point
            belongs to the jth cluster if transpose is False (default) or the
            level to which the jth data point belongs to the ith cluster if 
            transpose is True.
        p : float
            Determines the influence of the weights.  Should be between 1 and
            infinity.  Values closer to 1 yield more distinct centroids.
            Larger values lead to centroids which approach the global centroid.
            Should always be 1 for exclusive clustering.
        method : character
            Specifies the method used to find the centroid.  See
            singleclustercentroid for options.
        dist : string
            Specifies the distance function to use.
    Returns:
        sse : float
            The sum of squared error.  Lower values indicate a better
            clustering solution, all other factors being equal.
    """
    warnings.warn('SSE is a legacy fucntion.  Use numpy.sum(SEMatrix) instead.',DeprecationWarning,stacklevel=2)
    cdata = clustercentroids(data,levs,p,method=method)
    sse = 0.
    for i in range(len(data)):
        for j in range(len(cdata)):
            sse += levs[i][j]**p*(distances.distance(data[i],cdata[j],dist=dist))**2
    return sse

def point_SSE(data,levs,p=1.,method='a',dist='e'):
    """Calculates the contribution to the sum of squared error for each point.
    
    This is equivalent to summing the SEmatrix result over the point axis.
    Does not work for cdata in which a multivalued mode warning was raised.
    There are no plans to update it to do so.
    
    This is a legacy function.

    Parameters:
        data : ndarray
            Rank 2 array containing the data set.
        levs : ndarray
            Rank 2 array indicating the membership level of each data point in
            each cluster. levs[i][j] is the level to which the ith data point
            belongs to the jth cluster if transpose is False (default) or the
            level to which the jth data point belongs to the ith cluster if 
            transpose is True.
        p : float
            Determines the influence of the weights.  Should be between 1 and
            infinity.  Values closer to 1 yield more distinct centroids.
            Larger values lead to centroids which approach the global centroid.
            Should always be 1 for exclusive clustering.
        method : character
            Specifies the method used to find the centroid.  See
            singleclustercentroid for options.
        dist : string
            Specifies the distance function to use.
    Returns:
        sse : ndarray
            Rank 1 array containing the contribution to the sse for each point.
    """
    warnings.warn('point_SSE is a legacy fucntion.  Use numpy.sum(SEMatrix,axis=#) instead.',DeprecationWarning,stacklevel=2)
    cdata = clustercentroids(data,levs,p,method=method)
    sse = numpy.zeros(len(data),dtype=float)
    for i in range(len(data)):
        for j in range(len(cdata)):
            sse[i] += levs[i][j]**p*(distances.distance(data[i],cdata[j],dist=dist))**2
    return sse

def SEmatrix(data,levs,p=1.,method='a',dist='e',weights=None,cdata=None,distancematrix=None,link='m'):
    """Calculates the squared error matrix by point and cluster.
    
    While the transpose parameter has been removed, the behavior formerly
    obtained by setting transpose to True can be duplicated by the command
    numpy.transpose(SEmatrix(numpy.transpose(data),...)).

    Parameters:
        data : ndarray
            Rank 2 array containing the data set.
        levs : ndarray
            Rank 2 array indicating the membership level of each data point in
            each cluster. levs[i][j] is the level to which the ith data point
            belongs to the jth cluster.
        p : float
            Determines the influence of the weights.  Should be between 1 and
            infinity.  Values closer to 1 yield more distinct centroids.
            Larger values lead to centroids which approach the global centroid.
            Should always be 1 for exclusive clustering.
        method : character
            Specifies the method used to find the centroid.  See
            singleclustercentroid for options.  Not required if cdata is given.
        dist : string
            Specifies the distance function to use.
        weights : ndarray
            Optional.  If given, a rank 1 array with length equal to the number
            of rows in data.  Entries specify the weight for each dimension in
            the distance function.  Only needed if a medoid method is being
            used, dimensions are not equally weighted, and cdata is not given.
        cdata : ndarray
            Rank 2 array containing the centroids.
        distancematrix : ndarray
            The distance matrix for the data (i.e. the results of a 
            fulldistancematrix call).  Only used to speed up the call of 
            clustercentroid when cdata is not given.
        link : string
            In cases where cdata contains at least one multi-modal centroid,
            link is used to specify how the distance between each point and the
            multi-modal centroid(s) is found.  Possible options are:
            m - maximum link (largest pair-wise distance, default)
            s - single link (smallest pair-wise distance)
            a - average link (average pair-wise distance)
    Returns:
        sse : ndarray
            Rank 2 array containing the contribution to the sse for each 
            point/cluster contribution.  Row indecies correspond to points 
            and column indecies to clusters.
    """
    if cdata is None:
        cdata = clustercentroids(data,levs,p,method,weights,distancematrix)
    sse = numpy.zeros((len(data),len(levs[0])),dtype=float)
    for i in range(len(data)):
        if cdata.dtype.type is numpy.object_:
            for j in range(len(cdata)):
                k = map(len,cdata[j])
                index = numpy.zeros_like(k)
                d = numpy.zeros(numpy.prod(k))
                for n in range(len(d)):
                    cent = numpy.zeros(len(index))
                    for m in range(len(index)):
                        cent[m] = cdata[j,m][index[m]]
                    d[n] = distances.distance(data[i],cent,dist=dist)
                    index[0] += 1
                    for m in range(len(index)-1):
                        if index[m] == k[m]:
                            index[m] = 0
                            index[m+1] += 1
                if link == 'm':
                    sse[i][j] += levs[i][j]**p*(d.max())**2
                elif link == 's':
                    sse[i][j] += levs[i][j]**p*(d.min())**2
                elif link == 'a':
                    sse[i][j] += levs[i][j]**p*(numpy.mean(d))**2
                else:
                    raise ValueError('Link type not supported.')
        else:
            for j in range(len(cdata)):
                sse[i][j] += levs[i][j]**p*(distances.distance(data[i],cdata[j],dist=dist))**2
    return sse

def levscompare(levs1,levs2,rtol=1.0000000000000001e-005,atol=1e-008):
    """Compares two levs arrays to see if they are equivalent.
    
    Since there should be no preference for which cluster comes "first" in a
    levs array, it is possible for levs1 == levs2 or 
    numpy.allclose(levs1,levs2) to return False even when both levs arrays
    correspond to the same clustering solution.  However, given that the data
    point order is unchanged, then the two levs arrays should only differ by 
    column swaps.  Knowing this, this function compares the two levs arrays to
    see if they are the same.
    
    While the transpose parameter has been removed, the behavior formerly
    obtained by setting transpose to True can be duplicated by the command
    levscompare(numpy.transpose(levs1),numpy.transpose(levs2),...).

    Parameters:
        levs1, levs2 : ndarray
            Rank 2 array indicating the membership level of each data point in
            each cluster.  Each is usually the result of a kmeans or cmeans run 
            with random starting conditions.
        rtol : float
            The allowable relative error in levs between elements in levs1 and
            levs2.
        atol : float
            The allowable absolute error in levs between elements in levs1 and
            levs2.  levs1[:,i] is considered equal to levs2[:,j] when
            (rtol*levs2[:,j])+atol < abs(levs1[:,i]-levs2[:,j])
    Returns:
        equiv : boolean
            True if levs1 and levs2 correspond to the same clustering solution.
    """
    if levs1.shape != levs2.shape:
        equiv = False
    else:
        matches = []
        for i in numpy.transpose(levs1):
            for j in range(len(levs2[0])):
                if numpy.allclose(i,levs2[:,j],rtol,atol) and j not in matches:
                    matches.append(j)
                    break
        matches.sort()
        equiv = matches == range(len(levs2[0]))
    return equiv
    
def statsversion():
    print 'cluster/stats.py'
    print 'Created 14 November, 2007'
    print 'by R. Padraic Springuel'
    print 'Version %s modified %s' % (statsversionnum,statsmodified)
    print 'Most recent modification by %s' % statsmodifier
    return
      