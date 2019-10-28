"""Routines for finding the distance between two vectors.

This subpackage duplicates and expands on the abilities of Pycluster to find
the distance between two data points.

Masking is handled differently from Pycluster.  Instead of a seperate mask
argument which specifies which dimensions are missing for a particular data
vector the program makes use of numpy's NaN variable for missing data.  In
this fashion, missing data is embeded directly in the data vectors that are
passed to these distance functions.

All distances functions defined here are meant to calculate normalized versions
of the distance where ever possible.

A complete version history and licence and copyright information are located
in the source code.
"""


##########################
## Liscense Information ##
##########################

###############################################################################
#Copyright (c) 2007, R. Padraic Springuel                                     #
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
import scipy.stats
import warnings

def distance(a,b,weights=None,dist='e'):
    """External interface for distance functions.
    
    This function allows other packages to make use of this one without 
    requiring they be updated each time a new way of measuring the distance 
    between two vectors is added here.  So long as this function is kept upto 
    date, all ways of measuring the distance between two vectors that are in 
    this module will be available to any program calling this function.
    
    Parameters:
        a,b : ndarray
            The data points.  Expects two rank 1 arrays of the same length.
        weights : ndarray
            The weights for each dimension.  Expects rank 1 array of same 
            length as a & b.
        dist : string
           Specifies which distance measure is used.  Defaults to euclidian.
            Currently defined distances are:
            e - euclidean
            p - squared euclidian
            b - cityblock
            h - hamming
            c - pearson
            a - absolute pearson
            u - uncentered pearson
            r - arccosine of uncentered pearson
            x - absolute uncentered pearson
            s* - spearman
            k - kendall
            t - the modified simple matching of Rogers and Tanimoto
            y - the modified simple matching of Sokal and Sneath
            j - the jaccard
            d - modified jaccard of Dice 
            z - the modified jaccard of Sokal and Sneath
            L* - the general Minkowski metric
            Linf - Chebychev distance
            Notes: For the spearman distance the wildcard (*) should be one of
            the abbreviations for a pearson distance (c, a, u, r, or x).
            For the general minkowski metric the wildcard (*) should be
            replaced with the integer specifying which minkowski metric you
            want.  Also, L1 is equivalent to the cityblock distance and L2 is 
            equivalent to the euclidean distance.
    Returns:
        d : float
            The distance between the two data points.
    See Also:
        euclidian, peuclidian, cityblock, pcityblock, hamming, pearson, 
        abspearson, upearson, acosine, absupearson, spearman, kendall, 
        rogerstanimoto, sokalsneathsym, jaccard, dice, sokalsneathasym,
        minkowski, & chebychev
    """
    if type(a) is not numpy.ndarray and type(b) is not numpy.ndarray:
        raise TypeError('Vectors must have type numpy.ndarray')
    elif type(a) is not numpy.ndarray:
        raise TypeError('First vector must have type numpy.ndarray')
    elif type(b) is not numpy.ndarray:
        raise TypeError('Second vector must have type numpy.ndarray')
    elif len(a) != len(b):
        raise ValueError('Vectors must have the same length')
    elif not (weights is None) and len(weights) != len(a):
        raise ValueError('There must be the same number of weights as the vector length')
    elif numpy.isnan(a*b).all():
        d = numpy.nan
    else:
        if not (weights is None) and dist[0] == 's':
            warnings.warn('weights are not well defined for spearman distances and will be ignored',UserWarning,stacklevel=2)
        elif not (weights is None) and dist == 'k':
            warnings.warn('weights are not well defined for kendal distances and will be ignored',UserWarning,stacklevel=2)
        elif not (weights is None) and dist == 'Linf':
            warnings.warn('weights are not well defined for chebychev distances and will be ignored',UserWarning,stacklevel=2)
        a = a.astype('float')
        b = b.astype('float')
        if weights is None:
            weights = numpy.ones_like(a)
        if dist == 'e':
            d = euclidean(a,b,weights)
        elif dist == 'p':
            d = sqeuclidean(a,b,weights)
        elif dist == 'b':
            d = cityblock(a,b,weights)
        elif dist == 'h':
            d = hamming(a,b,weights)
        elif dist == 'c':
            d = pearson(a,b,weights)
        elif dist == 'a':
            d = abspearson(a,b,weights)
        elif dist == 'u':
            d = upearson(a,b,weights)
        elif dist == 'r':
            d = acosine(a,b,weights)
        elif dist == 'x':
            d = absupearson(a,b,weights)
        elif dist[0] == 's':
            d = spearman(a,b,dist[1])
        elif dist == 'k':
            d = kendall(a,b)
        elif dist == 't':
            d = rogerstanimoto(a,b,weights)
        elif dist == 'y':
            d = sokalsneathsym(a,b,weights)
        elif dist == 'j':
            d = jaccard(a,b,weights)
        elif dist == 'd':
            d = dice(a,b,weights)
        elif dist == 'z':
            d = sokalsneathasym(a,b,weights)
        elif dist == 'Linf':
            d = chebychev(a,b)
        elif dist[0] == 'L':
            d = minkowski(a,b,weights,int(dist[1:]))
        else:
            message = 'Unrecognized distance fucntion (%s) provided.' % dist
            raise ValueError(message)
    return d

def euclidean(a,b,weights):
    """The normalized euclidian distance between two data points.
    
    Parameters:
        a,b : ndarray
            The data points.  Expects two rank 1 arrays of the same length.
            All elements must be between 0 and 1 (inclusive) in order for
            normalization to work.
        weights : ndarray
            The weights for each dimension.  Expects rank 1 array of same length
            as a & b.
    Returns:
        d : float
            The normalized euclidian distance between the two data points.
    Notes:
        The normalized euclidian distance is defined mathematically as:
                  / 1 --
            d =  /  - >  w[i](a[i]-b[i])**2
               \/   N --
        where a[i] and b[i] are the ith elements of a & b respectively, N is 
        the weighted common dimensionality of the vectors, and w[i] is the 
        weight of the ith dimension.
    """
    result = weights*(a-b)**2
    N = numpy.nansum(~numpy.isnan(a)*~numpy.isnan(b)*weights)
    return numpy.sqrt(numpy.nansum(result)/N)

def sqeuclidean(a,b,weights):
    """The normalized euclidian distance between two data points.
    
    Parameters:
        a,b : ndarray
            The data points.  Expects two rank 1 arrays of the same length.
            All elements must be between 0 and 1 (inclusive) in order for
            normalization to work.
        weights : ndarray
            The weights for each dimension.  Expects rank 1 array of same length
            as a & b.
    Returns:
        d : float
            The normalized euclidian distance between the two data points.
    Notes:
        The normalized euclidian distance is defined mathematically as:
                1 --
            d = - >  w[i](a[i]-b[i])**2
                N --
        where a[i] and b[i] are the ith elements of a & b respectively, N is 
        the weighted common dimensionality of the vectors, and w[i] is the 
        weight of the ith dimension.
    """
    result = weights*(a-b)**2
    N = numpy.nansum(~numpy.isnan(a)*~numpy.isnan(b)*weights)
    return numpy.nansum(result)/N
    
def cityblock(a,b,weights):
    """Calculates the normalized city block distance between two data points.
    
    Parameters:
        a,b : ndarray
            The data points.  Expects two rank 1 arrays of the same length.
            All elements must be between 0 and 1 (inclusive) in order for
            normalization to work.
        weights : ndarray
            The weights for each dimension.  Expects rank 1 array of same 
            length as a & b.
    Returns:
        d : float
            The normalized city block distance between the two data points.
    Notes:
        The normalized city block distance is defined mathematically as:
                1 --
            d = - >  w[i]|a[i]-b[i]|
                N --
        where a[i] and b[i] are the ith elements of a & b respectively, N is 
        the weighted common dimensionality of the vectors, and w[i] is the 
        weight of the ith dimension.
    """
    result = weights*numpy.abs((a-b))
    N = numpy.nansum(~numpy.isnan(a)*~numpy.isnan(b)*weights)
    return numpy.nansum(result)/N

def hamming(a,b,weights):
    """Calculates the hamming distance between two data points.
    
    Also known as the matching distance or the simple matching distance
    when applied to binary data.
    Appropriate for binary data where two states are equally informative (e.g.
    male/female) and the code mapping could thus be reversed without change of
    information.  Or for non-binary data where size of difference is
    not important.
    
    Parameters:
        a,b : ndarray
            The data points.  Expects two rank 1 arrays of the same length.
        weights : ndarray
            The weights for each dimension.  Expects rank 1 array of same 
            length as a & b.
    Returns:
        d : float
            The hamming distance between the two data points.
    Notes:
        The hamming distance is defined mathematically as:
                1 --  
            d = - >  w[i](1-D(a[i],b[i]))
                N --
        where D is the kroneker delta, a[i] and b[i] are the ith elemtents of 
        a & b respectively, N is the weighted common dimensionality of the 
        vectors, and w[i] is the weight of the ith dimension.
    """
    result = weights*(a != b)
    N = numpy.nansum(~numpy.isnan(a)*~numpy.isnan(b)*weights)
    return numpy.nansum(result)/N

def pearson(a,b,weights):
    """Distance between two points based on the pearson correlation coefficient.
    
    By treating each data point as a one half of a list of ordered pairs it is 
    possible to calculate the pearson corelation coefficient for the list of 
    ordered pairs.  The pearson corelation coefficient is then converted to a 
    pseudo-distance by subtracting it from 1.
    The definition is taken from Pycluster.
    
    Parameters:
        a,b : ndarray
            The data points.  Expects two rank 1 arrays of the same length.
        weights : ndarray
            The weights for each dimension.  Expects rank 1 array of same 
            length as a & b.
    Returns:
        d : float
            The pearson distance between the two data points.
    Notes:
        The pearson distance is defined mathematically as:
                1 (          1      --                            )
            d = - ( 1 - ----------- >  w[i](a[i]-m[a])(b[i]-m[b]) )
                2 (     N*s[a]*s[b] --                            )
        where a[i] & b[i] are the ith elements of a & b respectively, m[a] & 
        m[b] are the weighted means of a & b respectively, s[b] & s[b] are the
        weighted standard deviations of a & b respectively, N is the weighted 
        common dimensionality of the vectors, and w[i] is the weight of the ith
        dimension. Only dimensions for which both vectors have values are used
        when computing the means and standard deviations.
    """
    a = ~numpy.isnan(b)*a
    b = ~numpy.isnan(a)*b
    amean = numpy.nansum(a*weights)/numpy.nansum(~numpy.isnan(a)*weights)
    bmean = numpy.nansum(b*weights)/numpy.nansum(~numpy.isnan(b)*weights)
    astd = numpy.sqrt(numpy.nansum((weights*(a-amean)**2))/numpy.nansum((~numpy.isnan(a)*weights)))
    bstd = numpy.sqrt(numpy.nansum((weights*(b-bmean)**2))/numpy.nansum((~numpy.isnan(b)*weights)))
    result = weights*((a-amean)/astd)*((b-bmean)/bstd)
    N = numpy.nansum(~numpy.isnan(a)*~numpy.isnan(b)*weights)
    return (1. - numpy.nansum(result)/N)/2.

def abspearson(a,b,weights):
    """Distance between two points based on the pearson correlation coefficient.
    
    By treating each data point as half of a list of ordered pairs it is 
    possible to caluclate the pearson correlation coefficent for the list. The
    correlation coefficent is then converted into a pseudo-distance by 
    subtracting its absolute value from 1.  Used over the pearson distance when
    linearity of correlation, and not slope of correlation, is a more 
    appropriate measure of similarity.
    
    Parameters:
        a,b : ndarray
            The data points.  Expects two rank 1 arrays of the same length.
        weights : ndarray
            The weights for each dimension.  Expects rank 1 array of same 
            length as a & b.
    Returns:
        d : float
            The absolute pearson distance between the two data points.
    Notes:    
        The absolute pearson distance is defined mathematically as:
                    |      1      --                            |
            d = 1 - | ----------- >  w[i](a[i]-m[a])(b[i]-m[b]) |
                    | N*s[a]*s[b] --                            |
        where a[i] & b[i] are the ith elements of a & b respectively, m[a] & 
        m[b] are the weighted means of a & b respectively, s[b] & s[b] are the
        weighted standard deviations of a & b respectively, N is the weight
        common dimensionality of the vectors, and w[i] is the weight of the ith
        dimension. Only dimensions for which both vectors have values are used 
        when computing the means and standard deviations.
    """
    return 1. - numpy.abs((pearson(a,b,weights)-1))

def upearson(a,b,weights):
    """Distance between two points based on the pearson correlation coefficient.
    
    By treating each data point as a one half of a list of ordered pairs it is 
    possible to calculate the pearson corelation coefficient for the list of 
    ordered pairs.  The pearson corelation coefficient is then converted to a 
    pseudo-distance by subtracting it from 1.  This function assumes the 
    ordered pairs are centered around 0.
    The definition is taken from Pycluster.
    
    Parameters:
        a,b : ndarray
            The data points.  Expects two rank 1 arrays of the same length.
        weights : ndarray
            The weights for each dimension.  Expects rank 1 array of same 
            length as a & b.
    Returns:
        d : float
            The uncentered pearson distance between the two data points.
    See Also:
        pearson
    Notes:
        The uncentered pearson distance is defined mathematically as:
                  (            --                     )
                  (            >  w[i]a[i]b[i]        )
                1 (            --                     )
            d = - ( 1 - ----------------------------- )
                2 (     --             --             )
                  (     >  w[i]a[i]**2 >  w[i]b[i]**2 )
                  (     --             --             )
        where a[i] & b[i] are the ith elements of a & b respectively and w[i] 
        is the weight of the ith dimension. Only dimensions for which both 
        vectors have values are used when computing the sums of squares.
    """
    a = ~numpy.isnan(b)*a
    b = ~numpy.isnan(a)*b
    result = weights*a*b
    d1 = weights*a**2
    d2 = weights*b**2
    return (1. - numpy.nansum(result)/numpy.sqrt((numpy.nansum(d1)*numpy.nansum(d2))))/2.

def absupearson(a,b,weights):
    """Distance between two points based on the pearson correlation coefficient.
    
    By treating each data point as half of a list of ordered pairs it is 
    possible to caluclate the pearson correlation coefficent for the list. The 
    correlation coefficent is then converted into a pseudo-distance by 
    subtracting its absolute value from 1.  This function assumes the ordered 
    pairs are centered around 0. Used over the uncentered pearson distance when
    linearity of correlation, and not slope of correlation, is a more 
    appropriate measure of similarity.
    
    Parameters:
        a,b : ndarray
            The data points.  Expects two rank 1 arrays of the same length.
        weights : ndarray
            The weights for each dimension.  Expects rank 1 array of same 
            length as a & b.
    Returns:
        d : float
            The absolute uncentered pearson distance between the two data 
            points.
    See Also:
        abspearson
    Notes:
        The absolute uncentered pearson distance is defined mathematically as:
                    |        --                     |
                    |        >  w[i]a[i]b[i]        |
                    |        --                     |
            d = 1 - | ----------------------------- |
                    | --             --             |
                    | >  w[i]a[i]**2 >  w[i]b[i]**2 |
                    | --             --             |
        where a[i] & b[i] are the ith elements of a & b respectively and w[i] 
        is the weight of the ith dimension. Only dimensions for which both 
        vectors have values are used when computing the sums of squares.
    """
    return 1. - numpy.abs((2.*upearson(a,b,weights)-1))   

def acosine(a,b,weights):
    """Distance between two points based on the pearson correlation coefficient.
    
    By treating each data point as half of a list of ordered pairs it is 
    possible to caluclate the pearson correlation coefficent for the list. 
    Since the pearson correlation coefficent for a sample can also be thought 
    of as the cosine of the angle between the two vectors,  the distance is 
    defined as its arccosine.  This function assumes the ordered pairs are 
    centered around 0. Used over the uncentered pearson distance when linearity
    of correlation, and not slope of correlation, is a more appropriate measure
    of similarity.
    
    Parameters:
        a,b : ndarray
            The data points.  Expects two rank 1 arrays of the same length.
        weights : ndarray
            The weights for each dimension.  Expects rank 1 array of same 
            length as a & b.
    Returns:
        d : float
            The inverse cosine pearson distance between the two data points.
    See Also:
        pearson, upearson
    Notes:
        This distance is defined mathematically as:
                         (        --                     )
                         (        >  w[i]a[i]b[i]        )
                1        (        --                     )
            d = -- arccos( ----------------------------- )
                pi       ( --             --             )
                         ( >  w[i]a[i]**2 >  w[i]b[i]**2 )
                         ( --             --             )
        where a[i] & b[i] are the ith elements of a & b respectively and w[i] 
        is the weight of the ith dimension. Only dimensions for which both 
        vectors have values are used when computing the sums of squares.
    """
    a = ~numpy.isnan(b)*a
    b = ~numpy.isnan(a)*b
    result = weights*a*b
    d1 = weights*a**2
    d2 = weights*b**2
    return (numpy.arccos(numpy.nansum(result)/numpy.sqrt((numpy.nansum(d1)*numpy.nansum(d2)))))/numpy.pi

def spearman(a,b,dist = 'c'):
    """Pearson distance with rank arrays instead of data arrays.
    
    Data values are replaced by their relative rank in the vector defining the
    point and then the pearson correlation is used on the rank vectors.
    Originally proposed by Spearman, C. (1904). The Proof and Measurement of 
    Association between Two Things. American Journal of Psychology, 15(1), 
    72-101.
    If data is already ranked, then you can use the corresponding pearson 
    function directly.
    
    Parameters:
        a,b : ndarray
            The data points.  Expects two rank 1 arrays of the same length.
    Returns:
        d : float
            The spearman distance between the two data points.
    See Also:
        pearson,abspearson,upearson,absupearson,acosine
    """
    #Because nan variables (missing data) cannot be ranked they screw up the 
    #ranking function and must be eliminated before hand.
    missing = numpy.isnan(a)+numpy.isnan(b)
    arankable = []
    brankable = []
    for i in range(len(missing)):
        if not missing[i]:
            arankable.append(a[i])
            brankable.append(b[i])
    arank = scipy.stats.rankdata(numpy.array(arankable))
    brank = scipy.stats.rankdata(numpy.array(brankable))
    if dist == 'c':
        d = pearson(arank,brank,numpy.ones_like(arank))
    elif dist == 'a':
        d = abspearson(arank,brank,numpy.ones_like(arank))
    elif dist == 'u':
        d = upearson(arank,brank,numpy.ones_like(arank))
    elif dist == 'r':
        d = acosine(arank,brank,numpy.ones_like(arank))
    elif dist == 'x':
        d = absupearson(arank,brank,numpy.ones_like(arank))
    return d

def kendall(a,b):
    """Calculates the distance between two points based on kendall's tau.
    
    The calculation of kendall's tau is described in Kendall, M. G. (1962).
    Rank Correlation Methods (London: Charles Grifin & Company Limited).
    This function incorporates the methods for dealing with ties discussed
    in chapter 3 of said book and the denominator for tau_b which is identified
    as being more appropriate for measuring agreement.
    To convert tau to a normalized distance it is subtracted from 1 and divided
    by 2.
    
    Parameters:
        a,b : ndarray
            The data points.  Expects two rank 1 arrays of the same length.
    Returns:
        d : float
            The kedall distance between the two data points.
    """
    #Because nan variables (missing data) cannot be ranked they screw up the 
    #ranking function and must be eliminated before hand.
    missing = numpy.isnan(a)+numpy.isnan(b)
    arankable = []
    brankable = []
    for i in range(len(missing)):
        if not missing[i]:
            arankable.append(a[i])
            brankable.append(b[i])
    arank = scipy.stats.rankdata(numpy.array(arankable))
    brank = scipy.stats.rankdata(numpy.array(brankable))
    reorder = []
    for i in range(len(arank)):
        reorder.append([arank[i],brank[i]])
    reorder.sort()
    #brankreorder = numpy.array(reorder)[:,1]
    S = 0.
    for i in range(len(reorder)):
        for j in range(i+1,len(reorder)):
            if reorder[i][0] != reorder[j][0]:
                if reorder[i][1] < reorder[j][1]:
                    S += 1.
                elif reorder[i][1] > reorder[j][1]:
                    S -= 1.
    N = numpy.sum(1-missing)
    N = N*(N-1)/2
    aunique = numpy.unique(arank)
    bunique = numpy.unique(brank)
    T = 0
    U = 0
    if len(aunique) < len(arank):
        for i in aunique:
            t = list(arank).count(i)
            if t > 1:
                T += t*(t-1.)/2.
    if len(bunique) < len(brank):
        for i in bunique:
            u = list(brank).count(i)
            if u > 1:
                U += u*(u-1.)/2.
    tau = S/numpy.sqrt((N-T)*(N-U))
    return (1 - tau)/2.
    
def rogerstanimoto(a,b,weights):
    """Hamming distance with similarties weighted extra.
    
    Used in Rogers and Tanimoto (1960).  A computer program for classifying
    plants.  Science, 132, 115-1118.
    
    Parameters:
        a,b : ndarray
            The data points.  Expects two rank 1 arrays of the same length.
        weights : ndarray
            The weights for each dimension.  Expects rank 1 array of same 
            length as a & b.
    Returns:
        d : float
            The distance between the two data points using this metric.
    See also:
        hamming
    """
    result = 2./(1./hamming(a,b,weights)+1.)
    return result

def sokalsneathsym(a,b,weights):
    """Hamming distance with dissimilarties weighted extra.
    
    Used in Sokal and Sneath (1963).  Principles of Numerical Taxonomy.
    Freeman: San Francisco.
    
    Parameters:
        a,b : ndarray
            The data points.  Expects two rank 1 arrays of the same length.
        weights : ndarray
            The weights for each dimension.  Expects rank 1 array of same 
            length as a & b.
    Returns:
        d : float
            The distance between the two data points using this metric.
    See also:
        hamming
    """
    result = 1./(2./hamming(a,b,weights)-1.)
    return result

def jaccard(a,b,weights):
    """The Jaccard distance.  Equivalent to 1 - jaccard coefficient.
    
    Developed for binary data where one state means something and the other 
    only indicates the absense of that meaning.  E.g. diagnosis of a disease.
    One state (assumed to be 1 by this algorithm) indicates the presense of the
    disease and thus a commonality between patients.  The absense of the 
    disease (a 0) however, does not necessarily indicate any commonality and
    thus shouldn't count for anything.
    Used in Jaccard (1908). Nouvelles recherches sur la distribution florale.
    Bull. Soc. Vaud. Sci. Nat., 44, 223-270
    Generalized here for nominal data with any number of meaningful states
    (non-zero) and one meaningless (0) state.
    
    Parameters:
        a,b : ndarray
            The data points.  Expects two rank 1 arrays of the same length.
        weights : ndarray
            The weights for each dimension.  Expects rank 1 array of same 
            length as a & b.
    Returns:
        d : float
            The distance between the two data points using this metric.
    """
    result = weights*(a != b)*~numpy.isnan(a)*~numpy.isnan(b)
    N = numpy.nansum(~numpy.isnan(a)*~numpy.isnan(b)*weights)-numpy.nansum((a == 0)*(b == 0)*weights)
    return numpy.nansum(result)/N
    
def dice(a,b,weights):
    """The Jaccard distance with simmilarities weighted extra.
    
    Used in Dice (1945).  Measures of the amount of ecological association
    between species.  J. Ecology, 26, 297-302.
    
    Parameters:
        a,b : ndarray
            The data points.  Expects two rank 1 arrays of the same length.
        weights : ndarray
            The weights for each dimension.  Expects rank 1 array of same 
            length as a & b.
    Returns:
        d : float
            The distance between the two data points using this metric.
    See also:
        jaccard
    """
    result = 1./(2./jaccard(a,b,weights)-1.)
    return result

def sokalsneathasym(a,b,weights):
    """The Jaccard distance with dissimmilarities weighted extra.
    
    Used in Sokal and Sneath (1963).  Principles of Numerical Taxonomy.
    Freeman: San Fancisco.
    
    Parameters:
        a,b : ndarray
            The data points.  Expects two rank 1 arrays of the same length.
        weights : ndarray
            The weights for each dimension.  Expects rank 1 array of same 
            length as a & b.
    Returns:
        d : float
            The distance between the two data points using this metric.
    See also:
        jaccard
    """
    result = 2./(1./jaccard(a,b,weights)+1.)
    return result
    
def minkowski(a,b,weights,p):
    """Calculates the Minkowski distance between two data points.
    
    Parameters:
        a,b : ndarray
            The data points.  Expects two rank 1 arrays of the same length.
        weights : ndarray
            The weights for each dimension.  Expects rank 1 array of same 
            length as a & b.
        p : integer
            The order of the Minkowski distance desired.
    Returns:
        d : float
            The Minkowski distance between the two data points.
    Notes:
        The cityblock distance (L1) the euclidian (L2) and the chebychev
        (Linf) are special cases of the minkowski distance.
    """
    result = weights*numpy.abs(a-b)**p
    N = numpy.nansum(~numpy.isnan(a)*~numpy.isnan(b)*weights)
    return (numpy.nansum(result)/N)**(1/p)

def chebychev(a,b):
    """Calculates the Chebychev distance between two data points.
    
    Parameters:
        a,b : ndarray
            The data points.  Expects two rank 1 arrays of the same length.
    Returns:
        d : float
            The chebychev distance between the two data points.
    """
    result = numpy.nanmax(a-b)
    return result
    
    
def distancesversion():
    print('cluster/distances.py')
    print('Created 6 November, 2007')
    print('by R. Padraic Springuel')
    print('Version %s modified %s' % (distancesversionnum,distancesmodified))
    print('Most recent modification by %s' % distancesmodifier)
    return
