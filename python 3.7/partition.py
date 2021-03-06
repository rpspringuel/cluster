"""Partitional clustering algorithms and functions related to them.

Partitional clustering produces unnested clusters from the data.  The main
algorithm used to implement this kind of clustering is the k-means algorithm
when exclusive clustering is desired and the c-means algorithm when fuzzy 
clustering is desired.  Both of those algorithms are implemented here.

A complete version history and licence and copyright information are located
in the source code.
"""

import numpy
from . import distances
import scipy
from . import _support
from . import stats
import warnings

def kmeans(data,nclusters=2,weights=None,method='a',dist='e',initial=None,threshold=0.05):
    """Exclusive partitional clustering.
    
    Data points are grouped into the given number of clusters based on their
    similarity to a set of prototypes (either randomly generated or user 
    supplied).  The prototypes are then updated to be more representative of
    their groups and the process is then repeated.  This repetition occurs
    until there is little to no change in the group assignments.
    Because of the non-deterministic nature of the k-means algorithm for
    randomly generated intitial centroids, the usual practice is to run the
    algorithm several times and to use the most frequently occuring solution.
    This code does not implement that practice, leaving it up to the user to
    determine if that is appropriate.  Furthermore, this code is even less
    deterministic than normal because it uses the random reassignment of a
    single point to handle an empty cluster.
    
    While the transpose parameter has been removed, the behavior formerly
    obtained by setting transpose to True can be duplicated by the command
    numpy.transpose(kmeans(numpy.transpose(data),...)).
    
    Parameters:
        data : ndarray
            Expects a rank 2 array.  Contains the data to be clustered.
        nclusters : integer
            The number of clusters that the data should be divided into.
        weights : ndarray
            Optional.  Expects a rank 1 array with length equal to the number
            of columns in data.  Entries are weights for each dimension in
            calculating the distance.
        method : character
            Specifies the method to be used to find the cluster centroids.  See
            stats.singleclustercentroid for available methods.
        dist : string
            Specifies the distance function to use when finding the distance
            between points and the centroids.  See distances.distance for
            available functions.
        initial : ndarray
            Optional.  Expects a rank 2 array with dimensions nclusters x 
            # columns in data containing the initial guess for the locations of
            the centroids or a rank 2 array with dimensions # rows in data x
            nclusters containing the initial guess for levs.  If none is given
            random guesses will be used.
        threshold : float
            Percent of points which can change cluster on final iteration.
            Function stops the first time the percentage of points changing
            cluster drops to or below this number.
    Returns:
        levs : ndarray
            A rank 2 array with dimensions # rows of data x nclusters
            containing 0's and 1's.  Each row/column should contain one
            and only one 1 to indicate which cluster that data point belongs
            to.  Each column/row indicates a different cluster.     
    See Also:
        stats.singleclustercentroid, distances.distance
    """
    if initial is None:
        initial = numpy.random.random((nclusters,len(data[0])))*(numpy.max(data)-numpy.min(data))+numpy.min(data)
    elif stats.levscheck(initial)[0]:
        initial = stats.clustercentroids(data,initial,1.,method)
    levs = numpy.zeros((len(data),nclusters))
    again = True
    while again:
        levs_new = numpy.zeros((len(data),nclusters))
        for i in range(len(data)):
            d = list(numpy.apply_along_axis(distances.distance,1,initial,data[i],weights,dist))
            levs_new[i,d.index(min(d))] = 1
        if numpy.sum(numpy.abs(levs_new-levs))/(2*len(data[0])) <= threshold:
            again = False
        test = stats.levscheck(levs_new)
        if not test[0]:
            again = True
            for i in test[2]:
                j = numpy.random.random_integers(len(data))-1
                levs_new[j] = 0
                levs_new[j,i] = 1
        initial = stats.clustercentroids(data,levs_new,1.,method)
        levs = levs_new
    return levs
    
def cmeans(data,nclusters=2,weights=None,p=2.,method='a',dist='e',initial=None,rtol=1.0000000000000001e-005,atol=1e-008):
    """Fuzzy partitional clustering.
    
    While the transpose parameter has been removed, the behavior formerly
    obtained by setting transpose to True can be duplicated by the command
    numpy.transpose(cmeans(numpy.transpose(data),...)).
    
    Parameters:
        data : ndarray
            Expects a rank 2 array.  Contains the data to be clustered.
        nclusters : integer
            The number of clusters that the data should be divided into.
        weights : ndarray
            Optional.  Expects a rank 1 array with length equal to the number
            of columns in data.  Entries are weights for each dimension in
            calculating the distance.
        p : float
            Determines the influence of the weights.  Should be between 1 and
            infinity.  Values closer to 1 yield more distinct centroids.
            Larger values lead to centroids which approach the global centroid.
            A value of exactly 1 cooresponds to using kmeans.
        method : character
            Specifies the method to be used to find the cluster centroids.  See
            stats.singleclustercentroid for available methods.
        dist : string
            Specifies the distance function to use when finding the distance
            between points and the centroids.  See distances.distance for
            available functions.
        initial : ndarray
            Optional.  Expects a rank 2 array with dimensions # rows of data x
            nclusters containing the initial guess for levs.  If none is given
            random guesses will be used.
        rtol : float
            The allowable relative error in levs between iterations.  Must be
            positive and << 1.0.  Algorithm stops when change in levs is below
            this for all elements.
        atol : float
            The allowable absolute error in levs between iterations.  Usually
            comes into play for those elements of the new levs that are very 
            small or zero; it says how small the previous iteration's levs must
            be also.
    Returns:
        levs : ndarray
            A rank 2 array with dimensions # rows of data x nclusters
            containing the level to which each data point belongs to each
            cluster.
    See Also:
        stats.singleclustercentroid, distances.distance
    """
    if p == 1:
        if initial is None:
            levs = kmeans(data,nclusters,weights,method,dist)
        else:
            cdata = stats.clustercentroids(data,initial,p,method)
            levs = kmeans(data,nclusters,weights,method,dist,cdata)
    else:
        if initial is None:
            initial = numpy.random.random((len(data),nclusters))
            initial *= 1./numpy.sum(initial,axis=0)
        levs = numpy.zeros_like(initial)
        again = True
        while again:
            cdata = stats.clustercentroids(data,initial,p,method)
            for i in range(len(data)):
                d = numpy.apply_along_axis(distances.distance,1,cdata,data[i],weights,dist)
                d = (1/d**2)**(1/(p-1))
                levs[i] = d/numpy.sum(d)
            if numpy.allclose(initial,levs,rtol,atol):
                again = False
            initial = levs
    return levs
    
def cmeans_noise(data,nclusters=2,weights=None,p=2.,method='a',dist='e',initial=None,rtol=1.0000000000000001e-005,atol=1e-008,l=1.):
    """Fuzzy partitional clustering with a noise cluster.
    
    Similar to normal c-means except that a "noise" cluster is added.  All data
    points are considered to be a constant distance from this noise cluster at
    each iteration.  The noise cluster will thus "absorb" points which are not
    well characterized by any of the "real" clusters.
    
    While the transpose parameter has been removed, the behavior formerly
    obtained by setting transpose to True can be duplicated by the command
    numpy.transpose(cmeans_noise(numpy.transpose(data),...)).
    
    Parameters:
        data : ndarray
            Expects a rank 2 array.  Contains the data to be clustered.
        nclusters : integer
            The number of clusters that the data should be divided into.  This
            does not include the noise cluster.
        weights : ndarray
            Optional.  Expects a rank 1 array with length equal to the number
            of rows.  Entries are weights for each dimension in calculating the
            distance.
        p : float
            Determines the influence of the weights.  Should be between 1 and
            infinity.  Values closer to 1 yield more distinct centroids.
            Larger values lead to centroids which approach the global centroid.
            A value of exactly 1 is invalid since it would correspond to using
            kmeans and kmeans can't be done with a noise cluster.
        method : character
            Specifies the method to be used to find the cluster centroids.  See
            stats.singleclustercentroid for available methods.
        dist : string
            Specifies the distance function to use when finding the distance
            between points and the centroids.  See distances.distance for
            available functions.
        initial : ndarray
            Optional.  Expects a rank 2 array with dimensions # rows of data x
            nclusters containing the initial guess for levs.  If none is given
            random guesses will be used.
        rtol : float
            The allowable relative error in levs between iterations.  Must be
            positive and << 1.0.  Algorithm stops when change in levs is below
            this for all elements.
        atol : float
            The allowable absolute error in levs between iterations.  Usually
            comes into play for those elements of the new levs that are very 
            small or zero; it says how small the previous iteration's levs must
            be also.
        l : float
            Parameter specfying the proportion of points that should be viewed
            as outliers (i.e. primarily in the noise cluster).  Higher values
            lead to more points being considered outliers.  At l = inf, all
            points are outliers.  At l = 0, none are.
    Returns:
        levs : ndarray
            A rank 2 array with dimensions # rows of data x nclusters+1
            containing the level to which each data point belongs to each
            cluster.  The last column/row is the noise cluster.
    See Also:
        stats.singleclustercentroid, distances.distance
    """
    if p == 1:
        raise ValueError('p cannot be 1 when a noise cluster is present.')
    else:
        if initial is None:
            initial = numpy.random.rand((len(data),nclusters))
            initial *= 1./numpy.sum(initial,axis=0)        
        initial = numpy.append(initial,numpy.zeros((len(data),1)),axis=1)
        levs = numpy.zeros_like(initial)
        again = True
        while again:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                cdata = stats.clustercentroids(data,initial,p,method)
            d = numpy.zeros_like(levs)
            for i in range(len(data)):
                d[i] = numpy.apply_along_axis(distances.distance,1,cdata,data[i],weights,dist)
            d[:,-1] = 0
            d[:,-1] = numpy.sum(d**2)/(nclusters*len(data)*l)
            d = (1/d**2)**(1/(p-1))
            levs = d/numpy.apply_over_axes(numpy.sum,d,1)
            if numpy.allclose(initial,levs,rtol,atol):
                again = False
            initial = levs
    return levs
