"""Test suite designed to make sure cluster is working properly.

Note that tests only cycle through flags which are not pass through flags (i.e.
flags which are simply passed to another function call).
"""

import numpy
import cluster
import pickle
import warnings
import sys
import os

for i in sys.path:
    if 'site-packages' in i:
        dir = i + '/cluster/test/data/'
        break


def distance(verbose=0,rtol=1.0000000000000001e-005,atol=1e-008,force=False):
    """Tests to see if distances submodule is working properly.
    
    This code catches and ignores the usual UserWarnings that using weights with
    the spearman, kendall, and chebychev distances would raise.
    
    Parameters:
        verbose : int
            Controls amount of output to screen:
                0 : Only final results are printed to screen.
                1 : Tests which fail print a message to the screen.
                2 : All tests report on pass fail status to screen.
        rtol : float
            The allowable relative error between calculated values and known
            results.
        atol : float
            The allowable absolute error in levs between calculated values and 
            known results.  If (rtol*known)+atol < abs(known-calc) then test
            passes.
        force : Boolean
            Whether or not to keep testing when a test raises an exception.
    
    Returns:
        testnum : int
            Number of tests run by this function.
        testfail_ex : int
            Number of tests which failed by raising exceptions.
        testfail_pf : int (0)
            Number of simple pass/fail tests which failed (there are no tests
            like this in this function).
        testfail_tol : int
            Number of tests which failed by being outside tolerance.
        testfail_img : int (0)
            Number of image tests which failed by being too different (there are
            no tests of this type in this function).
    """
    if verbose:
        print('Testing distances submodule')
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        testnum = 0
        testfail_ex = 0
        testfail_pf = 0
        testfail_tol = 0
        testfail_img = 0
        a = numpy.load(dir + 'distance_a.pkl', allow_pickle=True)
        b = numpy.load(dir + 'distance_b.pkl', allow_pickle=True)
        c = numpy.load(dir + 'distance_c.pkl', allow_pickle=True, encoding='latin1')
        weights = numpy.load(dir + 'distance_weights.pkl', allow_pickle=True, encoding='latin1')
        with open(dir + 'distance_dist.pkl', 'rb') as f:
            dist = pickle.load(f)
        with open(dir + 'distances_no_missing.pkl', 'rb') as f:
            distances_no_missing = pickle.load(f, encoding='latin1')
        for i in dist:
            try:
                d = cluster.distances.distance(a,b,weights,i[0])
            except Exception as ex:
                if not force:
                    raise
                else:
                    testfail_ex += 1
                    if verbose:
                        print('FAIL: %s without missing data raises %s' % (i[1],type(ex).__name__))
            else:
                t = numpy.allclose(d,distances_no_missing[i[0]],rtol,atol)
                if t and verbose > 1:
                    print('PASS: %s without missing data' % i[1])
                elif not t:
                    if verbose:
                        print('FAIL: %s without missing data is outside tolerance' % i[1])
                    testfail_tol += 1
            testnum += 1
        with open(dir + 'distances_missing.pkl', 'rb') as f:
            distances_missing = pickle.load(f, encoding='latin1')
        for i in dist:
            try:
                d = cluster.distances.distance(a,c,weights,i[0])
            except Exception as ex:
                if not force:
                    raise
                else:
                    testfail_ex += 1
                    if verbose:
                        print('FAIL: %s with missing data raises %s' % (i[1],type(ex).__name__))
            else:
                t = numpy.allclose(d,distances_missing[i[0]],rtol,atol)
                if t and verbose > 1:
                    print('PASS: %s with missing data' % i[1])
                elif not t:
                    if verbose:
                        print('FAIL: %s with missing data is outside tolerance' % i[1])
                    testfail_tol += 1
            testnum += 1
    return testnum,testfail_ex,testfail_pf,testfail_tol,testfail_img


def stats(verbose=0,rtol=1.0000000000000001e-005,atol=1e-008,force=False):
    """Tests to see if stats submodule is working properly.

    There is currently no testing for the plot functions which return a picture.
    This function raises a warning about that.
    
    Parameters:
        verbose : int
            Controls amount of output to screen:
                0 : Only final results are printed to screen.
                1 : Tests which fail print a message to the screen.
                2 : All tests report on pass fail status to screen.
        rtol : float
            The allowable relative error between calculated values and known
            results.
        atol : float
            The allowable absolute error in levs between calculated values and 
            known results.  If (rtol*known)+atol < abs(known-calc) then test
            passes.
        force : Boolean
            Whether or not to keep testing when a test raises an exception.
    
    Returns:
        testnum : int
            Number of tests run by this function.
        testfail_ex : int
            Number of tests which failed by raising exceptions.
        testfail_pf : int
            Number of simple pass/fail tests which failed.
        testfail_tol : int
            Number of tests which failed by being outside tolerance.
        testfail_img : int (0)
            Number of image tests which failed by being too different (there are
            no tests of this type in this function).
    """
    testnum = 0
    testfail_ex = 0
    testfail_pf = 0
    testfail_tol = 0
    testfail_img = 0
    if verbose:
        print('Testing stats submodule')
    #distancematrix (data)
    data = numpy.load(dir + 'data.pkl', allow_pickle=True, encoding='latin1')
    with open(dir + 'distancematrix.pkl', 'rb') as f:
        distancematrix = pickle.load(f,encoding='latin1')
    try:
        dm = cluster.stats.distancematrix(data)
    except Exception as ex:
        if not force:
            raise
        else:
            testfail_ex += 1
            if verbose:
                print('FAIL: distancematrix raises %s' % type(ex).__name__)
    else:
        t = True
        for i in range(len(dm)):
            t = t and numpy.allclose(dm[i],distancematrix[i],rtol,atol)
            if not t:
                break
        if t and verbose > 1:
            print('PASS: distancematrix')
        elif not t:
            if verbose:
                print('FAIL: distancematrix is outside tolerance')
            testfail_tol += 1
    testnum += 1
    #fulldistancematrix (data)
    fulldistancematrix = numpy.load(dir + 'fulldistancematrix.pkl', allow_pickle=True, encoding='latin1')
    try:
        fdm = cluster.stats.fulldistancematrix(data)
    except Exception as ex:
        if not force:
            raise
        else:
            testfail_ex += 1
            if verbose:
                print('FAIL: fulldistancematrix raises %s' % type(ex).__name__)
    else:
        t = numpy.allclose(fdm,fulldistancematrix,rtol,atol)
        if t and verbose > 1:
            print('PASS: fulldistancematrix')
        elif not t:
            if verbose:
                print('FAIL: fulldistancematrix is outside tolerance')
            testfail_tol += 1
    testnum += 1
    #silhouette (dm, levs)
    levs = numpy.load(dir + 'levs.pkl', allow_pickle=True, encoding='latin1')
    silhouette = numpy.load(dir + 'silhouette.pkl', allow_pickle=True, encoding='latin1')
    try:
        sil = cluster.stats.silhouette(1,levs,dm=distancematrix)
    except Exception as ex:
        if not force:
            raise
        else:
            testfail_ex +=1
            if verbose:
                print('FAIL: silhouette raises %s' % type(ex).__name__)
    else:
        t = numpy.allclose(sil,silhouette,rtol,atol)
        if t and verbose > 1:
            print('PASS: silhouette')
        elif not t:
            if verbose:
                print('FAIL: silhouette is outside tolerance')
            testfail_tol += 1
    testnum += 1    
    #levscheck (levs)
    with open(dir + 'check1.pkl', 'rb') as f:
        check1 = pickle.load(f)
    try:
        c = cluster.stats.levscheck(levs)
    except Exception as ex:
        if not force:
            raise
        else:
            testfail_ex += 1
            if verbose:
                print('FAIL: levscheck on a good levs array raises %s' % type(ex).__name__)
    else:
        if check1[0] and c[0] and verbose > 1:
            print('PASS: levscheck on good levs array')
        elif not (check1[0] and c[0]):
            if verbose:
                print('FAIL: levscheck on good levs array')
            testfail_pf += 1
    testnum += 1    
    with open(dir + 'check2.pkl', 'rb') as f:
        check2 = pickle.load(f)
    levs2 = numpy.concatenate([levs,numpy.zeros((len(levs),1)),numpy.ones((len(levs),1))],axis=1)
    try:
        c = cluster.stats.levscheck(levs2)
    except Exception as ex:
        if not force:
            raise
        else:
            testfail_ex += 1
            if verbose:
                print('FAIL: levscheck on a bad levs array raises %s' % type(ex).__name__)
    else:
        t = True
        for i in range(len(check2)):
            if check2[i] != c[i]:
                t = False
                break
        if t and verbose > 1:
            print('PASS: levscheck on bad levs array')
        elif not t:
            if verbose:
                print('FAIL: levscheck on bad levs array')
            testfail_pf += 1
    testnum += 1
    #singleclustercentroid (data, lev)
    with open(dir + 'method.pkl', 'rb') as f:
        method = pickle.load(f)
    with open(dir + 'singleclustercentroid.pkl', 'rb') as f:
        singleclustercentroid = pickle.load(f, encoding='latin1')
    for i in method:
        try:
            c = cluster.stats.singleclustercentroid(data,lev=levs[:,0],method=i[0])
        except Exception as ex:
            if not force:
                raise
            else:
                testfail_ex += 1
                if verbose:
                    print('FAIL: singleclustercentroid by %s raises %s' % (i[1],type(ex).__name__))
        else:
            if i[0] == 'd':
                t = all(map(numpy.allclose,c,singleclustercentroid[i[0]],[rtol]*len(c),[atol]*len(c)))
            else:
                t = numpy.allclose(c,singleclustercentroid[i[0]],rtol,atol)
            if t and verbose > 1:
                print('PASS: singleclustercentroid by %s' % i[1])
            elif not t:
                if verbose:
                    print('FAIL: singleclustercentroid by %s is outside tolerance' % i[1])
                testfail_tol += 1
        testnum += 1
    #clustercentroids (data, levs)
    clustercentroids = numpy.load(dir + 'clustercentroids.pkl', allow_pickle=True, encoding='latin1')
    try:
        c = cluster.stats.clustercentroids(data,levs)
    except Exception as ex:
        if not force:
            raise
        else:
            testfail_ex += 1
            if verbose:
                print('FAIL: clustercentroids raises %s' % type(ex).__name__)
    else:
        t = numpy.allclose(c,clustercentroids,rtol,atol)
        if t and verbose > 1:
            print('PASS: clustercentroids')
        elif not t:
            if verbose:
                print('FAIL: clustercentroids is outside tolerance')
            testfail_tol += 1
    testnum += 1
    #SEmatrix (data, levs)
    SEmatrix = numpy.load(dir + 'SEmatrix.pkl', allow_pickle=True, encoding='latin1')
    try:
        c = cluster.stats.SEmatrix(data,levs)
    except Exception as ex:
        if not force:
            raise
        else:
            testfail_ex += 1
            if verbose:
                print('FAIL: SEmatrix raises %s' % type(ex).__name__)
    else:
        t = numpy.allclose(c,SEmatrix,rtol,atol)
        if t and verbose > 1:
            print('PASS: SEmatrix')
        elif not t:
            if verbose:
                print('FAIL: SEmatrix is outside tolerance')
            testfail_tol += 1
    testnum += 1
    with open(dir + 'SEmatrix_mode.pkl', 'rb') as f:
        SEmatrix_mode = pickle.load(f, encoding='latin1')
    with open(dir + 'SElink.pkl', 'rb') as f:
        SElink = pickle.load(f)
    SEdata = numpy.load(dir + 'SEdata.pkl', allow_pickle=True)
    for i in SElink:
        try:
            c = cluster.stats.SEmatrix(SEdata,levs,link=i[0],method='d')
        except Exception as ex:
            if not force:
                raise
            else:
                testfail_ex += 1
                if verbose:
                    print('FAIL: SEmatrix with multiple modes resolved by %s raises %s' % (i[1],type(ex).__name__))
        else:
            t = numpy.allclose(c,SEmatrix_mode[i[0]],rtol,atol)
            if t and verbose > 1:
                print('PASS: SEmatrix with multiple modes resolved by %s' % i[1])
            elif not t:
                if verbose:
                    print('FAIL: SEmatrix with multiple modes resolved by %s is outside tolerance' % i[1])
                testfail_tol += 1
        testnum += 1
    #levscompare (levs, levs2)
    try:
        check1 = cluster.stats.levscompare(levs,levs2) # should fail
        t = cluster.stats.levscompare(levs,levs[:,::-1],rtol,atol) # should pass
    except Exception as ex:
        if not force:
            raise
        else:
            testfail_ex += 1
            if verbose:
                print('FAIL: levscompare raises %s' % type(ex).__name__)
    else:
        if not check1 and t and verbose > 1:
            print('PASS: levscompare')
        elif check1 or not t:
            if verbose:
                print('FAIL: levscompare')
            testfail_pf += 1
    testnum += 1
    return testnum,testfail_ex,testfail_pf,testfail_tol,testfail_img


def hierarch(verbose=0,rtol=1.0000000000000001e-005,atol=1e-008,force=False):
    """Tests to see if hierarch submodule is working properly.
    
    Parameters:
        verbose : int
            Controls amount of output to screen:
                0 : Only final results are printed to screen.
                1 : Tests which fail print a message to the screen.
                2 : All tests report on pass fail status to screen.
        rtol : float
            The allowable relative error between calculated values and known
            results.
        atol : float
            The allowable absolute error in levs between calculated values and 
            known results.  If (rtol*known)+atol < abs(known-calc) then test
            passes.
        force : Boolean
            Whether or not to keep testing when a test raises an exception.
    
    Returns:
        testnum : int
            Number of tests run by this function.
        testfail_ex : int
            Number of tests which failed by raising exceptions.
        testfail_pf : int
            Number of simple pass/fail tests which failed.
        testfail_tol : int
            Number of tests which failed by being outside tolerance.
        testfail_img : int (0)
            Number of image tests which failed by being too different (there are
            no tests of this type in this function).
    """
    testnum = 0
    testfail_ex = 0
    testfail_pf = 0
    testfail_tol = 0
    testfail_img = 0
    if verbose:
        print('Testing hierarch submodule')
    cluster.hierarch.rtol = rtol
    cluster.hierarch.atol = atol
    #loadaggtree (filename)
    with open(dir + 'tree.pkl', 'rb') as f:
        tree = pickle.load(f)
    try:
        tr = cluster.hierarch.loadaggtree(dir + 'tr.pkl')
    except Exception as ex:
        if not force:
            raise
        else:
            testfail_ex += 1
            if verbose:
                print('FAIL: loadaggtree raises %s' % type(ex).__name__)
    else:
        t = tree == tr
        if t and verbose > 1:
            print('PASS: loadaggtree')
        elif not t:
            if verbose:
                print('FAIL: loadaggtree')
            testfail_pf += 1
    testnum += 1
    #AggTree[i] = AggNode
    with open(dir + 'node.pkl', 'rb') as f:
        node = pickle.load(f)
    try:
        t = node == tree[0]
    except Exception as ex:
        if not force:
            raise
        else:
            testfail_ex += 1
            if verbose:
                print('FAIL: Attempting to access a node of AggTree raises %s' % type(ex).__name__)
    else:
        if t and verbose > 1:
            print('PASS: Accessing node of AggTree')
        elif not t:
            if verbose:
                print('FAIL: Accessing node of AggTree')
            testfail_pf += 1
    testnum += 1
    #aggtreecluster(link,aggr,distancematrix)
    with open(dir + 'links.pkl', 'rb') as f:
        links = pickle.load(f, encoding='latin1')
    with open(dir + 'tie.pkl', 'rb') as f:
        tie = pickle.load(f)
    fulldistancematrix = numpy.load(dir + 'fulldistancematrix.pkl', allow_pickle=True, encoding='latin1')
    for i in links:
        for j in tie:
            try:
                tree = cluster.hierarch.aggtreecluster(distancematrix = fulldistancematrix,link=i[0],tie=j[0],dist='p')
            except Exception as ex:
                if not force:
                    raise
                else:
                    testfail_ex += 1
                    if verbose:
                        print('FAIL: aggtreecluster with distancematrix given, %s, and %s raises %s' % (i[1],j[1],type(ex).__name__))
            else:
                filename = 'tree_%s_%s.pkl' % (i[0],j[0])
                tr = cluster.hierarch.loadaggtree(dir + filename)
                t = tr == tree
                if t and verbose > 1:
                    print('PASS: aggtreecluster with distancematrix given, %s, and %s' % (i[1],j[1]))
                elif not t:
                    if verbose:
                        print('FAIL: aggtreecluster with distancematrix given, %s, and %s' % (i[1],j[1]))
                    testfail_pf += 1
            testnum += 1
    data = numpy.load(dir + 'data.pkl', allow_pickle=True, encoding='latin1')
    with open(dir + 'clinks.pkl', 'rb') as f:
        clinks = pickle.load(f)
    for i in clinks:
        for j in tie:
            try:
                tree = cluster.hierarch.aggtreecluster(data=data,link=i[0],tie=j[0])
            except Exception as ex:
                if not force:
                    raise
                else:
                    testfail_ex += 1
                    if verbose:
                        print('FAIL: aggtreecluster with data given, %s, and %s raises %s' % (i[1],j[1],type(ex).__name__))
            else:
                filename = 'tree_%s_%s.pkl' % (i[0],j[0])
                tr = cluster.hierarch.loadaggtree(dir + filename)
                t = tr == tree
                if t and verbose > 1:
                    print('PASS: aggtreecluster with data given, %s, and %s' % (i[1],j[1]))
                elif not t:
                    if verbose:
                        print('FAIL: aggtreecluster with data given, %s, and %s' % (i[1],j[1]))
                    testfail_pf += 1
            testnum += 1
    #AggTree.save(filename)
    filename = 'dummy.pkl'
    try:
        tree.save(dir + filename)
    except Exception as ex:
        if not force:
            raise
        else:
            testfail_ex += 1
            if verbose:
                print('FAIL: AggTree.save raises %s' % type(ex).__name__)
    else:
        tr = cluster.hierarch.loadaggtree(dir + filename)
        t = tr == tree
        if t and verbose > 1:
            print('PASS: AggTree.save')
        elif not t:
            if verbose:
                print('FAIL: AggTree.save')
            testfail_pf += 1
    testnum += 1
    os.remove(dir + filename)
    #AggTree.aliases(aliases)
    test = [(0,'test0'), (1,'test1'),(2,'test2'),(-1,'test-1'),(-2,'test-2')]
    try:
        tree.aliases(test)
    except Exception as ex:
        if not force:
            raise
        else:
            testfail_ex += 1
            if verbose:
                print('FAIL: Attempting to assign aliases to AggTree raises %s' % type(ex).__name__)
    else:
        try:
            a = tree.aliases()
        except Exception as ex:
            if not force:
                raise
            else:
                testfail_ex += 1
                if verbose:
                    print('FAIL: Attempting to extract aliases from AggTree raises %s' % type(ex).__name__)
        else:
            a.sort()
            test.sort()
            t = test == a
            if t and verbose > 1:
                print('PASS: AggTree.aliases')
            elif not t:
                if verbose:
                    print('FAIL: Assigned and extracted aliases differ')
                testfail_pf += 1
    testnum += 1
    #AggTree.ancestors(node)
    try:
        anc = tree.ancestors(0)
    except Exception as ex:
        if not force:
            raise
        else:
            testfail_ex += 1
            if verbose:
                print('FAIL: AggTree.ancestors raises %s' % type(ex).__name__)
    else:
        with open(dir + 'ancestors.pkl', 'rb') as f:
            ancestors = pickle.load(f)
        t = anc == ancestors
        if t and verbose > 1:
            print('PASS: AggTree.ancestors')
        elif not t:
            if verbose:
                print('FAIL: AggTree.ancestors')
            testfail_pf += 1
    testnum += 1
    #AggTree.decendants(node)
    try:
        dec = tree.decendants(-2)
    except Exception as ex:
        if not force:
            raise
        else:
            testfail_ex += 1
            if verbose:
                print('FAIL: AggTree.decendants raises %s' % type(ex).__name__)
    else:
        with open(dir + 'decendants.pkl', 'rb') as f:
            decendants = pickle.load(f)
        t = dec == decendants
        if t and verbose > 1:
            print('PASS: AggTree.decendants')
        elif not t:
            if verbose:
                print('FAIL: AggTree.decendants')
            testfail_pf += 1
    testnum += 1
    #AggTree.cut(nclusters)
    cut = numpy.load(dir + 'cut.pkl', allow_pickle=True, encoding='latin1')
    try:
        c = tree.cut(12)
    except Exception as ex:
        if not force:
            raise
        else:
            testfail_ex += 1
            if verbose:
                print('FAIL: AggTree.cut raises %s' % type(ex).__name__)
    t = numpy.allclose(c,cut,rtol,atol)
    if t and verbose > 1:
        print('PASS: AggTree.cut')
    elif not t:
        if verbose:
            print('FAIL: AggTree.cut is outside tolerance')
        testfail_tol += 1
    testnum += 1
    #AggTree.complete()
    bad = cluster.hierarch.AggTree([cluster.hierarch.AggNode(3,4,.5)])
    try:
        t = (not bad.complete()) and tree.complete()
    except Exception as ex:
        if not force:
            raise
        else:
            testfail_ex += 1
            if verbose:
                print('FAIL: AggTree.complete raises %s' % type(ex).__name__)
    else:
        if t and verbose > 1:
            print('PASS: AggTree.complete')
        elif not t:
            if verbose:
                print('FAIL: AggTree.complete')
            testfail_pf += 1
    testnum += 1
    #AggTree.scale()
    with open(dir + 'tree_scaled.pkl', 'rb') as f:
        tr = pickle.load(f, encoding='latin1')
    try:
        tree.scale()
    except Exception as ex:
        if not force:
            raise
        else:
            testfail_ex += 1
            if verbose:
                print('FAIL: AggTree.scale raises %s' % type(ex).__name__)
    else:
        t = tree == tr
        if t and verbose > 1:
            print('PASS: AggTree.scale')
        elif not t:
            if verbose:
                print('FAIL: AggTree.scale')
            testfail_pf += 1
    testnum += 1
    #AggTree.cophenetic()
    with open(dir + 'kind.pkl', 'rb') as f:
        kind = pickle.load(f)
    for i in kind:
        filename = 'cop_%s.pkl' % i[0]
        cop = numpy.load(dir + filename, allow_pickle=True, encoding='latin1')
        try:
            cophenetic = tree.cophenetic(i[0])
        except Exception as ex:
            if not force:
                raise
            else:
                testfail_ex += 1
                if verbose:
                    print('FAIL: AggTree.cophenetic(%s) raise %s' % (i[1],type(ex).__name__))
        else:
            t = numpy.allclose(cophenetic,cop,rtol,atol)
            if t and verbose > 1:
                print("PASS: AggTree.cophenetic('%s')" % i[1])
            elif not t:
                if verbose:
                    print("FAIL: AggTree.cophenetic('%s') is outside tolerance" % i[1])
                testfail_tol +=1
        testnum +=1
    #len(AggTree)
    try:
        t = len(tree) == len(data)-1
    except Exception as ex:
        if not force:
            raise
        else:
            testfail_ex += 1
            if verbose:
                print('FAIL: len(AggTree) raises %s' % type(ex).__name__)
    else:
        if t and verbose > 1:
            print('PASS: len(AggTree)')
        elif not t:
            if verbose:
                print('FAIL: len(AggTree)')
            testfail_pf += 1
    testnum += 1
    #str(AggTree)
    with open(dir + 'treestring.pkl', 'rb') as f:
        treestring = pickle.load(f)
    try:
        t = treestring == str(tree)
    except Exception as ex:
        if not force:
            raise
        else:
            testfail_ex += 1
            if verbose:
                print('FAIL: str(AggTree) raises %s' % type(ex).__name__)
    else:
        if t and verbose > 1:
            print('PASS: str(AggTree)')
        elif not t:
            if verbose:
                print('FAIL: str(AggTree)')
            testfail_pf += 1
    testnum += 1
    #plot.datasort(tree,heavy,weight)
    with open(dir + 'heavy.pkl', 'rb') as f:
        heavy = pickle.load(f)
    plot_weight = numpy.load(dir + 'plot_weight.pkl', allow_pickle=True, encoding='latin1')
    for i in heavy:
        filename = 'plot_datasort_%s.pkl' % i[0]
        try:
            plot_datasort = cluster.hierarch.plot.datasort(tree,i[0],plot_weight)
        except Exception as ex:
            if not force:
                raise
            else:
                testfail_ex += 1
                if verbose:
                    print('FAIL: plot.datasort when data is %s raises %s' % (i[1],type(ex).__name__))
        else:
            with open(dir + filename, 'rb') as f:
                pd = pickle.load(f)
            t = pd == plot_datasort
            if t and verbose > 1:
                print('PASS: plot.datasort when data is %s' % i[1])
            elif not t:
                if verbose:
                    print('FAIL: plot.datasort when data is %s' % i[1])
                testfail_pf += 1
        testnum += 1
    #plot.coordinates(tree,zero,distalt,sym)
    with open(dir + 'distalt.pkl', 'rb') as f:
        distalt = pickle.load(f, encoding='latin1')
    with open(dir + 'sym.pkl', 'rb') as f:
        sym = pickle.load(f)
    for i in distalt:
        for j in sym:
            try:
                coords = cluster.hierarch.plot.coordinates(tree,zero=-1,distalt=i[0], sym=j[0])
            except Exception as ex:
                if not force:
                    raise
                else:
                    testfail_ex += 1
                    if verbose:
                        print('FAIL: plot.coordinates with %s and %s raises %s' % (i[1],j[1],type(ex).__name__))
            else:
                filename = 'coords_%s_%s.pkl' % (i[1],j[0])
                with open(dir + filename, 'rb') as f:
                    coordinates = pickle.load(f, encoding='latin1')
                t = numpy.allclose(coords,coordinates,rtol,atol)
                if t and verbose > 1:
                    print('PASS: plot.coordinates with %s and %s' % (i[1],j[1]))
                elif not t:
                    if verbose:
                        print('FAIL: plot.coordinates with %s and %s is outside tolerance' % (i[1],j[1]))
                    testfail_tol += 1
            testnum += 1
    return testnum,testfail_ex,testfail_pf,testfail_tol,testfail_img


def images(verbose=0,image_hash_size=10,image_hash_diff=5,force=False):
    """Tests to see if image generation routines are working properly.

    Currently all image generation routines are in hierarch.plot submodule.
    
    Parameters:
        verbose : int
            Controls amount of output to screen:
                0 : Only final results are printed to screen.
                1 : Tests which fail print a message to the screen.
                2 : All tests report on pass fail status to screen.
        image_hash_size : int
            The size of the hash used to compare images (roughly the level of
            detail considered).
        image_hash_diff : int
            The amount of difference allowed between image hashes before the
            test image is considered to fail the test.
        force : Boolean
            Whether or not to keep testing when a test raises an exception.
    
    Returns:
        testnum : int
            Number of tests run by this function.
        testfail_ex : int
            Number of tests which failed by raising exceptions.
        testfail_pf : int (0)
            Number of simple pass/fail tests which failed (there are no
            tests like this type in this function).
        testfail_tol : int (0)
            Number of tests which failed by being outside tolerance.
        testfail_img : int
            Number of image tests which failed by being too different.
    """
    testnum = 0
    testfail_ex = 0
    testfail_pf = 0
    testfail_tol = 0
    testfail_img = 0
    if verbose:
        print("Testing image production")
    warnings.warn('plot functions which create pictures are not fully tested',UserWarning)
    #plot.treebuild(coords,tree,unmask,orient,invert,line,p,label)
    #plot.clusterlabels(coords,labels,unmask,fontdict)
    #plot.datalabels(tree,dlabels,heavy,weight,unmask,orient,fontdict)
    #plot.wholetree(tree,dlabels,heavy,weight,line,sym,p,fontdict)
    #plot.poptree(tree,heavy,weight,line,sym,p,lowerlimit,fontdict)
    #plot.fadetree(tree,heavy,weight,line,sym,p,fontdict)
    return testnum,testfail_ex,testfail_pf,testfail_tol,testfail_img


def partition(verbose=0,rtol=1.0000000000000001e-005,atol=1e-008,force=False):
    """Tests to see if partition submodule is working properly.
    
    Parameters:
        verbose : int
            Controls amount of output to screen:
                0 : Only final results are printed to screen.
                1 : Tests which fail print a message to the screen.
                2 : All tests report on pass fail status to screen.
        rtol : float
            The allowable relative error between calculated values and known
            results.
        atol : float
            The allowable absolute error in levs between calculated values and 
            known results.  If (rtol*known)+atol < abs(known-calc) then test
            passes.
        force : Boolean
            Whether or not to keep testing when a test raises an exception.
    
    Returns:
        testnum : int
            Number of tests run by this function.
        testfail_ex : int
            Number of tests which failed by raising exceptions.
        testfail_pf : int (0)
            Number of simple pass/fail tests which failed (there are no
            tests like this type in this function).
        testfail_tol : int
            Number of tests which failed by being outside tolerance.
        testfail_img : int (0)
            Number of image tests which failed by being too different (there are
            no tests of this type in this function).
    """
    testnum = 0
    testfail_ex = 0
    testfail_pf = 0
    testfail_tol = 0
    testfail_img = 0
    if verbose:
        print('Testing partition submodule')
    #kmeans(data,nclusters,initial,threshold)
    data = numpy.load(dir + 'data.pkl', allow_pickle=True, encoding='latin1')
    initial = numpy.load(dir + 'initial.pkl', allow_pickle=True, encoding='latin1')
    kmeans = numpy.load(dir + 'kmeans.pkl', allow_pickle=True, encoding='latin1')
    try:
        k = cluster.partition.kmeans(data,3,initial=initial)
    except Exception as ex:
        if not force:
            raise
        else:
            testfail_ex += 1
            if verbose:
                print('FAIL: kmeans raises %s' % type(ex).__name__)
    else:
        t = numpy.allclose(k,kmeans,rtol,atol)
        if t and verbose > 1:
            print('PASS: kmeans')
        elif not t:
            if verbose:
                print('FAIL: kmeans is outside tolerance')
            testfail_tol += 1
    testnum += 1
    #cmeans(data,nclusters,p,initial,rtol,atol)
    cmeans = numpy.load(dir + 'cmeans.pkl', allow_pickle=True, encoding='latin1')
    try:
        c = cluster.partition.cmeans(data,3,initial=initial)
    except Exception as ex:
        if not force:
            raise
        else:
            testfail_ex += 1
            if verbose:
                print('FAIL: cmeans raises %s' % type(ex).__name__)
    else:
        t = numpy.allclose(c,cmeans,rtol,atol)
        if t and verbose > 1:
            print('PASS: cmeans')
        elif not t:
            if verbose:
                print('FAIL: cmeans is outside tolerance')
            testfail_tol += 1
    testnum += 1
    #cmeans_noise(data,nclusters,p,initial,rtol,atol,l)
    cmeans_noise = numpy.load(dir + 'cmeans_noise.pkl', allow_pickle=True, encoding='latin1')
    try:
        c = cluster.partition.cmeans_noise(data,3,initial=initial)
    except Exception as ex:
        if not force:
            raise
        else:
            testfail_ex += 1
            if verbose:
                print('FAIL: cmeans_noise raises %s' % type(ex).__name__)
    else:
        t = numpy.allclose(c,cmeans_noise,rtol,atol)
        if t and verbose > 1:
            print('PASS: cmeans_noise')
        elif not t:
            if verbose:
                print('FAIL: cmeans_noise is outside tolerance')
            testfail_tol += 1
    testnum += 1
    return testnum,testfail_ex,testfail_pf,testfail_tol,testfail_img


if __name__ == '__main__':
    import cluster
    cluster.run_tests()
