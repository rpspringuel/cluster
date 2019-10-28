"""Hierarchical clustering methods and functions related to them.

Hierarchical clustering produces nested clusters from the data.  The methods
here are based upon starting with each data point in a seperate cluster and
then successively joining the closest clusters until only one cluster remains.

A complete version history and licence and copyright information are located
in the source code.
"""


##########################
## Liscense Information ##
##########################

###############################################################################
#Copyright (c) 2008-2010, R. Padraic Springuel                                #
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
import cluster.stats as stats
import cluster._support as _support
import cluster.distances as distances
import types

rtol = 1.0000000000000001e-005
atol = 1e-008

class AggNode(object):
    """An aggnode represents the joining of two clusters into a single cluster.
    
    Properties:
        left, right : int
            The two clusters being joined together.  Original data points are
            numbered from 0 to (# data points -1) while clusters are numbered
            from -1 to -(number of data points-1)
        distance : float
            Optional.  The seperation between the two clusters being joined.  
            Will default to 0 if none is given.
        leftalias, rightalias : string
            String aliases for the data/clusters that may be more useful in
            identifying them than their numerical designation.
    """
    def __init__(self,left,right,distance=0,leftalias=None,rightalias=None):
        if type(left) is not int or type(right) is not int:
            if int(left) == left and int(right) == right:
                left = int(left)
                right = int(right)
            else:
                raise TypeError('Data/clusters must be identified by integers.')
        if type(distance) is not float:
            distance = float(distance)
        self.left = left
        self.right = right
        self.distance = distance
        if leftalias is None:
            self.leftalias = str(left)
        else:
            self.leftalias = leftalias
        if rightalias is None:
            self.rightalias = str(right)
        else:
            self.rightalias = rightalias
    def __str__(self):
        r = '(%s, %s) : %f' % (self.leftalias,self.rightalias,self.distance)
        return r
    def __eq__(self,y):
        """x == y
        
        Because distances are often floats, equivalence for them is evaluated
        using numpy.allclose rather than strict equivalence.  As a result, this
        module defines two global varaibles in its name space (rtol and atol)
        which can be used to control the sensitivity of this equivalence check.
        """
        test1 = self.left == y.left and self.right == y.right
        test2 = self.left == y.right and self.right == y.left
        test3 = numpy.allclose(self.distance,y.distance,rtol,atol)
        test = (test1 or test2) and test3
        return test

class AggTree(object):
    """A agglomerative hierarchical clustering solution.
    
    Essentially a list of the nodes in the clustering solution, this is
    implemented as its own class so that it will have certian properties.
    In particular, initializations of this class will check to make sure that
    the list of nodes is valid, appended/replacement nodes will be checked for 
    validity, and special methods are available.
    AggNodes should be listed in the reverse order of how they were made to make
    the tree.  I.e. tree[0] is the last joining to be made in assembling the
    tree while tree[-1] is the first.  This is so the index of the cluster made
    by a joining matches with the integer used to identify it when it is joined
    to another cluster later on (i.e. AggNode(-4,-3) would join the nodes at
    tree[-4] and tree[-3]).  This is the reverse order of how Pycluster orders
    the members of its Tree class.
    
    Properties:
        nodes : list of AggNode
            The nodes that make up the clustering solution.
        pop : list of int
            How many data points are in each node.  pop[i] corresponds to
            nodes[i].  By default, it is assumed that each positive numbered
            node represents a single occurance of a data point.  If this is
            not the case (i.e. all(freq==1) is false) then the value of pop[i]
            should be manually overridden for any node which brings in a new 
            data point with freq != 1.  If building the tree one node at a time
            (as is done in aggtreecluster) then this adjusted frequency will be
            propogated to later nodes automatically.
    
    Notes:
        This class is more flexible than the Pycluster equivalent because it
        allows partial trees to be stored within it.  Care should be used,
        therefore, when manually creating AggTrees.
    """
    def __init__(self,nodes):
        for i in nodes:
            if type(i) is not AggNode:
                raise TypeError('Members of tree must be nodes.')
        if nodes[-1].right < 0:
            error = 'Node %i referenced before assignment.' % nodes[-1].right
            raise ValueError(error)
        elif nodes[-1].left < 0:
            error = 'Node %i referecned before assignment.' % nodes[-1].left
            raise ValueError(error)
        self.nodes = [nodes[-1]]
        self.pop = [2]
        self.assigned = [nodes[-1].right,nodes[-1].left]
        for i in nodes[-2::-1]:
            if i.left < -len(self.nodes):
                error = 'Node %i referenced before assignment.' % i.left
                raise ValueError(error)
            elif i.right < -len(self.nodes):
                error = 'Node %i referenced before assignment.' % i.right
                raise ValueError(error)
            if i.left in self.assigned:
                error = 'Node %i is joined to another node multiple times.' % i.left
                raise ValueError(error)
            elif i.right in self.assigned:
                error = 'Node %i is joined to another node multiple times.' % i.right
                raise ValueError(error)
            self.nodes.insert(0,i)
            self.assigned.append(i.left)
            self.assigned.append(i.right)
            if i.left < 0 and i.right < 0:
                self.pop.insert(0,self.pop[i.left]+self.pop[i.right])
            elif i.left < 0:
                self.pop.insert(0,self.pop[i.left]+1)
            elif i.right < 0:
                self.pop.insert(0,self.pop[i.right]+1)
            else:
                self.pop.insert(0,2)
    def __getitem__(self,i):
        return self.nodes[i]
    def __str__(self):
        r = ''
        for i in self.nodes:
            r += i.__str__()
            r += '\n'
        return r[:-1]
    def __setitem__(self,i,node):
        """Changes a node in the tree after checking to see that it is valid.
        """
        if type(node) is not AggNode:
            raise TypeError('Members of tree must be nodes.')
        temp = []
        for j in self.nodes:
            temp.append(j)
        self.nodes[i] = node
        try:
            self.__init__(self.nodes)
        except:
            self.nodes = temp
            raise
    def __len__(self):
        return len(self.nodes)
    def __eq__(self,y):
        """Basic equivalence test for trees.
        
        This tests for exact equivalence.  I.e. nodes have to be in the exact
        same order, even if they are created at the same distance.  For an
        equivalence test that is less sensitive to node order without loss of
        distnace sensitivity use:
        numpy.allclose(self.cophenetic('dist'),y.cophenetic('dist')).
        """
        if len(self) != len(y):
            test = False
        else:
            test = True
            for i in range(len(self.nodes)):
                test = test and self.nodes[i] == y.nodes[i]
                if not test:
                    break
        return test
    def append(self,node):
        """Adds a node to the tree after checking to see that it is valid.
        
        Note: Since clusters are identified by a negative number indicating the
        order of their joining (i.e. -1 is the first cluster formed, -2 is the
        second, etc.) appended nodes are added to the begining of the tree.
        """
        if type(node) is not AggNode:
            raise TypeError('Members of tree must be nodes.')
        if node.left < -len(self.nodes):
            error = 'Node %i referenced before assignment.' % node.left
            raise ValueError(error)
        elif node.right < -len(self.nodes):
            error = 'Node %i referenced before assignment.' % node.right
            raise ValueError(error)
        if node.left in self.assigned:
            error = 'Node %i is joined to another node multiple times.' % node.left
            raise ValueError(error)
        elif node.right in self.assigned:
            error = 'Node %i is joined to another node multiple times.' % node.right
            raise ValueError(error)
        self.nodes.insert(0,node)
        self.assigned.append(node.left)
        self.assigned.append(node.right)
        if node.left < 0 and node.right < 0:
            self.pop.insert(0,self.pop[node.left]+self.pop[node.right])
        elif node.left < 0:
            self.pop.insert(0,self.pop[node.left]+1)
        elif node.right < 0:
            self.pop.insert(0,self.pop[node.right]+1)
        else:
            self.pop.insert(0,2)
    def scale(self):
        """Scales the distances in the tree so that they are between 0 and 1.
        """
        distances = []
        for i in self.nodes:
            distances.append(i.distance)
        floor = numpy.nanmin(distances)
        range = numpy.ptp(distances)
        for i in self.nodes:
            i.distance = (i.distance-floor)/range
    def complete(self):
        """Checks to see if the given tree represents a complete clustering solution.
        
        Returns:
            r : boolean
                True if all data points and clusters are present in tree.
                False otherwise.  Number of data points is assumed to be equal
                to 1 more than the largest identifying index in the tree.
        """
        nodes = [-len(self)]
        for i in self.nodes:
            nodes.append(i.right)
            nodes.append(i.left)
        nodes.sort()
        r = nodes == list(range(min(nodes),max(nodes)+1))
        return r
    def cut(self,nclusters):
        """Groups data into clusters based on tree structure.
        
        Converts a hierarchical clustering solution into an equivalent 
        exlcusive partitional clustering solution.
        
        While the transpose parameter has been removed, the behavior formerly
        obtained by setting transpose to True can be duplicated by the command
        numpy.transpose(tree.cut(nclusters)).
        
        Parameters:
            self : AggTree
                The hierarchical clustering solution.
            nclusters : integer
                The desired number of clusters.  Should be positive and less
                than the total number of data points.
        Returns:
            levs : ndarray
                A rank 2 array with dimensions # data points x nclusters
                containing the level to which each data point belongs to each
                cluster.
        """
        if not self.complete():
            raise AttributeError('Incomplete trees cannot be cut.')
        nodes = []
        clusters = [-len(self)]
        for i in range(nclusters-1):
            clusters.remove(-len(self.nodes)+i)
            clusters.append(self.nodes[i].right)
            clusters.append(self.nodes[i].left)
            nodes.append(self.nodes[i].right)
            nodes.append(self.nodes[i].left)
        clusters = numpy.array(clusters)[:,numpy.newaxis].tolist()
        for i in range(nclusters-1,len(self.nodes)):
            nodes.append(self.nodes[i].right)
            nodes.append(self.nodes[i].left)
            for j in range(len(clusters)):
                if -len(self.nodes)+i in clusters[j]:
                    clusters[j].append(self.nodes[i].right)
                    clusters[j].append(self.nodes[i].left)
        levs = numpy.zeros((max(nodes)+1,nclusters),float)
        for i in range(len(clusters)):
            for j in clusters[i]:
                if j >= 0:
                    levs[j][i] = 1
        return levs
    def decendants(self,node,alias=False):
        """Find the nodes and data points in the given node.
        
        Parameters:
            self : AggTree
                The tree clustering solution.
            node : int
                Should be less than 0.  The index of the node whose decendants
                are desired.
        Returns:
            dec : list
                List of the nodes and data points in node.
        """
        if node >= 0:
            dec = []
        else:
            dec = [self.nodes[node].left,self.nodes[node].right]
            for i in dec:
                if i < 0:
                    dec.append(self.nodes[i].left)
                    dec.append(self.nodes[i].right)
        dec.sort()
        return dec
    def ancestors(self,node):
        """Find the nodes which contain the given node.
        
        Parameters:
            self : AggTree
                The tree clustering solution.
            node : int
                Should be less than 0.  The index of the node whose
                ancestors are desired.
        Returns:
            anc : list
                List of the nodes containing node.
        """
        anc = [node]
        for i in anc:
            for j in range(-len(self.nodes),0)[::-1]:
                if i == self.nodes[j].left or i == self.nodes[j].right:
                    anc.append(j)
                    break
        anc.remove(node)
        anc.sort()
        return anc
    def aliases(self,a=None):
        """Provides a list of aliases associated with nodes and data, or sets them.
        
        Parameters:
            self : AggTree
                The tree clustering solution.
            a : tuple or list of tuples
                Optional.  Tuples should be aranged as (n,alias) where n is the
                integer identifier of the node or data point and alias is its
                string alias.
        Returns:
            a : list of tuples
                Only returned if no a is given.  List of each numerical
                identifier for data or nodes with the corresponding alias.
        """
        if a is None:
            a = []
            for i in self.nodes:
                try:
                    if i.left != int(i.leftalias):
                        a.append((i.left,i.leftalias))
                except ValueError:
                    a.append((i.left,i.leftalias))
                try:
                    if i.right != int(i.rightalias):
                        a.append((i.right,i.rightalias))
                except ValueError:
                    a.append((i.right,i.rightalias))
            a.sort()
            return a
        elif type(a) is list:
            for i in a:
                for j in self.nodes:
                    if j.left == i[0]:
                        j.leftalias = i[1]
                        break
                    if j.right == i[0]:
                        j.rightalias = i[1]
                        break
            return
        elif type(a) is tuple:
            for j in self.nodes:
                if j.left == a[0]:
                    j.leftalias = a[1]
                    break
                if j.right == a[0]:
                    j.rightalias = a[1]
                    break
            return
    def save(self,filename):
        """Saves the tree to a human readable file.
        
        Parameters:
            self : AggTree
                A tree clustering solution.
            filename : string
                The name of the file where the tree is to be stored.
        """
        text = ''
        for i in self.nodes:
            text += '(%i, %i) : %f' % (i.left,i.right,i.distance)
            text += '; %s' % i.leftalias
            text += ' & %s' % i.rightalias
            text += '\n'
        a = open(filename, 'w')
        a.writelines(text)
        a.close()
        return
    def cophenetic(self,distance):
        """The cophenetic distance matrix for the tree.
        
        The cophenetic distance between two points is defined as the distance at
        which the two points are first joined into the same cluster.
        
        Parameters:
            self : AggTree
                A tree clustering solution.
            distance : string
                The type of cophentic distance to be used:
                'dist' - The value of distance property for the node which first
                         joins the two points.
                'rank' - The creation order of the cluster in the hierarchy.
        
        Returns:
            dm : ndarray
                Rank 2 array containing the cophenetic distance each pair of
                points.  The ith,jth element is the cophenetic distance between
                the ith and jth data points.
        """
        dm = numpy.zeros((len(self)+1,len(self)+1))
        for i in range(-len(self),0):
            dec1 = self.decendants(self[i].left)
            dec2 = self.decendants(self[i].right)
            for j in dec1:
                if j > 0:
                    for k in dec2:
                        if k > 0:
                            if distance == 'dist':
                                dm[j,k] = dm[k,j] = self[i].distance
                            elif distance == 'rank':
                                dm[j,k] = dm[k,j] = numpy.abs(i)
                            else:
                                raise ValueError('Unrecognized distance option.')
        return dm

def loadaggtree(filename):
    """Loads an agglomeratice cluster tree saved using save method for AggTree.
    
    Parameters:
        filename : string
            The name of the file where the tree that is to be retrieved is
            stored.
    """
    a = open(filename)
    b = a.readlines()
    nodes = []
    for i in range(len(b)):
        left = int(b[i][b[i].index('(')+1:b[i].index(',')])
        right = int(b[i][b[i].index(',')+1:b[i].index(')')])
        distance = float(b[i][b[i].index(':')+1:b[i].index(';')])
        leftalias = b[i][b[i].index(';')+2:b[i].index('&')-1]
        rightalias = b[i][b[i].index('&')+2:b[i].index('\n')]
        nodes.append(AggNode(left,right,distance,leftalias,rightalias))
    return AggTree(nodes)

def aggtreecluster(data=None,weights=None,dist='e',tie=None,link='m',distancematrix=None,verbose=False):
    """Implements agglomerative hierarchical clustering.
    
    Where possible this function makes use of the Lance-Williams update formula
    for calculating the distance between a newly formed cluster and all other
    clusters.  While this isn't necessarily the most computationally efficient
    algorithm for all methods, it is the most general and thus gives the largest
    range of ability straight out of the box.  More computationally efficient
    algorithms may be added at a later date.
    
    While the transpose parameter has been removed, the behavior formerly
    obtained by setting transpose to True can be duplicated by the command
    aggtreecluster(numpy.transpose(data),...).
    
    Parameters:
        data : ndarray
            Rank 2 array containing the data to be clustered.  Each row
            represents a single data point.  Optional if distancematrix is given
            (but see below).
        weights : ndarray
            Optional.  If given, a rank 1 array with length equal to the number
            of columns in data.  Entries specify the weight for each dimension
            in the distance function.
        dist : string
            Specifies the desired distance function by it's alias.
        tie : string
            Specifies method to be used for resolving ties for the minimum
            distance:
            None - Tie with oldest group will be choosen (oldest second group if
                   oldest groups are tied).  Data points are given an age based
                   on their order in the data array (older points appear first),
                   clusters are given an age based on the step at which they
                   were created (clusters created earlier are older). (default)
            random - Choose randomly from the ties  Method appears in L. Kaufman
                     and P. J. Rousseeuw, Finding groups in data: An
                     introduction to cluster analysis, Wiley series in
                     probability and mathematical _support: Applied
                     probability and _support (Wiley, 1990).
            aggr - Choose the tie that creates the largest new group (second
                   order ties resolved by None)
            doc - Choose the tie that creates the smallest new group (second
                  order ties resolved by None)
            sas - Same as None except the age of a cluster is the age of the
                  oldest data point in that cluster.  Method appears in SAS/STAT
                  User's Guide, Version 8, SAS Institute Inc. (1999),
                  http://www.okstate.edu/sas/v8/saspdf/stat/pdfidx.htm.
        link : string or float or ndarray or function
            Specifies the linkage method to be used:
            s - single-linkage (smallest pair-wise distance)
            m - maximum-linkage (largest pair-wise distance, default)
            c* - centroid-linkage (distance between centroids).  The wildcard
                 (*) should be replaced by the method to be used to find the
                 centroid.
            a - average-linkage (average pair-wise distance, or Unweighted Pair
                Group Method using Arithmetic average)
            p - Weighted Pair Group Method using Arithmetic average
            w - Ward's link (minimize increase in SSE)
            g - Gower's link (distance between centrdoid average)
            float - A flexible strategy.  The Lance-Williams formula is used
                    with the following constraints: alphaA = alphaB = (1 -
                    beta)/2 and gamma = 0.  beta is the parameter provided by
                    the user.  Method appears in G. N. Lance and W. T. Williams,
                    A general theory of classificatory sorting strategies: 1.
                    Hierarchical systems, The Computer Journal 9, 373 (1966),
                    http://dx.doi.org/10.1093/comjnl/9.4.373.
            ndarray - Static manipulation of the Lance-Williams formula.  The 
                      link should be a rank 1 array with 4 elements: alphaA,
                      alphaB, beta, and gamma.
            function - Dynamic manipulation of the Lance-Williams formula.  The
                       function should have the following properties:
                       Parameters:
                        n1, n2 : integer
                            The indecies of the two clusters being joined
                        tree : AggTree
                            The current state of the tree being built
                        N : integer
                            The number of data points.
                       Returns:
                        alphaA, alphaB, beta, gamma : ndarray
                            The values for the coeficients of the Lance-Williams
                            formula.  Each is a rank 1 ndarray of lenght (2N-1)
                            where N is number of data points.  The *[i]
                            corresponds to the coeficient to be used to calculte
                            the distance between the new cluster and the ith
                            cluster.  Values should be 0 for clusters which
                            don't yet exist.
                       See wardLN for an example function.
        distancematrix : ndarray or list of ndarrays
            Either a rank 2 array or a list of rank 1 arrays containing the 
            distances between each data point.  distancematrix[i][j] is the
            distance between point i and point j.  If distancematrix
            is given without data, then centroid-linkage (link == 'c*') cannot
            be used except in 1 case: link == 'ca' and dist == 'e'.
            If distancematrix is given then data, weights, and dist are ignored
            for all non-centroid methods and for the centroid method mentioned
            above.
        verbose: boolean
            If True then the algorithm will print periodic updates to the screen
            to indicate where it is in the process.
    Returns:
        tree : AggTree
            The hierarchical clustering solution.
    See Also:
        stats.singleclustercentroid, stats.fulldistancematrix, wardLN
    """
    if data is None and distancematrix is None:
        raise RuntimeError('Either data or distancematrix must be given.')
    elif not (data is None) and not (distancematrix is None) and len(data) != len(distancematrix):
        raise RuntimeError('data and distancematrix are of incompatible sizes.')
    elif data is None and type(link) is bytes:
        if link[0] == 'c' and not (link == 'ca' and dist == 'p'):
            raise RuntimeError('Centroid-linkage cannot be used without data.')
    elif distancematrix is None:
        if verbose:
            print('Calculating distance matrix.')
        distancematrix = stats.fulldistancematrix(data,weights,dist,verbose)
    elif type(distancematrix) is list:
        for i in range(len(distancematrix)):
            distancematrix[i].resize(len(distancematrix))
        distancematrix = numpy.array(distancematrix)
        distancematrix = distancematrix + numpy.transpose(distancematrix)
    N = len(distancematrix)
    if verbose:
        print('%i joinings will be required' % (N-1))
    current = list(range(N))
    distancematrix = numpy.resize(distancematrix,(2*N-1,N))
    distancematrix = numpy.transpose(distancematrix).copy()
    distancematrix = numpy.resize(distancematrix,(2*N-1,2*N-1))
    if verbose:
        print('Finding cluster 1')
    c = []
    d = []
    for i in range(len(current)):
        c += [current[i]]*(len(current)-i-1)
        d += current[i+1:]
    search = distancematrix[c,d]
    m = numpy.nanmin(search)
    if tie == 'random':
        ix = numpy.nonzero(search == m)
        i = numpy.random.randint(len(ix[0]))
        e = tuple(ia[i] for ia in ix)
        n1 = c[e[0]]
        n2 = d[e[0]]
    else:
        mask = search == m
        n1 = c[mask.argmax()]
        n2 = d[mask.argmax()]
    if verbose:
        print('%i, %i: %f' % (n1,n2,m))
    tree = AggTree([AggNode(n1,n2,m)])
    tree.pop[-1] = 2
    if type(link) is str:
        if link[0] == 'c':
            centroid = []
    LW = True
    while len(tree) < N-1:
        current.remove(n1)
        current.remove(n2)
        if type(link) is str:
            if link == 's':
                alphaA = alphaB = 0.5
                beta = 0.
                gamma = -0.5
            elif link == 'm':
                alphaA = alphaB = 0.5
                beta = 0.
                gamma = 0.5
            elif link == 'a':
                if n1 < 0 and n2 < 0:
                    alphaA = 1.*tree.pop[n1]/(tree.pop[n1]+tree.pop[n2])
                    alphaB = 1.*tree.pop[n2]/(tree.pop[n1]+tree.pop[n2])
                elif n1 < 0:
                    alphaA = 1.*tree.pop[n1]/(tree.pop[n1]+1.)
                    alphaB = 1./(tree.pop[n1]+1.)
                elif n2 < 0:
                    alphaA = 1./(1.+tree.pop[n2])
                    alphaB = 1.*tree.pop[n2]/(1.+tree.pop[n2])
                else:
                    alphaA = 0.5
                    alphaB = 0.5
                beta = 0.
                gamma = 0.
            elif link == 'p':
                alphaA = 0.5
                alphaB = 0.5
                beta = 0.
                gamma = 0.
            elif link == 'ca' and dist == 'p':
                if n1 < 0 and n2 < 0:
                    alphaA = 1.*tree.pop[n1]/(tree.pop[n1]+tree.pop[n2])
                    alphaB = 1.*tree.pop[n2]/(tree.pop[n1]+tree.pop[n2])
                    beta = -1.*tree.pop[n1]*tree.pop[n2]/(tree.pop[n1]+tree.pop[n2])**2
                elif n1 < 0:
                    alphaA = 1.*tree.pop[n1]/(tree.pop[n1]+1.)
                    alphaB = 1./(tree.pop[n1]+1.)
                    beta = -1.*tree.pop[n1]/(tree.pop[n1]+1.)**2
                elif n2 < 0:
                    alphaA = 1./(1.+tree.pop[n2])
                    alphaB = 1.*tree.pop[n2]/(1.+tree.pop[n2])
                    beta = -1.*tree.pop[n2]/(1.+tree.pop[n2])**2
                else:
                    alphaA = 0.5
                    alphaB = 0.5
                    beta = -0.25
                gamma = 0.
            elif link == 'w':
                alphaA,alphaB,beta,gamma = wardLW(n1,n2,tree,N)
            elif link == 'g':
                alphaA = alphaB = 0.5
                beta = -0.25
                gamma = 0
            elif link[0] == 'c':
                LW = False
                dec = tree.decendants(n1) + tree.decendants(n2) + [n1,n2]
                dec = numpy.array(dec)
                lev =  numpy.zeros(len(data))
                lev[dec[dec>=0]] = 1
                if link[1] == 'o':
                    centroid.insert(0, stats.singleclustercentroid(data,lev,1.,link[1:],weights,distancematrix[:N,:N]))
                else:
                    centroid.insert(0, stats.singleclustercentroid(data,lev,1.,link[1],weights))
                if link[1] == 'd':
                    k = list(map(len,centroid[0]))
                    index = numpy.zeros_like(k)
                    cent = numpy.zeros((numpy.prod(k),len(centroid[0])))
                    for n in range(numpy.prod(k)):
                        for m in range(len(index)):
                            cent[n][m] = centroid[0][m][index[m]]
                        index[0] += 1
                        for m in range(len(index)-1):
                            if index[m] == k[m]:
                                index[m] = 0
                                index[m+1] += 1
                    for i in current:
                        if i >= 0:
                            d = numpy.zeros(len(cent))
                            for n in range(len(cent)):
                                d[n] = distances.distance(data[i],cent[n],dist=dist)
                            if link[2] == 'm':
                                distancematrix[-len(tree),i] = distancematrix[i,-len(tree)] = d.max()
                            elif link[2] == 's':
                                distancematrix[-len(tree),i] = distancematrix[i,-len(tree)] = d.min()
                            elif link[2] == 'a':
                                distancematrix[-len(tree),i] = distancematrix[i,-len(tree)] = numpy.mean(d)
                            else:
                                raise ValueError('Link method ' + link + ' not supported.')
                        else:
                            d = numpy.zeros((len(cent),len(centroid[i])))
                            for n in range(len(cent)):
                                for m in range(len(centroid[i])):
                                    d[n][m] = distances.distance(centroid[i][m],cent[n],weights,dist)
                            if link[2] == 'm':
                                distancematrix[-len(tree),i] = distancematrix[i,-len(tree)] = d.max()
                            elif link[2] == 's':
                                distancematrix[-len(tree),i] = distancematrix[i,-len(tree)] = d.min()
                            elif link[2] == 'a':
                                distancematrix[-len(tree),i] = distancematrix[i,-len(tree)] = numpy.mean(d)
                            else:
                                raise ValueError('Link method ' + link + ' not supported.')
                    centroid[0] = cent.copy()
                else:
                    for i in current:
                        if i >= 0:
                            distancematrix[-len(tree),i] = distancematrix[i,-len(tree)] = distances.distance(data[i],centroid[0],weights,dist)
                        else:
                            distancematrix[-len(tree),i] = distancematrix[i,-len(tree)] = distances.distance(centroid[i],centroid[0],weights,dist)
            else:
                raise ValueError('Link method ' + link + ' not supported.')
        elif type(link) is float:
            beta = link
            alphaA = alphaB = (1. - beta)/2.
            gamma = 0
        elif type(link) is numpy.ndarray:
            alphaA = link[0]
            alphaB = link[1]
            beta = link[2]
            gamma = link[3]
        elif type(link) is types.FunctionType:
            alphaA,alphaB,beta,gamma = link(n1,n2,tree)
        else:
            raise ValueError('Link type "'+ type(link) + '" not valid.\nMust be string, float, ndarray, or function.')
        if LW:
            distancematrix[-len(tree)] = distancematrix[:,-len(tree)] = alphaA*distancematrix[n1] + alphaB*distancematrix[n2] + beta*distancematrix[n1,n2] + gamma*numpy.abs(distancematrix[n1]-distancematrix[n2])
        current.append(-len(tree))
        if verbose:
            print('Finding cluster %i' % (len(tree)+1))
        c = []
        d = []
        for i in range(len(current)):
            c += [current[i]]*(len(current)-i-1)
            d += current[i+1:]
        search = distancematrix[c,d]
        m = numpy.nanmin(search)
        if tie == 'random':
            ix = numpy.nonzero(search == m)
            i = numpy.random.randint(len(ix[0]))
            e = tuple(ia[i] for ia in ix)
            n1 = c[e[0]]
            n2 = d[e[0]]
        elif tie == 'aggr':
            mask = search == m
            n1 = c[mask.argmax()]
            n2 = d[mask.argmax()]
            p1 = 0
            for i in range(len(search)):
                if mask[i]:
                    if c[i] < 0:
                        p2 = tree.pop[c[i]]
                    else:
                        p2 = 1
                    if d[i] < 0:
                        p2 += tree.pop[d[i]]
                    else:
                        p2 += 1
                    if p2 > p1:
                        n1 = c[i]
                        n2 = d[i]
                        p1 = p2
        elif tie == 'doc':
            mask = search == m
            n1 = c[mask.argmax()]
            n2 = d[mask.argmax()]
            p1 = N
            for i in range(len(search)):
                if mask[i]:
                    if c[i] < 0:
                        p2 = tree.pop[c[i]]
                    else:
                        p2 = 1
                    if d[i] < 0:
                        p2 += tree.pop[d[i]]
                    else:
                        p2 += 1
                    if p2 < p1:
                        n1 = c[i]
                        n2 = d[i]
                        p1 = p2
        elif tie == 'sas':
            mask = search == m
            n1 = c[mask.argmax()]
            n2 = d[mask.argmax()]
            age = [N,N]
            for i in tree.decendants(n1):
                if i >=0 and i < age[0]:
                    age[0] = i
            for i in tree.decendants(n2):
                if i >=0 and i < age[1]:
                    age[1] = i
            age.sort()
            for i in range(len(search)):
                newage = [N,N]
                if mask[i]:
                    if c[i] >= 0:
                        newage[0] = c[i]
                    else:
                        for j in tree.decendants(c[i]):
                            if j >=0 and j < newage[0]:
                                newage[0] = j
                    if d[i] >= 0:
                        newage[1] = d[i]
                    else:
                        for j in tree.decendants(d[i]):
                            if j >=0 and j < newage[1]:
                                newage[1] = j
                    newage.sort()
                    if newage[1] < age[1] or (newage[1] == age[1] and newage[0] < age[0]):
                        n1 = c[i]
                        n2 = d[i]
                        age = newage
        else:
            mask = search == m
            n1 = c[mask.argmax()]
            n2 = d[mask.argmax()]
        if verbose:
            print('%i, %i: %f' % (n1,n2,m))
        tree.append(AggNode(n1,n2,m))
    return tree

def wardLW(n1,n2,tree,N):
    """Calculates the coeficients for the Lance-Williams formula for Ward's method.
    
    Parameters:
        n1, n2 : integer
            The indecies of the two clusters being joined
        tree : AggTree
            The current state of the tree being built
        N : integer
            The number of data points.
    Returns:
        alphaA, alphaB, beta, gamma : ndarray
            The values for the coeficients of the Lance-Williams formula.  Each
            is a rank 1 ndarray of lenght (2N-1) where N is number of data
            points.  *[i] corresponds to the coeficient to be used to 
            calculate the distance between the new cluster and the ith cluster.
            Values should be 0 for clusters which don't yet exist.
            
    Notes:
        Because gamma is constant for all clusters, numpy's broadcasting rules
        are used to save memory by setting it to a integer instead of an
        ndarray.
    """
    mq = numpy.concatenate([numpy.ones(N),numpy.zeros(N-1)])
    mq[len(mq)-len(tree.pop):] = tree.pop
    if n1 < 0 and n2 < 0:
        alphaA = 1.*(tree.pop[n1]+mq)/(tree.pop[n1]+tree.pop[n2]+mq)
        alphaB = 1.*(tree.pop[n2]+mq)/(tree.pop[n1]+tree.pop[n2]+mq)
        beta = -1.*mq/(tree.pop[n1]+tree.pop[n2]+mq)
    elif n1 < 0:
        alphaA = 1.*(tree.pop[n1]+mq)/(tree.pop[n1]+1.+mq)
        alphaB = 1.*(1.+mq)/(tree.pop[n1]+1.+mq)
        beta = -1.*mq/(tree.pop[n1]+1.+mq)
    elif n2 < 0:
        alphaA = 1.*(1.+mq)/(1.+tree.pop[n2]+mq)
        alphaB = 1.*(tree.pop[n2]+mq)/(1.+tree.pop[n2]+mq)
        beta = -1.*mq/(1.+tree.pop[n2]+mq)
    else:
        alphaA = 1.*(1.+mq)/(2.+mq)
        alphaB = 1.*(1.+mq)/(2.+mq)
        beta = -1.*mq/(2.+mq)
    gamma = 0
    return alphaA,alphaB,beta,gamma            


#########################
## Divisive Clustering ##
#########################

# Note: These functions and classes are not implemented yet and represent a work in progress.  Attempts to use them will always raise an error.

class DivNode(object):
    """A DivNode represents the splitting of a cluster into two clusters.
    
    The way that divisive hierarchical clustering is implemented here makes it
    incompatible with the classes that were set up for agglomerative
    hierarchical clustering.  In particular, an AggNode allows clusters to be
    identified by negative integers based on when the cluster was formed.  This
    saves data space but requires you to know the substructure of the cluster
    when we reference it.  In divisive hierarchical clustering we don't know
    this substructure.  Thus we require that clusters be referenced by a full
    list of their members.
    
    Properties:
        left, right : list of int
            The two clusters being formed.  Each list contains the positive
            integers which identify the data points in that cluster.
        distance : float
            Optional.  The seperation between the two clusters that have been
            formed.  Will default to 0 if none is given.
        leftalias, rightalias : string
            String aliases for the data/clusters that may be more useful in
            identifying them than their membership lists.
    """
    def __init__(self,left,right,distance=0,leftalias=None,rightalias=None):
        raise NotImplementedError('Divisive clustering is not available yet.')
        if type(left) is not list or type(right) is not list:
            raise TypeError('Clusters must be a list of positive integers.')
        for i in left:
            if i is not int or i < 0:
                raise TypeError('Clusters must be a list of positive integers.')
        for i in right:
            if i is not int or i < 0:
                raise TypeError('Clusters must be a list of positive integers.')
        if type(distance) is not float:
            distance = float(distance)
        left.sort()
        self.left = left
        right.sort()
        self.right = right
        self.distance = distance
        if leftalias is None:
            self.leftalias = str(left)
        else:
            self.leftalias = leftalias
        if rightalias is None:
            self.rightalias = str(right)
        else:
            self.rightalias = rightalias
    def __str__(self):
        r = '(%s, %s) : %f' % (self.leftalias,self.rightalias,self.distance)
        return r

class DivTree(object):
    """A divisive hierarchical clustering solution.
    
    Essentially a list of the nodes in the clustering solution, this is
    implemented as its own class so that it will have certian properties.
    In particular, initializations of this class will check to make sure that
    the list of nodes is valid, appended/replacement nodes will be checked for 
    validity, and special methods are available.
    DivNodes should be listed in the order of how they were made to make
    the tree.
    
    Properties:
        nodes : list of DivNode
            The nodes that make up the clustering solution.
        pop : list of int
            How many data points are in each node.  pop[i] corresponds to
            nodes[i].
    
    Notes:
        This class is more flexible than the Pycluster equivalent because it
        allows partial trees to be stored within it.  Care should be used,
        therefore, when manually creating AggTrees.
    """
    def __init__(self,nodes):
        raise NotImplementedError('Divisive clustering is not available yet.')
        for i in nodes:
            if type(i) is not DivNode:
                raise TypeError('Members of tree must be nodes.')
        self.nodes = [nodes[0]]
        self.pop = [len(nodes[0].right)+len(nodes[0].left)]
        for i in nodes[1::]:
            add = False
            test = i.left+i.right
            test.sort()
            for j in self.nodes:
                if test == j.right or test == j.left:
                    add = True
                    break
            if not add:
                error = 'The cluster %s does not exist in the tree' % (test)
                raise ValueError(error)
            self.nodes.append(i)
            self.pop.append(len(test))
    def __getitem__(self,i):
        return self.nodes[i]
    def __str__(self):
        r = ''
        for i in self.nodes:
            r += i.__str__()
            r += '\n'
        return r[:-1]
    def __setitem__(self,i,node):
        """Changes a node in the tree after checking to see that it is valid.
        """
        if type(node) is not DivNode:
            raise TypeError('Members of tree must be nodes.')
        temp = []
        for j in self.nodes:
            temp.append(j)
        self.nodes[i] = node
        try:
            self.__init__(self.nodes)
        except ValueError:
            self.nodes = temp
            raise ValueError('Replacement node tries to join a node to multiple clusters.')
    def __len__(self):
        return len(self.nodes)
    def append(self,node):
        """Adds a node to the tree after checking to see that it is valid.
        """
        if type(node) is not DivNode:
            raise TypeError('Members of tree must be nodes.')
        temp = []
        for i in self.nodes:
            temp.append(i)
        self.nodes.append(node)
        try:
            self.__init__(self.nodes)
        except ValueError:
            self.nodes = temp
            raise
    def scale(self):
        """Scales the distances in the tree so that they are between 0 and 1.
        """
        distances = []
        for i in self.nodes:
            distances.append(i.distance)
        for i in self.nodes:
            i.distance = (i.distance-min(distances))/(max(distances)-min(distances))
    def complete(self):
        """Checks to see if the given tree represents a complete clustering solution.
        
        Returns:
            r : boolean
                True if all data points and clusters are present in tree.
                False otherwise.  Number of data points is assumed to be equal
                to 1 more than the largest identifying index in the tree.
        """
        top = self.nodes[0].left+self.nodes[0].right
        bottom = []
        for i in self.nodes:
            if len(i.right) == 1:
                bottom += i.right
            if len(i.left) == 1:
                bottom += i.left
        top.sort()
        bottom.sort()
        r = top == bottom
        return r
    def cut(self,nclusters):
        """Groups data into clusters based on tree structure.
        
        Converts a hierarchical clustering solution into an equivalent 
        exlcusive partitional clustering solution.
        
        While the transpose parameter has been removed, the behavior formerly
        obtained by setting transpose to True can be duplicated by the command
        numpy.transpose(tree.cut(nclusters)).
        
        Parameters:
            self : AggTree
                The hierarchical clustering solution.
            nclusters : integer
                The desired number of clusters.  Should be positive and less
                than the total number of data points.
        Returns:
            levs : ndarray
                A rank 2 array with dimensions # data points x nclusters
                containing the level to which each data point belongs to each
                cluster.
        """
        if not self.complete():
            raise AttributeError('Incomplete trees cannot be cut.')
        if n == 1:
            clusters = [self.nodes[0].left+self.nodes[0].right]
        else:
            clusters = [self.nodes[0].left,self.nodes[0].right]
        for i in range(1,nclusters-1):
            test = self.nodes[i].left+self.nodes[i].right
            test.sort()
            clusters.remove(test)
            clusters.append(self.nodes[i].right)
            clusters.append(self.nodes[i].left)
            nodes.append(self.nodes[i].right)
            nodes.append(self.nodes[i].left)
        levs = numpy.zeros((len(self.nodes)+1,nclusters),float)
        for i in range(len(clusters)):
            for j in clusters[i]:
                if j >= 0:
                    levs[j][i] = 1
        return levs
    def aliases(self,a=None):
        """Provides a list of aliases associated with nodes and data, or sets them.
        
        Parameters:
            self : DivTree
                The tree clustering solution.
            a : tuple or list of tuples
                Optional.  Tuples should be aranged as (n,alias) where n is the
                integer identifier of the node or data point and alias is its
                string alias.
        Returns:
            a : list of tuples
                Only returned if no a is given.  List of each numerical
                identifier for data or nodes with the corresponding alias.
        """
        if a is None:
            a = []
            for i in self.nodes:
                if str(i.left) != i.leftalias:
                    a.append((i.left,i.leftalias))
                if str(i.right) != i.rightalias:
                    a.append((i.right,i.rightalias))
            a.sort()
            return a
        elif type(a) is list:
            for i in a:
                for j in self.nodes:
                    if j.left == i[0]:
                        j.leftalias = i[1]
                        break
                    if j.right == i[0]:
                        j.rightalias = i[1]
                        break
            return
        elif type(a) is tuple:
            for j in self.nodes:
                if j.left == a[0]:
                    j.leftalias = a[1]
                    break
                if j.right == a[0]:
                    j.rightalias = a[1]
                    break
            return

def divtreecluster(data=None,weights=None,dist='e',distancematrix=None):
    """Implements divisive hierarchical clustering.
    
    Parameters:
        data : ndarray
            Rank 2 array containing the data to be clustered.  Each row
            represents a single data point.  Either data or distancematrix
            should be None.
        weights : ndarray
            Optional.  If given, a rank 1 array with length equal to the number
            of columns in data.  Entries specify the weight for each dimension
            in the distance function.
        dist : string
            Specifies the desired distance function by it's alias.
        distancematrix : ndarray or list of ndarrays
            Either a rank 2 array or a list of rank 1 arrays containing the 
            distances between each data point.  In either case 
            distancematrix[i][j] is the distance between point i and point j.
            Either distancematrix or data should be None.
            If distancematrix is given then weights and dist are ignored.
    Returns:
        tree : DivTree
            The hierarchical clustering solution.
    See Also:
        stats.fulldistancematrix
    """
    raise NotImplementedError('Divisive clustering is not available yet.')
    if data is None and distancematrix is None:
        raise RuntimeError('Either data or distancematrix must be given.')
    elif not (data is None) and not (distancematrix is None):
        raise RuntimeError('Either data or distancematrix must be None.')
    elif distancematrix is None:
        distancematrix = stats.fulldistancematrix(data,weights,dist)
    elif type(distancematrix) is list:
        for i in range(len(distancematrix)):
            distancematrix[i].resize(len(distancematrix))
        distancematrix = numpy.array(distancematrix)
        distancematrix += numpy.transpose(distancematrix)
    dissat = _support.mean(distancematrix,axis=0)
    n1 = numpy.argmax(dissat)
    new = numpy.zeros_like(distancematrix)
    distancematrix = dstack((distancematrix,new))
    

def hierarchversion():
    print('hierarch/__init__.py')
    print('by R. Padraic Springuel')
    print('Created 22 January, 2008')
    print('Version %s modified %s' % (hierarchversionnum,hierarchmodified))
    print('Most recent modification by %s' % hierarchmodifier)
    return

