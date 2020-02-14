"""Generates the test standards for cluster.

Importing this module creates the test standards and data that cluster uses to
test itself, overwriting any that already exist.  As a result, it should only be
imported on a system that has already been verified as working.  It should only
need to be imported when a change to cluster requires an expansion or
modification to the tests needed to verify its operation.
"""

import numpy
import cluster
import pickle
import sys

for i in sys.path:
    if 'site-packages' in i:
        dir = i + '/cluster/test/data/'
        break

print('Distances module')
a = numpy.random.randint(20,size=20)
a.dump(dir + 'distance_a.pkl')
b = numpy.random.randint(20,size=20)
b.dump(dir + 'distance_b.pkl')
c = b.astype(float)
c[numpy.random.randint(20,size=numpy.random.randint(10))] = numpy.nan
c.dump(dir + 'distance_c.pkl')
weights = numpy.random.rand(20)
weights.dump(dir + 'distance_weights.pkl')
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
with open(dir + 'distance_dist.pkl','wb') as f:
    pickle.dump(dist,f)
distance_no_missing = {}
for i in dist:
    d = cluster.distances.distance(a,b,weights,i[0])
    distance_no_missing[i[0]] = d
with open(dir + 'distances_no_missing.pkl','wb') as f:
    pickle.dump(distance_no_missing,f)
distance_missing = {}
for i in dist:
    d = cluster.distances.distance(a,c,weights,i[0])
    distance_missing[i[0]] = d
with open(dir + 'distances_missing.pkl','wb') as f:
    pickle.dump(distance_missing,f)

print('Stats module')
data = numpy.random.rand(40,6)
data.dump(dir + 'data.pkl')
distancematrix = cluster.stats.distancematrix(data)
with open(dir + 'distancematrix.pkl','wb') as f:
    pickle.dump(distancematrix,f)
fulldistancematrix = cluster.stats.fulldistancematrix(data)
fulldistancematrix.dump(dir + 'fulldistancematrix.pkl')
levs = numpy.random.rand(40,4)
levs = levs/levs.sum(axis=1).reshape(len(levs),1)
levs.dump(dir + 'levs.pkl')
silhouette = cluster.stats.silhouette(1,levs,dm=distancematrix)
silhouette.dump(dir + 'silhouette.pkl')
check1 = cluster.stats.levscheck(levs)
with open(dir + 'check1.pkl','wb') as f:
    pickle.dump(check1,f)
levs2 = numpy.concatenate([levs,numpy.zeros((len(levs),1)),numpy.ones((len(levs),1))],axis=1)
check2 = cluster.stats.levscheck(levs2)
with open(dir + 'check2.pkl','wb') as f:
    pickle.dump(check2,f)
method = [['a','arithmetic mean'],
          ['m','median'],
          ['s','absolute mean'],
          ['g','geometric mean'],
          ['h','harmonic mean'],
          ['q','quadratic mean'],
          ['d','mode'],
          ['oe','medoid']]
with open(dir + 'method.pkl','wb') as f:
    pickle.dump(method,f)
singleclustercentroid = {}
for i in method:
    singleclustercentroid[i[0]] = cluster.stats.singleclustercentroid(data,lev=levs[:,0],method=i[0])
with open(dir + 'singleclustercentroid.pkl','wb') as f:
    pickle.dump(singleclustercentroid,f)
clustercentroids = cluster.stats.clustercentroids(data,levs)
clustercentroids.dump(dir + 'clustercentroids.pkl')
SEmatrix = cluster.stats.SEmatrix(data,levs)
SEmatrix.dump(dir + 'SEmatrix.pkl')
SElink = [['m','maximum link'],
          ['s','single link'],
          ['a','average link']]
with open(dir + 'SElink.pkl','wb') as f:
    pickle.dump(SElink,f)
SEdata = numpy.random.randint(5,size=(40,6))
SEdata.dump(dir + 'SEdata.pkl')
SEmatrix_mode = {}
for i in SElink:
    SEmatrix_mode[i[0]] = cluster.stats.SEmatrix(SEdata,levs,link=i[0],method='d')
with open(dir + 'SEmatrix_mode.pkl','wb') as f:
    pickle.dump(SEmatrix_mode,f)

print('Hierarch module')
links = [['s','Single Link'],
         ['m','Complete Link'],
         ['ca','Centroid Link'],
         ['a','Average Link'],
         ['w',"Ward's Link"],
         ['g',"Grower's Link"],
         [0.4,'Flexible Strategy'],
         [numpy.array([0.2,0.3,0.4,0.5]),'Lance-Wiliams Coefficients']]
with open(dir + 'links.pkl','wb') as f:
    pickle.dump(links,f)
tie = [[None,'No Ties'],
       ['aggr','Aggresive Group Formation'],
       ['doc','Docile Group Formation'],
       ['random','Random tie resolution'],
       ['sas','SAS/STAT tie breaking method']]
with open(dir + 'tie.pkl','wb') as f:
    pickle.dump(tie,f)
for i in links:
    for j in tie:
        tree = cluster.hierarch.aggtreecluster(distancematrix = fulldistancematrix,link=i[0],tie=j[0],dist='p')
        filename = 'tree_%s_%s.pkl' % (i[0],j[0])
        tree.save(dir + filename)
clinks = [['co','Medoid Link'],
#          ['cda','Mode Average Link'],
#          ['cds','Mode Single Link'],
#          ['cdm','Mode Complete Link']
           ]
with open(dir + 'clinks.pkl','wb') as f:
    pickle.dump(clinks,f)
for i in clinks:
    for j in tie:
        tree = cluster.hierarch.aggtreecluster(data=data,link=i[0],tie=j[0])
        filename = 'tree_%s_%s.pkl' % (i[0],j[0])
        tree.save(dir + filename)
test = [(0,'test0'), (1,'test1'),(2,'test2'),(-1,'test-1'),(-2,'test-2')]
tree.aliases(test)
with open(dir + 'tree.pkl','wb') as f:
    pickle.dump(tree,f)
node = tree[0]
with open(dir + 'node.pkl','wb') as f:
    pickle.dump(node,f)
tree.save(dir + 'tr.pkl')
ancestors = tree.ancestors(0)
with open(dir + 'ancestors.pkl','wb') as f:
    pickle.dump(ancestors,f)
decendants = tree.decendants(-2)
with open(dir + 'decendants.pkl','wb') as f:
    pickle.dump(decendants,f)
cut = tree.cut(12)
cut.dump(dir + 'cut.pkl')
tree.scale()
with open(dir + 'tree_scaled.pkl','wb') as f:
    pickle.dump(tree,f)
kind = [['dist','distances'],
        ['rank','ranks']]
with open(dir + 'kind.pkl','wb') as f:
    pickle.dump(kind,f)
for i in kind:
    cop = tree.cophenetic(i[0])
    filename = 'cop_%s.pkl' % i[0]
    cop.dump(dir + filename)
treestring = str(tree)
with open(dir + 'treestring.pkl','wb') as f:
    pickle.dump(treestring,f)
heavy = [[None,'not sorted'],
         ['left','sorted left'],
         ['right','sorted right']]
with open(dir + 'heavy.pkl','wb') as f:
    pickle.dump(heavy,f)
plot_weight = numpy.random.rand(40)
plot_weight.dump(dir + 'plot_weight.pkl')
for i in heavy:
    filename = 'plot_datasort_%s.pkl' % i[0]
    plot_datasort = cluster.hierarch.plot.datasort(tree,i[0],plot_weight)
    with open(dir + filename,'wb') as f:
        pickle.dump(plot_datasort,f)
distalt = [[None,'node distances'],
           ['order','formation order'],
           [numpy.random.rand(40),'provided distances']]
with open(dir + 'distalt.pkl','wb') as f:
    pickle.dump(distalt,f)
sym = [[True,'symmetric branching'],
       [False,'weighted branching']]
with open(dir + 'sym.pkl','wb') as f:
    pickle.dump(sym,f)
for i in distalt:
    for j in sym:
        coords = cluster.hierarch.plot.coordinates(tree,zero=-1,distalt=i[0], sym=j[0])
        filename = 'coords_%s_%s.pkl' % (i[1],j[0])
        with open(dir + filename, 'wb') as f:
            pickle.dump(coords,f)

print('Partition module')
initial = numpy.zeros((40,3))
initial[list(range(40)),numpy.random.randint(3,size=40)] = 1
initial.dump(dir + 'initial.pkl')
kmeans = cluster.partition.kmeans(data,3,initial=initial)
kmeans.dump(dir + 'kmeans.pkl')
cmeans = cluster.partition.cmeans(data,3,initial=initial)
cmeans.dump(dir + 'cmeans.pkl')
cmeans_noise = cluster.partition.cmeans_noise(data,3,initial=initial)
cmeans_noise.dump(dir + 'cmeans_noise.pkl')
