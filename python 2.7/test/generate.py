"""Generates the test standards for cluster.

Importing this module creates the test standards and data that cluster uses to
test itself, overwriting any that already exist.  As a result, it should only be
imported on a system that has already been verified as working.  It should only
need to be imported when a change to cluster requires an expansion or
modification to the tests needed to verify its operation.
"""

import numpy
import cluster
import cPickle
import sys

for i in sys.path:
    if 'site-packages' in i:
        dir = i + '/cluster/test/data/'
        break

print 'Distances module'
a = numpy.random.randint(20,size=20)
a.dump(dir + 'distance_a.txt')
b = numpy.random.randint(20,size=20)
b.dump(dir + 'distance_b.txt')
c = b.astype(float)
c[numpy.random.randint(20,size=numpy.random.randint(10))] = numpy.nan
c.dump(dir + 'distance_c.txt')
weights = numpy.random.rand(20)
weights.dump(dir + 'distance_weights.txt')
dist = [['e', 'Euclidian'],
        ['p', 'Squared Euclidian'],
        ['b', 'City Block'],
        ['h', 'Hamming'],
        ['c', 'Pearson'],
        ['a', 'Absolute Pearson'],
        ['u', 'Uncentered Pearson'],
        ['r', 'arccosine of Uncentered Pearson'],
        ['x', 'Absolute Uncentered Pearson'],
        ['sc', 'Spearman'],
        ['su', 'Uncentered Spearman'],
        ['sr', 'arccosine of Uncentered Spearman'],
        ['sx', 'Absolute Uncentered Spearman'],
        ['k', 'Kendall'],
        ['t', 'Modified Simple Matching of Rogers and Tanimoto'],
        ['y', 'Modified Simple Matching of Sokal and Sneath'],
        ['j', 'Jaccard'],
        ['d', 'Modified Jaccard of Dice'],
        ['z', 'Modified Jaccard of Sokal and Sneath'],
        ['L1', 'First order Minkowski Metric'],
        ['L2', 'Second order Minkowski Metric'],
        ['L3', 'Third order Minkowski Metric'],
        ['L4', 'Fourth order Minkowski Metric'],
        ['Linf', 'Chebychev']]
f = file(dir + 'distance_dist.txt','w')
cPickle.dump(dist,f)
distance_no_missing = {}
for i in dist:
    d = cluster.distances.distance(a,b,weights,i[0])
    distance_no_missing[i[0]] = d
f = file(dir + 'distances_no_missing.txt','w')
cPickle.dump(distance_no_missing,f)
distance_missing = {}
for i in dist:
    d = cluster.distances.distance(a,c,weights,i[0])
    distance_missing[i[0]] = d
f = file(dir + 'distances_missing.txt','w')
cPickle.dump(distance_missing,f)

print 'Stats module'
data = numpy.random.rand(40,6)
data.dump(dir + 'data.txt')
distancematrix = cluster.stats.distancematrix(data)
f = file(dir + 'distancematrix.txt','w')
cPickle.dump(distancematrix,f)
fulldistancematrix = cluster.stats.fulldistancematrix(data)
fulldistancematrix.dump(dir + 'fulldistancematrix.txt')
levs = numpy.random.rand(40,4)
levs = levs/levs.sum(axis=1).reshape(len(levs),1)
levs.dump(dir + 'levs.txt')
silhouette = cluster.stats.silhouette(1,levs,dm=distancematrix)
silhouette.dump(dir + 'silhouette.txt')
check1 = cluster.stats.levscheck(levs)
f = file(dir + 'check1.txt','w')
cPickle.dump(check1,f)
levs2 = numpy.concatenate([levs,numpy.zeros((len(levs),1)),numpy.ones((len(levs),1))],axis=1)
check2 = cluster.stats.levscheck(levs2)
f = file(dir + 'check2.txt','w')
cPickle.dump(check2,f)
method = [['a','arithmetic mean'],
          ['m','median'],
          ['s','absolute mean'],
          ['g','geometric mean'],
          ['h','harmonic mean'],
          ['q','quadratic mean'],
          ['d','mode'],
          ['oe','medoid']]
f = file(dir + 'method.txt','w')
cPickle.dump(method,f)
singleclustercentroid = {}
for i in method:
    singleclustercentroid[i[0]] = cluster.stats.singleclustercentroid(data,lev=levs[:,0],method=i[0])
f = file(dir + 'singleclustercentroid.txt','w')
cPickle.dump(singleclustercentroid,f)
clustercentroids = cluster.stats.clustercentroids(data,levs)
clustercentroids.dump(dir + 'clustercentroids.txt')
SEmatrix = cluster.stats.SEmatrix(data,levs)
SEmatrix.dump(dir + 'SEmatrix.txt')
SElink = [['m','maximum link'],
          ['s','single link'],
          ['a','average link']]
f = file(dir + 'SElink.txt','w')
cPickle.dump(SElink,f)
SEdata = numpy.random.randint(5,size=(40,6))
SEdata.dump(dir + 'SEdata.txt')
SEmatrix_mode = {}
for i in SElink:
    SEmatrix_mode[i[0]] = cluster.stats.SEmatrix(SEdata,levs,link=i[0],method='d')
f = file(dir + 'SEmatrix_mode.txt','w')
cPickle.dump(SEmatrix_mode,f)

print 'Hierarch module'
links = [['s','Single Link'],
         ['m','Complete Link'],
         ['ca','Centroid Link'],
         ['a','Average Link'],
         ['w',"Ward's Link"],
         ['g',"Grower's Link"],
         [0.4,'Flexible Strategy'],
         [numpy.array([0.2,0.3,0.4,0.5]),'Lance-Wiliams Coefficients']]
f = file(dir + 'links.txt','w')
cPickle.dump(links,f)
tie = [[None,'No Ties'],
       ['aggr','Aggresive Group Formation'],
       ['doc','Docile Group Formation'],
       ['random','Random tie resolution'],
       ['sas','SAS/STAT tie breaking method']]
f = file(dir + 'tie.txt','w')
cPickle.dump(tie,f)
for i in links:
    for j in tie:
        tree = cluster.hierarch.aggtreecluster(distancematrix = fulldistancematrix,link=i[0],tie=j[0],dist='p')
        filename = 'tree_%s_%s.txt' % (i[0],j[0])
        tree.save(dir + filename)
clinks = [['co','Medoid Link'],
#          ['cda','Mode Average Link'],
#          ['cds','Mode Single Link'],
#          ['cdm','Mode Complete Link']
           ]
f = file(dir + 'clinks.txt','w')
cPickle.dump(clinks,f)
for i in clinks:
    for j in tie:
        tree = cluster.hierarch.aggtreecluster(data=data,link=i[0],tie=j[0])
        filename = 'tree_%s_%s.txt' % (i[0],j[0])
        tree.save(dir + filename)
test = [(0,'test0'), (1,'test1'),(2,'test2'),(-1,'test-1'),(-2,'test-2')]
tree.aliases(test)
f = file(dir + 'tree.txt','w')
cPickle.dump(tree,f)
node = tree[0]
f = file(dir + 'node.txt','w')
cPickle.dump(node,f)
tree.save(dir + 'tr.txt')
ancestors = tree.ancestors(0)
f = file(dir + 'ancestors.txt','w')
cPickle.dump(ancestors,f)
decendants = tree.decendants(-2)
f = file(dir + 'decendants.txt','w')
cPickle.dump(decendants,f)
cut = tree.cut(12)
cut.dump(dir + 'cut.txt')
tree.scale()
f = file(dir + 'tree_scaled.txt','w')
cPickle.dump(tree,f)
kind = [['dist','distances'],
        ['rank','ranks']]
f = file(dir + 'kind.txt','w')
cPickle.dump(kind,f)
for i in kind:
    cop = tree.cophenetic(i[0])
    filename = 'cop_%s.txt' % i[0]
    cop.dump(dir + filename)
treestring = str(tree)
f = file(dir + 'treestring.txt','w')
cPickle.dump(treestring,f)
heavy = [[None,'not sorted'],
         ['left','sorted left'],
         ['right','sorted right']]
f = file(dir + 'heavy.txt','w')
cPickle.dump(heavy,f)
plot_weight = numpy.random.rand(40)
plot_weight.dump(dir + 'plot_weight.txt')
for i in heavy:
    filename = 'plot_datasort_%s.txt' % i[0]
    plot_datasort = cluster.hierarch.plot.datasort(tree,i[0],plot_weight)
    f = file(dir + filename,'w')
    cPickle.dump(plot_datasort,f)
distalt = [[None,'node distances'],
           ['order','formation order'],
           [numpy.random.rand(40),'provided distances']]
f = file(dir + 'distalt.txt','w')
cPickle.dump(distalt,f)
sym = [[True,'symmetric branching'],
       [False,'weighted branching']]
f = file(dir + 'sym.txt','w')
cPickle.dump(sym,f)
for i in distalt:
    for j in sym:
        filename = 'coords_%s_%s.txt' % (i[1],j[0])
        f = file(dir + filename, 'w')
        coords = cluster.hierarch.plot.coordinates(tree,zero=-1,distalt=i[0], sym=j[0])
        cPickle.dump(coords,f)

print 'Partition module'
initial = numpy.zeros((40,3))
initial[range(40),numpy.random.randint(3,size=40)] = 1
initial.dump(dir + 'initial.txt')
kmeans = cluster.partition.kmeans(data,3,initial=initial)
kmeans.dump(dir + 'kmeans.txt')
cmeans = cluster.partition.cmeans(data,3,initial=initial)
cmeans.dump(dir + 'cmeans.txt')
cmeans_noise = cluster.partition.cmeans_noise(data,3,initial=initial)
cmeans_noise.dump(dir + 'cmeans_noise.txt')

print 'Legacy functions'
clusterid = numpy.random.randint(5,size=40)
clusterid.dump(dir + 'legacy_clusterid.txt')
dm = numpy.random.rand(40,40)
dm -= numpy.identity(40)*numpy.diagonal(dm)
dm *= 1/numpy.sum(dm,axis=1).reshape(40,1)
dm.dump(dir + 'legacy_dm.txt')
old_silhouette = numpy.array(cluster.stats.old_silhouette(1,clusterid,dm))
old_silhouette.dump(dir + 'legacy_silhouette.txt')
members = cluster.stats.members(clusterid)
f = file(dir + 'legacy_members.txt','w')
cPickle.dump(members,f)
levs = cluster.stats.clusterid_to_levs(clusterid)
levs.dump(dir + 'legacy_levs.txt')
method = [['a','arithmetic mean'],
          ['m','median']]
f = file(dir + 'legacy_method.txt','w')
cPickle.dump(method,f)
transpose = [[True,'columns'],
             [False,'rows']]
f = file(dir + 'legacy_transpose.txt','w')
cPickle.dump(transpose,f)
old_singleclustercentroids = []
for i in method:
    for j in transpose:
        if j[0]:
            d = cluster.stats.old_singleclustercentroid(numpy.transpose(data),members[0],i[0],j[0])
        else:
            d = cluster.stats.old_singleclustercentroid(data,members[0],i[0],j[0])
        old_singleclustercentroids.append(d)
old_singleclustercentroids = numpy.array(old_singleclustercentroids)
old_singleclustercentroids.dump(dir + 'legacy_singleclustercentroids.txt')
old_clustercentroids = cluster.stats.old_clustercentroids(data,members)
old_clustercentroids.dump(dir + 'legacy_clustercentroids.txt')
old_SSE = cluster.stats.old_SSE(data,clusterid)
old_SSE.dump(dir + 'legacy_SSE.txt')
SSE = cluster.stats.SSE(data,levs)
f = file(dir + 'legacy_SSE.txt','w')
cPickle.dump(SSE,f)
point_SSE = cluster.stats.point_SSE(data,levs)
point_SSE.dump(dir + 'legacy_point_SSE.txt')
