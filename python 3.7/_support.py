"""Support functions.

Removes some functions

A complete version history and licence and copyright information are located
in the source code.
"""

import numpy

def weighttest(x,w):
    """Checks and formats weights.
    
    Allows the use of uncertianties using ErrorVal as the weights for the
    statistical functions.  This function also makes sure that nan values in
    the data don't have weights associated with them as that would throw off
    the calculation of the statistics when nan values are ignored.
    
    Parameters:
        x : ndarray or ArrayOfErr
            The data that the weights are supposed to correspond to.
        w : ndarray
            The weight set.  If None, we check for the use of ErrorVal first.
            If ErrorVal is used, weights are assigned as the inverse of the
            total uncertianty for each data point.  If ErrorVal is not used,
            then None defaults to equal weighting.
    Returns:
        y : ndarray
            The data set ready for the statistics functions to use.
        w : ndarray
            The weight set ready for the statistics functions to use.
    See Also:
        ErrorVal (available at http://users.bigpond.net.au/gazzar/python.html)
    """
    if w is None:
        try:
            from ErrorVal import NegErrs,PosErrs,PrimeVals
            w = 1/(NegErrs(x)+PosErrs(x))
            y = PrimeVals(x)
        except (ImportError, AttributeError):
            w = numpy.ones_like(x)
            y = x
    else:
        try:
            from ErrorVal import PrimeVals
            y = PrimeVals(x)
        except (ImportError, AttributeError):
            y = x
    w = w*~numpy.isnan(y) #makes sure that nan data points don't have a weight
    return numpy.array(y),w

def absmean(x,w=None,axis=None,NN=True):
    """Computes the algebraic mean of the absolute values of the input array.
    
    Parameters:
        x : ndarray or ArrayOfErr
            The data which will be averaged.
        w : ndarray
            Optional.  The weights corresponding to each data point.  Must be
            same shape as x or broadcastable to that shape.
        axis : integer
            The axis over which the absolute mean is to be taken.  If none is
            given then the absolute mean will be taken over the entire array.
        NN : boolean
            If True (default) nan values in x will not be ignored and so nan
            will be returned if they are present.  If False, then nan values
            will be ignored in x and weights of nan will be treated as a weight
            of 0.
    Returns:
        result : float or ndarray
            The algebraic mean of the absolute values of x.  If axis is None
            then a single float is returned.  Otherwise a ndarray containing
            the algebraic means evaluated along the axis is returned.
    """
    x,w = weighttest(x,w)
    if NN:
        result = 1.*numpy.sum(numpy.abs(x*w),axis=axis)/numpy.sum(w,axis=axis)
    else:
        result = 1.*numpy.nansum(numpy.abs(x*w),axis=axis)/numpy.nansum(w,axis=axis)
    return result

def geomean(x,w=None,axis=None,NN=True):
    """Computes the geometric mean of the input array.
    
    Parameters:
        x : ndarray or ArrayOfErr
            The data which will be averaged.
        w : ndarray
            Optional.  The weights corresponding to each data point.  Must be
            same shape as x or broadcastable to that shape.
        axis : integer
            The axis over which the geometric mean is to be taken.  If none is
            given then the geometric mean will be taken over the entire array.
        NN : boolean
            If True (default) nan values in x will not be ignored and so nan
            will be returned if they are present.  If False, then nan values
            will be ignored in x and weights of nan will be treated as a weight
            of 0.
    Returns:
        result : float or ndarray
            The geometric mean of x.  If axis is None then a single float is
            returned.  Otherwise a ndarray containing the geometric means 
            evaluated along the axis is returned.
    """
    x,w = weighttest(x,w)
    if NN:
        result = numpy.product(x**w,axis=axis)**(1./numpy.sum(w,axis=axis))
    else:
        are_nan = numpy.isnan(x)
        x[are_nan] = 1
        result = numpy.product(x**w,axis=axis)**(1./numpy.nansum(w,axis=axis))
    return result

def harmean(x,w=None,axis=None,NN=True):
    """Computes the harmonic mean of the input array.
    
    Parameters:
        x : ndarray or ArrayOfErr
            The data which will be averaged.
        w : ndarray
            Optional.  The weights corresponding to each data point.  Must be
            same shape as x or broadcastable to that shape.
        axis : integer
            The axis over which the harmonic mean is to be taken.  If none is
            given then the harmonic mean will be taken over the entire array.
        NN : boolean
            If True (default) nan values in x will not be ignored and so nan
            will be returned if they are present.  If False, then nan values
            will be ignored in x and weights of nan will be treated as a weight
            of 0.
    Returns:
        result : float or ndarray
            The harmonic mean of x.  If axis is None then a single float is 
            returned.  Otherwise a ndarray containing the harmonic means 
            evaluated along the axis is returned.
    """
    x,w = weighttest(x,w)
    if numpy.any(x == 0):
        return numpy.nan
    if NN:
        result = 1.*numpy.sum(w,axis=axis)/numpy.sum(w/x,axis=axis)
    else:
        result = 1.*numpy.nansum(w,axis=axis)/numpy.nansum(w/x,axis=axis)
    return result

def quadmean(x,w=None,axis=None,NN=True):
    """Computes the quadratic mean of the input array.
        
    Parameters:
        x : ndarray or ArrayOfErr
            The data which will be averaged.
        w : ndarray
            Optional.  The weights corresponding to each data point.  Must be
            same shape as x or broadcastable to that shape.
        axis : integer
            The axis over which the quadratic mean is to be taken.  If none is
            given then the quadratic mean will be taken over the entire array.
        NN : boolean
            If True (default) nan values in x will not be ignored and so nan
            will be returned if they are present.  If False, then nan values
            will be ignored in x and weights of nan will be treated as a weight
            of 0.
    Returns:
        result : float or ndarray
            The quadratic mean of x.  If axis is None then a single float is 
            returned.  Otherwise a ndarray containing the quadratic means 
            evaluated along the axis is returned.
    """
    x,w = weighttest(x,w)
    if NN:
        result = numpy.sqrt(1.*numpy.sum(w*x**2,axis=axis)/numpy.sum(w,axis=axis))
    else:
        result = numpy.sqrt(1.*numpy.nansum(w*x**2,axis=axis)/numpy.nansum(w,axis=axis))
    return result

def mean(x,w=None,axis=None,NN=True):
    """Computes the mean.
            
    Parameters:
        x : ndarray or ArrayOfErr
            The data which will be averaged.
        w : ndarray
            Optional.  The weights corresponding to each data point.  Must be
            same shape as x or broadcastable to that shape.
        axis : integer
            The axis over which the mean is to be taken.  If none is given then
            the mean will be taken over the entire array.
        NN : boolean
            If True (default) nan values in x will not be ignored and so nan
            will be returned if they are present.  If False, then nan values
            will be ignored in x and weights of nan will be treated as a weight
            of 0.
    Returns:
        result : float or ndarray
            The mean of x.  If axis is None then a single float is returned.
            Otherwise a ndarray containing the means evaluated along the axis
            is returned.
    """
    x,w = weighttest(x,w)
    if NN:
        result = 1.*numpy.sum(x*w,axis=axis)/numpy.sum(w,axis=axis)
    else:
        result = 1.*numpy.nansum(x*w,axis=axis)/numpy.nansum(w,axis=axis)
    return result

def median(x,w=None,axis=None,NN=True):
    """Calculates the median (middle value).
    
    Interface level function that provides axis control.  See source of
    median_work for actual computation of the median.
    
    Parameters:
        x : ndarray or ArrayOfErr
            The data which will be averaged.
        w : ndarray
            Optional.  The weights corresponding to each data point.  Must be
            same shape as x or broadcastable to that shape.
        axis : integer
            The axis over which the median is to be taken.  If none is given
            then the median will be taken over the entire array.
        NN : boolean
            If True (default) nan values in x and w will not be ignored and so 
            nan will be returned if they are present.  If False, then nan 
            values will be ignored in x and weights of nan will be treated as a
            weight of 0.
    
    Returns:
        result : float or ndarray
            The median of x.  If axis is None then a single float is returned.
            Otherwise a ndarray containing the medians evaluated along the axis
            is returned.
    """
    x,w = weighttest(x,w)
    mytype = [('data',x.dtype),('weight',w.dtype)]
    d = numpy.zeros(numpy.shape(x),dtype=mytype)
    d['data'] = x
    d['weight'] = w
    if axis is None:
        result = median_work(d,NN)
    else:
        result = numpy.apply_along_axis(median_work,axis,d,NN)
    return result

def median_work(d,NN=True):
    """Calculates the median (middle value).
    
    Parameters:
        d : ndarray
            The data and weight corresponding to each data point in a single 
            rank 1 array.
        NN : boolean
            If True (default) nan values in x and w will not be ignored and so 
            nan will be returned if they are present.  If False, then nan 
            values will be ignored in x and weights of nan will be treated as a
            weight of 0.
    Returns:
        result : float
            The median of the data in d.
    """
    x,w = d['data'],d['weight']
    if (numpy.any(numpy.isnan(x)) or numpy.any(numpy.isnan(w))) and NN:
        return numpy.nan
    t = numpy.nansum(w)/2.
    xrankable = []
    missing = numpy.isnan(x)
    for i in range(len(x.flat)):
        if not missing.flat[i] and w.flat[i] != 0:
            xrankable.append([x.flat[i],w.flat[i]])
    xrankable.sort()
    if len(xrankable) == 0:
        result = numpy.nan
    elif len(xrankable) == 1:
        result = float(xrankable[0][0])
    else:
        cumw = numpy.cumsum(numpy.array(xrankable)[:,1])
        for i in range(len(cumw)):
            if cumw[i-1] < t < cumw[i]:
                result = float(xrankable[i][0])
                break
            elif cumw[i] == t:
                result = (xrankable[i][0]+xrankable[i+1][0])/2.
                break
    return result

def nanunique(x):
    """Finds the unique values of x with proper handling of nan values.
    
    numpy.unique returns a NaN entry for every entry that was NaN in the 
    original array.  This function removes the redundant NaN entries.
    
    Parameters:
        x : ndarray
            The array whose unique values are desired.
    Return:
        r : ndarray
            The unique values of x.
    """
    a = numpy.unique(x)
    r = []
    for i in a:
        if i in r or (numpy.isnan(i) and numpy.any(numpy.isnan(r))):
            continue
        else:
            r.append(i)
    return numpy.array(r)

def mode(x,w=None,axis=None,NN=True):
    """Finds all modes (most frequent values) of an input array.
    
    Because the mode is well defined even when some data is nan, this function
    does not use weighttest (which would set the weights of nan to 0) but
    instead does its own testing of the weights.
    
    Parameters:
        x : ndarray or ArrayOfErr
            The data which will be averaged.
        w : ndarray
            Optional.  The weights corresponding to each data point.  Must be
            same shape as x or broadcastable to that shape.
        axis : integer
            The axis over which the mode is to be taken.  If none is given
            then the mode will be taken over the entire array.
        NN : boolean
            If True (default) nan values in w will not be ignored and so nan
            will be returned if they are present in w.  If False, then weights
            of nan will be treated as a weight of 0.
    Returns:
        result : ndarray
            The modes of x along the axis.  If axis is None, then the array
            dtype is the same as x and the modes are for the entire array taken
            as a flat array.  For any other value of axis, the array dtype is
            object in order to handle the possibility of differing numbers of
            modes in different subsets of x over axis.
    """
    if w is None:
        try:
            from ErrorVal import NegErrs,PosErrs,PrimeVals
            w = 1/(NegErrs(x)+PosErrs(x))
            x = PrimeVals(x)
        except (ImportError, AttributeError):
            w = numpy.ones_like(x)
    else:
        try:
            from ErrorVal import PrimeVals
            x = PrimeVals(x)
        except (ImportError, AttributeError):
            pass
        if numpy.shape(x) != numpy.shape(w):
            w = numpy.zeros_like(x) + w
    if not NN:
        w = numpy.nan_to_num(w)
    if axis is None:
        uniques,counts = discretehistogram(x,w)
        m = uniques[counts == numpy.max(counts)]
    else:
        n = list(numpy.shape(x))
        del n[axis]
        N = numpy.prod(n)
        m = numpy.zeros(n,dtype=object)
        index = numpy.array([numpy.zeros_like(n)]*N)
        for i in range(1,N):
            index[i] = index[i-1]
            index[i][0] += 1
            for j in range(len(index[i])-1):
                if index[i][j] == n[j]:
                    index[i][j] = 0
                    index[i][j+1] += 1
        index = index.tolist()
        for k in index:
            k.insert(axis,':')
            str = 'x%s' % k
            str = str.replace("'",'')
            xtake = eval(str)
            str = 'w%s' % k
            str = str.replace("'",'')
            wtake = eval(str)
            uniques,counts = discretehistogram(xtake,wtake)
            t = uniques[counts == numpy.max(counts)]
            k.remove(':')
            m[tuple(k)] = numpy.array(t)
    return m

def discretehistogram(x,w=None):
    """Calculates the histogram for x assuming that the data in x is discrete.
    
    Numpy's histogram function assumes the data in x is continuous and thus it
    is necessary to define the number and/or range of the bins.  This function,
    on the other hand, assumes that the data in x is discrete and thus a true
    histogram of the data in x is a count of the occurances of each unique
    value in x.  This enables it to handle nan data in a way that
    numpy.historgram cannot and so nanunique is used rather than unique.
    
    As in numpy's histogram function, multi-dimensional arrays are flattened.
    Normalization routines are not implemented.
    
    Parameters:
        x : ndarray or ArrayOfErr
            The data set.
        w : ndarray
            Optional.  The weights corresponding to each data point.  Must be
            same shape as x or broadcastable to that shape.
    Returns:
        uniques : ndarray
            The unique values of x.
        counts : ndarray
            The frequency counts of the elements of uniques in x.  counts[i]
            is the count of uniques[i].
    """
    if w is None:
        try:
            from ErrorVal import NegErrs,PosErrs,PrimeVals
            w = 1/(NegErrs(x)+PosErrs(x))
            x = PrimeVals(x)
        except (ImportError, AttributeError):
            w = numpy.ones_like(x)
    else:
        try:
            from ErrorVal import PrimeVals
            x = PrimeVals(x)
        except (ImportError, AttributeError):
            pass
        if numpy.shape(x) != numpy.shape(w):
            w = numpy.zeros_like(x) + w
    uniques = nanunique(x)
    counts = numpy.zeros_like(uniques).astype(float)
    for i in range(len(uniques)):
        if numpy.isnan(uniques[i]):
            counts[i] = numpy.sum(numpy.isnan(x)*w)
        else:
            counts[i] = numpy.sum((x == uniques[i])*w)
    return uniques,counts
