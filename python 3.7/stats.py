"""Cluster _support which are method independant.

Routines which calculate _support for data and clustering results.
_support in this package do not care what the particluar clustering
methodology is.

A complete version history and licence and copyright information are located
in the source code.
"""

import numpy
from . import distances
import scipy
from . import _support
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
                    print('%i%% complete' % current)
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
                    print('%i%% complete' % current)
    return dm

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
                k = list(map(len,cdata[j]))
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
        equiv = matches == list(range(len(levs2[0])))
    return equiv
