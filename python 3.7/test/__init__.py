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

def distance(verbose=0,rtol=1.0000000000000001e-005,atol=1e-008):
    """Tests to see if distance is working properly.
    
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
    
    Returns:
        testnum : int
            Number of tests run by this function.
        testfail : int
            Number of tests which failed.
    """
    print('Testing distances module')
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        testnum = 0
        testfail = 0
        a = numpy.load(dir + 'distance_a.pkl', allow_pickle=True)
        b = numpy.load(dir + 'distance_b.pkl', allow_pickle=True)
        c = numpy.load(dir + 'distance_c.pkl', allow_pickle=True, encoding='latin1')
        weights = numpy.load(dir + 'distance_weights.pkl', allow_pickle=True, encoding='latin1')
        f = open(dir + 'distance_dist.pkl', 'rb')
        dist = pickle.load(f)
        f = open(dir + 'distances_no_missing.pkl', 'rb')
        distances_no_missing = pickle.load(f, encoding='latin1')
        for i in dist:
            d = cluster.distances.distance(a,b,weights,i[0])
            t = numpy.allclose(d,distances_no_missing[i[0]],rtol,atol)
            if t and verbose > 1:
                print('%s distance passes without missing data' % i[1])
            elif not t:
                if verbose:
                    print('%s distance fails without missing data' % i[1])
                testfail += 1
            testnum += 1
        f = open(dir + 'distances_missing.pkl', 'rb')
        distances_missing = pickle.load(f, encoding='latin1')
        for i in dist:
            d = cluster.distances.distance(a,c,weights,i[0])
            t = numpy.allclose(d,distances_missing[i[0]],rtol,atol)
            if t and verbose > 1:
                print('%s distance passes with missing data' % i[1])
            elif not t:
                if verbose:
                    print('%s distance fails with missing data' % i[1])
                testfail += 1
            testnum += 1
    return testnum,testfail

def stats(verbose=0,rtol=1.0000000000000001e-005,atol=1e-008):
    testnum = 0
    testfail = 0
    print('Testing stats module')
    #distancematrix (data)
    data = numpy.load(dir + 'data.pkl', allow_pickle=True, encoding='latin1')
    f = open(dir + 'distancematrix.pkl', 'rb')
    distancematrix = pickle.load(f,encoding='latin1')
    dm = cluster.stats.distancematrix(data)
    t = True
    for i in range(len(dm)):
        t = t and numpy.allclose(dm[i],distancematrix[i],rtol,atol)
        if not t:
            break
    if t and verbose > 1:
        print('distancematrix passes')
    elif not t:
        if verbose:
            print('distancematrix fails')
        testfail += 1
    testnum += 1
    #fulldistancematrix (data)
    fulldistancematrix = numpy.load(dir + 'fulldistancematrix.pkl', allow_pickle=True, encoding='latin1')
    fdm = cluster.stats.fulldistancematrix(data)
    t = numpy.allclose(fdm,fulldistancematrix,rtol,atol)
    if t and verbose > 1:
        print('fulldistancematrix passes')
    elif not t:
        if verbose:
            print('fulldistancematrix fails')
        testfail += 1
    testnum += 1
    #silhouette (dm, levs)
    levs = numpy.load(dir + 'levs.pkl', allow_pickle=True, encoding='latin1')
    silhouette = numpy.load(dir + 'silhouette.pkl', allow_pickle=True, encoding='latin1')
    sil = cluster.stats.silhouette(1,levs,dm=distancematrix)
    t = numpy.allclose(sil,silhouette,rtol,atol)
    if t and verbose > 1:
        print('silhouette passes')
    elif not t:
        if verbose:
            print('silhouette fails')
        testfail += 1
    testnum += 1    
    #levscheck (levs)
    f = open(dir + 'check1.pkl', 'rb')
    check1 = pickle.load(f)
    c = cluster.stats.levscheck(levs)
    if check1[0] and c[0] and verbose > 1:
        print('levscheck passes on good levs array')
    elif not (check1[0] and c[0]):
        if verbose:
            print('levscheck fails on good levs array')
        testfail += 1
    testnum += 1    
    f = open(dir + 'check2.pkl', 'rb')
    check2 = pickle.load(f)
    levs2 = numpy.concatenate([levs,numpy.zeros((len(levs),1)),numpy.ones((len(levs),1))],axis=1)
    c = cluster.stats.levscheck(levs2)
    t = True
    for i in range(len(check2)):
        if check2[i] != c[i]:
            t = False
            break
    if t and verbose > 1:
        print('levscheck passes on bad levs array')
    elif not t:
        if verbose:
            print('levscheck fails on bad levs array')
        testfail += 1
    testnum += 1
    #singleclustercentroid (data, lev)
    f = open(dir + 'method.pkl', 'rb')
    method = pickle.load(f)
    f = open(dir + 'singleclustercentroid.pkl', 'rb')
    singleclustercentroid = pickle.load(f, encoding='latin1')
    for i in method:
        c = cluster.stats.singleclustercentroid(data,lev=levs[:,0],method=i[0])
        if i[0] == 'd':
            t = all(map(numpy.allclose,c,singleclustercentroid[i[0]],[rtol]*len(c),[atol]*len(c)))
        else:
            t = numpy.allclose(c,singleclustercentroid[i[0]],rtol,atol)
        if t and verbose > 1:
            print('singleclustercentroid passes for %s' % i[1])
        elif not t:
            if verbose:
                print('singleclustercentroid fails for %s' % i[1])
            testfail += 1
        testnum += 1
    #clustercentroids (data, levs)
    clustercentroids = numpy.load(dir + 'clustercentroids.pkl', allow_pickle=True, encoding='latin1')
    c = cluster.stats.clustercentroids(data,levs)
    t = numpy.allclose(c,clustercentroids,rtol,atol)
    if t and verbose > 1:
        print('clustercentroids passes')
    elif not t:
        if verbose:
            print('clustercentroids fails')
        testfail += 1
    testnum += 1
    #SEmatrix (data, levs)
    SEmatrix = numpy.load(dir + 'SEmatrix.pkl', allow_pickle=True, encoding='latin1')
    c = cluster.stats.SEmatrix(data,levs)
    t = numpy.allclose(c,SEmatrix,rtol,atol)
    if t and verbose > 1:
        print('SEmatrix passes')
    elif not t:
        if verbose:
            print('SEmatrix fails')
        testfail += 1
    testnum += 1
    f = open(dir + 'SEmatrix_mode.pkl', 'rb')
    SEmatrix_mode = pickle.load(f, encoding='latin1')
    f = open(dir + 'SElink.pkl', 'rb')
    SElink = pickle.load(f)
    SEdata = numpy.load(dir + 'SEdata.pkl', allow_pickle=True)
    for i in SElink:
        c = cluster.stats.SEmatrix(SEdata,levs,link=i[0],method='d')
        t = numpy.allclose(c,SEmatrix_mode[i[0]],rtol,atol)
        if t and verbose > 1:
            print('SEmatrix passes with multiple modes resolved by %s' % i[1])
        elif not t:
            if verbose:
                print('SEmatrix fails with multiple modes resolved by %s' % i[1])
            testfail += 1
        testnum += 1
    #levscompare (levs1, levs2)
    check1 = cluster.stats.levscompare(levs,levs2)
    if not check1:
        t = cluster.stats.levscompare(levs,levs[:,::-1],rtol,atol)
        if t and verbose > 1:
            print('levscompare passes')
        elif not t:
            if verbose:
                print('levscompare fails')
            testfail += 1
        testnum += 1
    return testnum,testfail

def hierarch(verbose=0,rtol=1.0000000000000001e-005,atol=1e-008):
    testnum = 0
    testfail = 0
    print('Testing hierarch module')
    cluster.hierarch.rtol = rtol
    cluster.hierarch.atol = atol
    #loadaggtree (filename)
    f = open(dir + 'tree.pkl', 'rb')
    tree = pickle.load(f)
    tr = cluster.hierarch.loadaggtree(dir + 'tr.pkl')
    t = tree == tr
    if t and verbose > 1:
        print('loadaggtree passes')
    elif not t:
        if verbose:
            print('loadaggtree fails')
        testfail += 1
    testnum += 1
    #AggTree[i] = AggNode
    f = open(dir + 'node.pkl', 'rb')
    node = pickle.load(f)
    t = node == tree[0]
    if t and verbose > 1:
        print('AggTree[i] passes')
    elif not t:
        if verbose:
            print('AggTree[i] fails')
        testfail += 1
    testnum += 1
    #aggtreecluster(link,aggr,distancematrix)
    f = open(dir + 'links.pkl', 'rb')
    links = pickle.load(f, encoding='latin1')
    f = open(dir + 'tie.pkl', 'rb')
    tie = pickle.load(f)
    fulldistancematrix = numpy.load(dir + 'fulldistancematrix.pkl', allow_pickle=True, encoding='latin1')
    for i in links:
        for j in tie:
            tree = cluster.hierarch.aggtreecluster(distancematrix = fulldistancematrix,link=i[0],tie=j[0],dist='p')
            filename = 'tree_%s_%s.pkl' % (i[0],j[0])
            tr = cluster.hierarch.loadaggtree(dir + filename)
            t = tr == tree
            if t and verbose > 1:
                print('aggtreecluster passes with %s and %s' % (i[1],j[1]))
            elif not t:
                if verbose:
                    print('aggtreecluster fails with %s and %s' % (i[1],j[1]))
                testfail += 1
            testnum += 1
    data = numpy.load(dir + 'data.pkl', allow_pickle=True, encoding='latin1')
    f = open(dir + 'clinks.pkl', 'rb')
    clinks = pickle.load(f)
    for i in clinks:
        for j in tie:
            tree = cluster.hierarch.aggtreecluster(data=data,link=i[0],tie=j[0])
            filename = 'tree_%s_%s.pkl' % (i[0],j[0])
            tr = cluster.hierarch.loadaggtree(dir + filename)
            t = tr == tree
            if t and verbose > 1:
                print('aggtreecluster passes with %s and %s' % (i[1],j[1]))
            elif not t:
                if verbose:
                    print('aggtreecluster fails with %s and %s' % (i[1],j[1]))
                testfail += 1
            testnum += 1
    #AggTree.save(filename)
    filename = 'dummy.pkl'
    tree.save(dir + filename)
    tr = cluster.hierarch.loadaggtree(dir + filename)
    t = tr == tree
    if t and verbose > 1:
        print('AggTree.save passes')
    elif not t:
        if verbose:
            print('AggTree.save fails')
        testfail += 1
    testnum += 1
    os.remove(dir + filename)
    #AggTree.aliases(aliases)
    test = [(0,'test0'), (1,'test1'),(2,'test2'),(-1,'test-1'),(-2,'test-2')]
    tree.aliases(test)
    a = tree.aliases()
    a.sort()
    test.sort()
    t = test == a
    if t and verbose > 1:
        print('AggTree.aliases passes')
    elif not t:
        if verbose:
            print('AggTree.aliases fails')
        testfail += 1
    testnum += 1
    #AggTree.ancestors(node)
    anc = tree.ancestors(0)
    f = open(dir + 'ancestors.pkl', 'rb')
    ancestors = pickle.load(f)
    t = anc == ancestors
    if t and verbose > 1:
        print('AggTree.ancestors passes')
    elif not t:
        if verbose:
            print('AggTree.ancestors fails')
        testfail += 1
    testnum += 1
    #AggTree.decendants(node)
    dec = tree.decendants(-2)
    f = open(dir + 'decendants.pkl', 'rb')
    decendants = pickle.load(f)
    t = dec == decendants
    if t and verbose > 1:
        print('AggTree.decendants passes')
    elif not t:
        if verbose:
            print('AggTree.decendants fails')
        testfail += 1
    testnum += 1
    #AggTree.cut(nclusters)
    cut = numpy.load(dir + 'cut.pkl', allow_pickle=True, encoding='latin1')
    c = tree.cut(12)
    t = numpy.allclose(c,cut,rtol,atol)
    if t and verbose > 1:
        print('AggTree.cut passes')
    elif not t:
        if verbose:
            print('AggTree.cut fails')
        testfail += 1
    testnum += 1
    #AggTree.complete()
    bad = cluster.hierarch.AggTree([cluster.hierarch.AggNode(3,4,.5)])
    t = (not bad.complete()) and tree.complete()
    if t and verbose > 1:
        print('AggTree.complete passes')
    elif not t:
        if verbose:
            print('AggTree.complete fails')
        testfail += 1
    testnum += 1
    #AggTree.scale()
    f = open(dir + 'tree_scaled.pkl', 'rb')
    tr = pickle.load(f, encoding='latin1')
    tree.scale()
    t = tree == tr
    if t and verbose > 1:
        print('AggTree.scale passes')
    elif not t:
        if verbose:
            print('AggTree.scale fails')
        testfail += 1
    testnum += 1
    #AggTree.cophenetic()
    f = open(dir + 'kind.pkl', 'rb')
    kind = pickle.load(f)
    for i in kind:
        filename = 'cop_%s.pkl' % i[0]
        cop = numpy.load(dir + filename, allow_pickle=True, encoding='latin1')
        cophenetic = tree.cophenetic(i[0])
        t = numpy.allclose(cophenetic,cop,rtol,atol)
        if t and verbose > 1:
            print("AggTree.cophenetic('%s') passes" % i[1])
        elif not t:
            if verbose:
                print("AggTree.cophenetic('%s') fails" % i[1])
            testfail +=1
        testnum +=1
    #len(AggTree)
    t = len(tree) == len(data)-1
    if t and verbose > 1:
        print('len(AggTree) passes')
    elif not t:
        if verbose:
            print('len(AggTree) fails')
        testfail += 1
    testnum += 1
    #str(AggTree)
    f = open(dir + 'treestring.pkl', 'rb')
    treestring = pickle.load(f)
    t = treestring == str(tree)
    if t and verbose > 1:
        print('str(AggTree) passes')
    elif not t:
        if verbose:
            print('str(AggTree) fails')
        testfail += 1
    testnum += 1
    #plot.datasort(tree,heavy,weight)
    f = open(dir + 'heavy.pkl', 'rb')
    heavy = pickle.load(f)
    plot_weight = numpy.load(dir + 'plot_weight.pkl', allow_pickle=True, encoding='latin1')
    for i in heavy:
        filename = 'plot_datasort_%s.pkl' % i[0]
        plot_datasort = cluster.hierarch.plot.datasort(tree,i[0],plot_weight)
        f = open(dir + filename, 'rb')
        pd = pickle.load(f)
        t = pd == plot_datasort
        if t and verbose > 1:
            print('plot.datasort passes when data is %s' % i[1])
        elif not t:
            if verbose:
                print('plot.datasort fails when data is %s' % i[1])
            testfail += 1
        testnum += 1
    #plot.coordinates(tree,zero,distalt,sym)
    f = open(dir + 'distalt.pkl', 'rb')
    distalt = pickle.load(f, encoding='latin1')
    f = open(dir + 'sym.pkl', 'rb')
    sym = pickle.load(f)
    for i in distalt:
        for j in sym:
            filename = 'coords_%s_%s.pkl' % (i[1],j[0])
            f = open(dir + filename, 'rb')
            coords = cluster.hierarch.plot.coordinates(tree,zero=-1,distalt=i[0], sym=j[0])
            coordinates = pickle.load(f, encoding='latin1')
            t = numpy.allclose(coords,coordinates,rtol,atol)
            if t and verbose > 1:
                print('plot.coordinates passes with %s and %s' % (i[1],j[1]))
            elif not t:
                if verbose:
                    print('plot.coordinates fails with %s and %s' % (i[1],j[1]))
                testfail += 1
            testnum += 1
    #PICTURE RETURNS
    warnings.warn('plot functions which create pictures are not currently tested',UserWarning)
    #plot.treebuild(coords,tree,unmask,orient,invert,line,p,label)
    #plot.clusterlabels(coords,labels,unmask,fontdict)
    #plot.datalabels(tree,dlabels,heavy,weight,unmask,orient,fontdict)
    #plot.wholetree(tree,dlabels,heavy,weight,line,sym,p,fontdict)
    #plot.poptree(tree,heavy,weight,line,sym,p,lowerlimit,fontdict)
    #plot.fadetree(tree,heavy,weight,line,sym,p,fontdict)
    return testnum,testfail

def partition(verbose=0,rtol=1.0000000000000001e-005,atol=1e-008):
    testnum = 0
    testfail = 0
    print('Testing partition module')
    #kmeans(data,nclusters,initial,threshold)
    data = numpy.load(dir + 'data.pkl', allow_pickle=True, encoding='latin1')
    initial = numpy.load(dir + 'initial.pkl', allow_pickle=True, encoding='latin1')
    kmeans = numpy.load(dir + 'kmeans.pkl', allow_pickle=True, encoding='latin1')
    k = cluster.partition.kmeans(data,3,initial=initial)
    t = numpy.allclose(k,kmeans,rtol,atol)
    if t and verbose > 1:
        print('kmeans passes')
    elif not t:
        if verbose:
            print('kmeans fails')
        testfail += 1
    testnum += 1
    #cmeans(data,nclusters,p,initial,rtol,atol)
    cmeans = numpy.load(dir + 'cmeans.pkl', allow_pickle=True, encoding='latin1')
    c = cluster.partition.cmeans(data,3,initial=initial)
    t = numpy.allclose(c,cmeans,rtol,atol)
    if t and verbose > 1:
        print('cmeans passes')
    elif not t:
        if verbose:
            print('cmeans fails')
        testfail += 1
    testnum += 1
    #cmeans_noise(data,nclusters,p,initial,rtol,atol,l)
    cmeans_noise = numpy.load(dir + 'cmeans_noise.pkl', allow_pickle=True, encoding='latin1')
    c = cluster.partition.cmeans_noise(data,3,initial=initial)
    t = numpy.allclose(c,cmeans_noise,rtol,atol)
    if t and verbose > 1:
        print('cmeans_noise passes')
    elif not t:
        if verbose:
            print('cmeans_noise fails')
        testfail += 1
    testnum += 1
    return testnum,testfail

def legacy(verbose=0,rtol=1.0000000000000001e-005,atol=1e-008):
    """Tests to see if legacy functions are working properly.
    
    Legacy functions were written while cluster was being used along side
    PyCluster.  Since cluster can now do everything that PyCluster can do and
    more, this should no longer be the case.  If you still need these functions
    (perhaps to check that a conversion is producing equivalent results), this
    function will test to make sure that they are working properly.  This code
    supresses the normal DeprecationWarning's that legacy functions would issue.
    
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
    
    Returns:
        testnum : int
            Number of tests run by this function.
        testfail : int
            Number of tests which failed.
    """
    print('Testing legacy functions')
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        testnum = 0
        testfail = 0
        dm = numpy.load(dir + 'legacy_dm.pkl', allow_pickle=True)
        clusterid = numpy.load(dir + 'legacy_clusterid.pkl', allow_pickle=True)
        old_silhouette = numpy.load(dir + 'legacy_silhouette.pkl', allow_pickle=True)
        sil = cluster.stats.old_silhouette(1,clusterid,dm)
        t = numpy.allclose(sil,old_silhouette,rtol,atol)
        if t and verbose > 1:
            print('old_silhouette passes')
        elif not t:
            if verbose:
                print('old_silhouette fails')
            testfail += 1
        testnum += 1
        f = open(dir + 'legacy_members.pkl', 'rb')
        members = pickle.load(f)
        mems = cluster.stats.members(clusterid)
        t = mems == members
        if t and verbose > 1:
            print('members passes')
        elif not t:
            if verbose:
                print('members fails')
            testfail += 1
        testnum += 1
        levs = numpy.load(dir + 'legacy_levs.pkl', allow_pickle=True)
        l = cluster.stats.clusterid_to_levs(clusterid)
        t = numpy.allclose(l,levs,rtol,atol)
        if t and verbose > 1:
            print('clusterid_to_levs passes')
        elif not t:
            if verbose:
                print('clusterid_to_levs fails')
            testfail += 1
        testnum += 1
        c = cluster.stats.levs_to_clusterid(l)
        t = numpy.allclose(c,clusterid,rtol,atol)
        if t and verbose > 1:
            print('levs_to_clusterid passes')
        elif not t:
            if verbose:
                print('levs_to_clusterid fails')
            testfail += 1
        testnum += 1
        method = pickle.load(dir + 'legacy_method.pkl')
        transpose = pickle.load(dir + 'legacy_transpose.pkl')
        data = numpy.load(dir + 'data.pkl', allow_pickle=True)
        old_singleclustercentroids = numpy.load(dir + 'legacy_singleclustercentroids.pkl', allow_pickle=True)
        n = 0
        for i in method:
            for j in transpose:
                if j[0]:
                    d = cluster.stats.old_singleclustercentroid(numpy.transpose(data),members[0],i[0],j[0])
                else:
                    d = cluster.stats.old_singleclustercentroid(data,members[0],i[0],j[0])
                t = numpy.allclose(d,old_singleclustercentroids[n],rtol,atol)
                if t and verbose > 1:
                    print('old_singleclustercentroid passes on %s centroid for %s' % (i[1],j[1]))
                elif not t:
                    if verbose:
                        print('old_singleclustercentroid fails on %s centroid for %s' % (i[1],j[1]))
                    testfail += 1
                testnum += 1
                n += 1
        old_clustercentroids = numpy.load(dir + 'legacy_clustercentroids.pkl', allow_pickle=True)
        d = cluster.stats.old_clustercentroids(data,members)
        t = numpy.allclose(d,old_clustercentroids,rtol,atol)
        if t and verbose > 1:
            print('old_clustercentroids passes')
        elif not t:
            if verbose:
                print('old_clustercentroids fails')
            testfail += 1
        testnum += 1
        old_SSE = numpy.load(dir + 'legacy_SSE.pkl', allow_pickle=True)
        d = cluster.stats.old_SSE(data,clusterid)
        t = numpy.allclose(d,old_SSE,rtol,atol)
        if t and verbose > 1:
            print('old_SSE passes')
        elif not t:
            if verbose:
                print('old_SSE fails')
            testfail += 1
        testnum += 1
        f = open(dir + 'legacy_SSE.pkl', 'rb')
        SSE = pickle.load(f)
        sse = cluster.stats.SSE(data,levs)
        t = numpy.allclose(sse,SSE,rtol,atol)
        if t and verbose > 1:
            print('SSE passes')
        elif not t:
            if verbose:
                print('SSE fails')
            testfail += 1
        testnum += 1
        point_SSE = numpy.load(dir + 'legacy_point_SSE.pkl', allow_pickle=True)
        psse = cluster.stats.point_SSE(data,levs)
        t = numpy.allclose(psse,point_SSE,rtol,atol)
        if t and verbose > 1:
            print('point_SSE passes')
        elif not t:
            if verbose:
                print('point_SSE fails')
            testfail += 1
        testnum += 1
    return testnum,testfail

if __name__ == '__main__':
    import cluster
    cluster.test()
