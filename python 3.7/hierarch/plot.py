"""Ploting routines for the visualization of hierarcical clustering.

Visualization of clustering solutions, in particular dendrograms for
hierarchical clustering.  These routines assume Pycluster was used to generate
the clustering solutions and uses matplotlib to create the graphs.

If these routines are used with interactive mode on, your program will slow
down signifigantly for large dendrograms because this program relies on
multiple calls of different matplotlib commands.  This package will work better
if you use it with interactive mode off and issue a show() command after you've
called all the routines from this package that you need.

NOTE: The documentation will alwasy describe the dendrogram as if it was 
oriented vertically.  It is possible, however, to orient the dendrogram
horizontally.  If you choose this option, then what the documentation describes
as happening vertically will happen horizontally and vis versa.

A complete version history and licence and copyright information are located
in the source code.
"""

#####################
## Version History ##
#####################

plotversionnum = '1.0'
plotmodified = '8 February, 2008'
plotmodifier = 'R. Padraic Springuel'
#Started porting functions from ClusterPlot and editing them to reference this
#package's functions instead of Pycluster.

plotversionnum = '1.1'
plotmodified = '11 February, 2008'
plotmodifier = 'R. Padraic Springuel'
#Finished porting functions from ClusterPlot.

plotversionnum = '1.2'
plotmodified = '4 June, 2009'
plotmodifier = 'R. Padraic Springuel'
#Fixed a problem with datasort when the heavy argument is specified.

plotversionnum = '1.3'
plotmodified = '22 April, 2010'
plotmodifier = 'R. Padraic Springuel'
#Fixed a problem with datasort when the heavy argument is specicied to provide
#for a default weight argument and to manage weight and pop better.

plotversionnum = '1.3.1'
plotmodified = '19 May, 2010'
plotmodifier = 'R. Padraic Springuel'
#Changed treebuild to provide special handling for legend labels.  Old behavior
#treated labels as a keyword argument to be passed to pylab.plot, which leads to
#a legend entry for each line in the dendrogram.  new behavior only passes the
#label keyword for the first line to be plotted by treebuild.

plotversionnum = '3.0.0'
plotmodified = '19 September, 2019'
plotmodifier = 'R. Padraic Springuel'
#Python 3.7 compatibility.

##########################
## Liscense Information ##
##########################

###############################################################################
#Copyright (c) 2008, R. Padraic Springuel                                     #
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

import pylab
import numpy

def datasort(tree,heavy=None,weight=None):
    """Data sorting routine to prevent branch crossings.
    
    This routine sorts the data based on the information in the cluster tree so
    that when the tree is created there are no branch crossings.  The return is
    a list of the indecies in an order that will result in no branch crossings.
    
    Parameters:
        tree : Tree
            The hierarchical clustering solution.
        heavy : string
            Optional.  Specifies which direction the cluster with the higher
            number of members should be sorted to.  Specify as 'left', 'right',
            or None.  If None, weight will be ignored.
        weight : ndarray
            Optional.  Only appropriate when not (heavy is None).  Rank 1 array
            containing weights for each data point.  I.e. the preference level
            to which that data point should go in the direction of heavy.  Used
            to selectively reorder certian branches when heavy is set.
    Returns:
        order : list
            List of data points in an order that will prevent branches from
            crossing.  Data points are identified by their integer
            identification in tree.
    """
    if not (heavy is None):
        if weight is None:
            weight = numpy.ones(len(tree)+1)
        pop = numpy.concatenate((weight,numpy.array(tree.pop)))
        for i in range(-1,-len(tree)-1,-1):
            pop[i] = pop[tree[i].left] + pop[tree[i].right]
    if heavy == 'left':
        if pop[tree[-len(tree)].left] > pop[tree[-len(tree)].right]:
            order = [tree[-len(tree)].left,tree[-len(tree)].right]
        else:
            order = [tree[-len(tree)].right,tree[-len(tree)].left]
    elif heavy == 'right':
        if pop[tree[-len(tree)].left] > pop[tree[-len(tree)].right]:
            order = [tree[-len(tree)].right,tree[-len(tree)].left]
        else:
            order = [tree[-len(tree)].left,tree[-len(tree)].right]
    else:
        order = [tree[-len(tree)].left,tree[-len(tree)].right]
    for i in range(-(len(tree)),0):
        for j in range(len(order)):
            if i == order[j]:
                if heavy == 'left':
                    if pop[tree[i].left] > pop[tree[i].right]:
                        order[j] = tree[i].right
                        order.insert(j,tree[i].left)
                    else:
                        order[j] = tree[i].left
                        order.insert(j,tree[i].right)
                elif heavy == 'right':
                    if pop[tree[i].left] > pop[tree[i].right]:
                        order[j] = tree[i].left
                        order.insert(j,tree[i].right)
                    else:
                        order[j] = tree[i].right
                        order.insert(j,tree[i].left)
                else:
                    order[j] = tree[i].right
                    order.insert(j,tree[i].left)
    return order

def coordinates(tree,zero=0,distalt=None,heavy=None,weight=None,sym=False):
    """Calculates the coordinates of each data point and cluster.
    
    Parameters:
        tree : Tree
            The hierarchical clustering solution.
        zero : float
            The height at which data points should be placed.
        distalt : ndarray or string
            Optional.  Height coordinates for the nodes.  If None is given the
            distance property of each node will set its height.  Can also be
            set to 'order' in which case each node's height will be its ordinal
            position in the tree.
        heavy : string
            Optional.  Specifies which direction the cluster with the higher
            number of members should be sorted to.  Specify as 'left', 'right',
            or None.  If None, weight will be ignored.
        weight : ndarray
            Optional.  Rank 1 array containing weights for each data point.  
            Used to selectively reorder certian branches when heavy is set.
        sym : boolean
            Sets how horizontal coordinates of nodes are calculated.  If False
            then a weighted average of child nodes' horizontal coordinates with
            weights being determined by the population of those child clusters 
            will be used.  If True then an unweighted average of the child 
            clusters horizontal coordinates will be used.  Note, if more than
            two clusters get tied together into one cluster at the same cluster
            distance this joining will not look symetric since this joining is
            made over the course of several steps.
    Returns:
        coords : list of tuples
            Each tuple contains the coordinates for its respective data point
            or node.  Data points are the first len(tree)+1 tuples and are
            indexed according to their numerical identifier in tree.  Nodes are
            the last len(tree) tuples are identified the same way, taking
            advantage of their negetive identification numbers.
    """
    coords = list(numpy.zeros(len(tree)*2+1))
    a = datasort(tree,heavy,weight)
    for i in range(len(a)):
        coords[a[i]] = (float(i),zero)
    for i in range(-len(tree),0)[::-1]:
        if distalt is None:
            y = tree[i].distance
        elif distalt == 'order':
            y = abs(i)
        else:
            y = distalt[i]
        if not sym:
            if tree[i].right >= 0:
                right = 1
            else:
                right = tree.pop[tree[i].right]
            if tree[i].left >= 0:
                left = 1
            else:
                left = tree.pop[tree[i].left]
            x = (right*coords[tree[i].right][0]+left*coords[tree[i].left][0])/(left+right)
        else:
            x = (coords[tree[i].right][0]+coords[tree[i].left][0])/2
        coords[i] = (x,y)
    return coords

def treebuild(coords,tree,unmask=None,orient='v',invert=False,line='b-',p=0.95,label=None,**kwargs):
    """Construct the dendrogram.
    
    Parameters:
        coords : list of tuples
            Each tuple contains the coordinates for its respective data point
            or node.  Data points are the first len(tree)+1 tuples and are
            indexed according to their numerical identifier in tree.  Nodes are
            the last len(tree) tuples are identified the same way, taking
            advantage of their negetive identification numbers.
        tree : Tree
            The hierarchical clustering solution.
        unmask : ndarray
            Rank 1 array of boolean values.  Should have length len(tree)*2+1
            with the first len(tree)+1 values cooresponding to the data points
            and the last len(tree) values corresponding to the nodes.  For each
            value: if True that data point/node will be plotted; if False that
            data point/node will not be plotted.  Connections are only drawn if
            both ends are plotted.
        orient : character
            Specifies whether the tree should be oriented vertically ('v',
            default) or horizontally ('h').  If horizontal, map top into left
            and bottom into right in the behavior of the remaining arguments.
        invert : boolean
            Specifies whether the data should be at the bottom of the 
            dendrogram (False, default) or at the top (True).
        line : string
            String specifying what type of line should be used to make the
            the connections in the dendrogram.
        p : float
            The portion of the vertical space that the tree will take up.  The
            remainder is split 3:1 above and below the tree.  Setting p to be 
            something below 1 ensures that the entire vertical extent of tree
            will be visible.
        label : string
            The legend label that is to be assigned to the tree.  While this is
            a normal keyword argument for pylab.plot, it is necessary to provide
            special handling for it so that a tree gets only one such label.
        **kwargs : multiple types
            Other arguments used to control the behavior of the pylab.plot
            command.
    Output:
        If matplotlib is in interactive mode, then the dendrogram will appear
        in the plot window one connection at a time.  If interactive mode is
        off then a pylab.show() command after the completion of this function
        will cause the whole dendrogram to be shown in the plot window all at
        once.  Note: this function runs very slow in interactive mode.
    See Also:
        matplotlib online documenation for line and **kwargs options.
    """
    from numpy import array
    if unmask is None:
        unmask = numpy.ones(len(coords),bool)
    pylab.hold(True)
    first = True
    for i in range(-len(tree),0):
        if unmask[i] and unmask[tree[i].left]:
            if orient == 'v':
                x = [coords[i][0],coords[tree[i].left][0],coords[tree[i].left][0]]
                y = [coords[i][1],coords[i][1],coords[tree[i].left][1]]
            elif orient == 'h':
                y = [coords[i][0],coords[tree[i].left][0],coords[tree[i].left][0]]
                x = [coords[i][1],coords[i][1],coords[tree[i].left][1]]
            else:
                print('Invalid orientation.')
                return
            if not (label is None) and first:
                pylab.plot(x,y,line,label=label,**kwargs)
                first = False
            else:
                pylab.plot(x,y,line,**kwargs)            
        if unmask[i] and unmask[tree[i].right]:
            if orient == 'v':
                x = [coords[i][0],coords[tree[i].right][0],coords[tree[i].right][0]]
                y = [coords[i][1],coords[i][1],coords[tree[i].right][1]]
            elif orient == 'h':
                y = [coords[i][0],coords[tree[i].right][0],coords[tree[i].right][0]]
                x = [coords[i][1],coords[i][1],coords[tree[i].right][1]]
            if not (label is None) and first:
                pylab.plot(x,y,line,label=label,**kwargs)
                first = False
            else:
                pylab.plot(x,y,line,**kwargs)            
    if orient == 'v':
        pylab.xlim(-1,len(tree)+2)
        ymin = coords[0][1]
        ymax = coords[0][1]
        for i in range(len(coords)):
            if coords[i][1] < ymin:
                ymin = coords[i][1]
            elif coords[i][1] > ymax:
                ymax = coords[i][1]
        if invert:
            pylab.ylim(ymax+(ymax-ymin)*(1.-p)*3/4,ymin-((ymax-ymin)*(1.-p)/4))
        else:
            pylab.ylim(ymin-((ymax-ymin)*(1.-p)/4),ymax+(ymax-ymin)*(1.-p)*3/4)
    elif orient == 'h':
        pylab.ylim(-1,len(tree)+2)
        xmin = coords[0][1]
        xmax = coords[0][1]
        for i in range(len(coords)):
            if coords[i][1] < xmin:
                xmin = coords[i][1]
            elif coords[i][1] > xmax:
                xmax = coords[i][1]
        if invert:
            pylab.xlim(xmax+(xmax-xmin)*(1.-p)*3/4,xmin-((xmax-xmin)*(1.-p)/4))
        else:
            pylab.xlim(xmin-((xmax-xmin)*(1.-p)/4),xmax+(xmax-xmin)*(1.-p)*3/4)
    return

def clusterlabels(coords,labels,unmask=None,fontdict=None,**kwargs):
    """Labels each cluster with the specified string.
    
    Parameters:
        coords : list of tuples
            Each tuple contains the coordinates for its respective data point
            or node.  Data points are the first len(tree)+1 tuples and are
            indexed according to their numerical identifier in tree.  Nodes are
            the last len(tree) tuples are identified the same way, taking
            advantage of their negetive identification numbers.
        labels : list of strings
            The label to be applied to each coordinate.
        unmask : ndarray
            Rank 1 array of boolean values.  For each value: if True the
            corresponding label will be plotted; if False the corresponding
            label will not be plotted.
        fontdict : dictionary
            Dictionary to specify the appearence of the labels.
        **kwargs : multiple types
            Other arguments used to specify the behavior of the pylab.text()
            command.
    Output:
        If matplotlib is in interactive mode the labels will appear in the plot
        window one at a time.  If interactive mode is off, they are added to
        the current figure instance and can be seen with a pylab.show() command.
    See Also:
        matplotlib online documentation for fontdict and **kwargs options.
    """
    if unmask is None:
        unmask = numpy.ones(len(coords),bool)
    for i in range(len(coords)):
        if unmask[i]:
            pylab.text(coords[i][0],coords[i][1],labels[i],fontdict=fontdict,**kwargs)
    return

def datalabels(tree,dlabels,heavy=None,weight=None,unmask=None,orient='v',fontdict=None,**kwargs):
    """Labels just the data points using tick marks on the plot.
    
    Parameters:
        tree : Tree
            The hierarchical clustering solution.
        dlabels : list of strings
            The labels for each data point.
        heavy : string
            Optional.  Specifies which direction the cluster with the higher
            number of members should be sorted to.  Specify as 'left', 'right',
            or None.  If None, weight will be ignored.
        weight : ndarray
            Optional.  Rank 1 array containing weights for each data point.  
            Used to selectively reorder certian branches when heavy is set.
        unmask : ndarray
            Rank 1 array of boolean values.  For each value: if True the
            corresponding data label will be plotted; if False the 
            corresponding data label will not be plotted.
        orient : character
            Specifies whether the tree should be oriented vertically ('v',
            default) or horizontally ('h').  If horizontal, map top into left
            and bottom into right in the behavior of the remaining arguments.
        fontdict : dictionary
            Dictionary to specify the appearence of the labels.
        **kwargs : multiple types
            Other arguments used to specify the behavior of the pylab.xticks()
            or pylab.yticks() command.
    Output:
        The labels will be added to the current plot instance as tick marks.
        If matplotlib is in interactive mode you will be able to see this
        immediately.  Otherwise it will not be visible until a pylab.show()
        command is issued.
    """
    if unmask is None:
        unmask = numpy.ones(len(dlabels),bool)
    a = datasort(tree,heavy,weight)
    dl = []
    for i in range(len(dlabels)):
        if unmask[i]:
            dl.append(dlabels[a[i]])
        else:
            dl.append('')
    if orient == 'v':
        pylab.xticks(list(range(len(dlabels))),dl,fontdict=fontdict,**kwargs)
    if orient == 'h':
        pylab.yticks(list(range(len(dlabels))),dl,fontdict=fontdict,**kwargs)
    return

#######################
## Wrapper Functions ##
#######################

#The wrapper functions below allow the quick creation of dendrograms.  They do
#that, however, by limiting the options avaliable to manipulate the appearence
#of the dendrogram.  For full control over the appearence of the dendrogram,
#the above functions should be used independantly.

#To minimize conflicts, the color of the lines in the tree cannot be specified
#with a matplotlib keyword argument but must instead be specified with the
#specific color argument.  The keyword arguments are reserved for text
#text properties for the labels.


def wholetree(tree,dlabels=None,heavy=None,weight=None,line='b-',sym=False,p=0.95,fontdict=None,**kwargs):
    """Creates the whole tree and places the data labels if they are provided.
    
    Parameters:
        tree : Tree
            The hierarchical clustering solution.
        dlabels : list of strings
            The labels for each data point.
        heavy : string
            Optional.  Specifies which direction the cluster with the higher
            number of members should be sorted to.  Specify as 'left', 'right',
            or None.  If None, weight will be ignored.
        weight : ndarray
            Optional.  Rank 1 array containing weights for each data point.  
            Used to selectively reorder certian branches when heavy is set.
        line : string
            String specifying what type of line should be used to make the
            the connections in the dendrogram.
        sym : boolean
            Sets how horizontal coordinates of nodes are calculated.  If False
            then a weighted average of child nodes' horizontal coordinates with
            weights being determined by the population of those child clusters 
            will be used.  If True then an unweighted average of the child 
            clusters horizontal coordinates will be used.  Note, if more than
            two clusters get tied together into one cluster at the same cluster
            distance this joining will not look symetric since this joining is
            made over the course of several steps.
        p : float
            The portion of the vertical space that the tree will take up.  The
            remainder is split 3:1 above and below the tree.  Setting p to be 
            something below 1 ensures that the entire vertical extent of tree
            will be visible.
        fontdict : dictionary
            Dictionary to specify the appearence of the labels.
        **kwargs : multiple types
            Other arguments used to specify the behavior of the pylab.text()
            command.
    Output:
        The dendrogram will be created in the current plot instance.  If
        interactive mode is on it will appear once piece at a time in the
        plot window.  If it is off then it can be made to appear with a
        pylab.show() command.
    """
    coords = coordinates(tree,0,None,heavy,weight,sym)
    treebuild(coords,tree,None,'v',False,line,p)
    if not (dlabels is None):
        datalabels(tree,dlabels,heavy,weight,'v',fontdict=fontdict,**kwargs)
    return

    
def poptree(tree,heavy=None,weight=None,line='b-',sym=False,p=0.95,lowerlimit=1,fontdict=None,**kwargs):
    """A dendrogram where each cluster is labeled by its population.
    
    Parameters:
        tree : Tree
            The hierarchical clustering solution.
        heavy : string
            Optional.  Specifies which direction the cluster with the higher
            number of members should be sorted to.  Specify as 'left', 'right',
            or None.  If None, weight will be ignored.
        weight : ndarray
            Optional.  Rank 1 array containing weights for each data point.  
            Used to selectively reorder certian branches when heavy is set.
        line : string
            String specifying what type of line should be used to make the
            the connections in the dendrogram.
        sym : boolean
            Sets how horizontal coordinates of nodes are calculated.  If False
            then a weighted average of child nodes' horizontal coordinates with
            weights being determined by the population of those child clusters 
            will be used.  If True then an unweighted average of the child 
            clusters horizontal coordinates will be used.  Note, if more than
            two clusters get tied together into one cluster at the same cluster
            distance this joining will not look symetric since this joining is
            made over the course of several steps.
        p : float
            The portion of the vertical space that the tree will take up.  The
            remainder is split 3:1 above and below the tree.  Setting p to be 
            something below 1 ensures that the entire vertical extent of tree
            will be visible.
        lowerlimit : float
            Sets the maximum size of the clusters that are plotted.  Identical 
            data points (i.e. those with 0 joining distance) are always hidden.
        fontdict : dictionary
            Dictionary to specify the appearence of the labels.
        **kwargs : multiple types
            Other arguments used to specify the behavior of the pylab.text()
            command.
    Output:
        The dendrogram will be created in the current plot instance.  If
        interactive mode is on it will appear once piece at a time in the
        plot window.  If it is off then it can be made to appear with a
        pylab.show() command.
    """ 
    if weight is None:
        pop = tree.pop
    else:
        pop = tree.pop*weight
    unmask = numpy.ones(len(pop),bool)
    labels = [1]*(len(pop)+1)
    for i in range(len(pop)):
        if pop[i] < lowerlimit:
            unmask[i] = False
        labels.append(str(pop[i]))
    unmask = numpy.append(numpy.zeros(len(pop)+1,bool),unmask)        
    for i in range(len(tree)):
        if tree[i].distance == 0:
            unmask[tree[i].right] = False
            unmask[tree[i].left] = False
    coords = coordinates(tree,0,None,heavy,weight,sym)
    treebuild(coords,tree,unmask,'v',False,line,p)
    clusterlabels(coords,labels,unmask,fontdict=fontdict,**kwargs)
    return

def fadetree(tree,heavy=None,weight=None,line='b-',sym=False,p=0.95,fontdict=None,**kwargs):
    """Creates a dendrogram where branches fade out as they become less populated.
    
    Parameters:
        tree : Tree
            The hierarchical clustering solution.
        heavy : string
            Optional.  Specifies which direction the cluster with the higher
            number of members should be sorted to.  Specify as 'left', 'right',
            or None.  If None, weight will be ignored.
        weight : ndarray
            Optional.  Rank 1 array containing weights for each data point.  
            Used to selectively reorder certian branches when heavy is set.
        line : string
            String specifying what type of line should be used to make the
            the connections in the dendrogram.
        sym : boolean
            Sets how horizontal coordinates of nodes are calculated.  If False
            then a weighted average of child nodes' horizontal coordinates with
            weights being determined by the population of those child clusters 
            will be used.  If True then an unweighted average of the child 
            clusters horizontal coordinates will be used.  Note, if more than
            two clusters get tied together into one cluster at the same cluster
            distance this joining will not look symetric since this joining is
            made over the course of several steps.
        p : float
            The portion of the vertical space that the tree will take up.  The
            remainder is split 3:1 above and below the tree.  Setting p to be 
            something below 1 ensures that the entire vertical extent of tree
            will be visible.
        fontdict : dictionary
            Dictionary to specify the appearence of the labels.
        **kwargs : multiple types
            Other arguments used to specify the behavior of the pylab.text()
            command.
    Output:
        The dendrogram will be created in the current plot instance.  If
        interactive mode is on it will appear once piece at a time in the
        plot window.  If it is off then it can be made to appear with a
        pylab.show() command.
    """
    if weight is None:
        pop = tree.pop
    else:
        pop = tree.pop*weight
    coords = coordinates(tree,0,None,heavy,weight,sym)
    unmask1 = numpy.zeros(len(pop),bool)
    unmask2 = numpy.zeros(len(pop),bool)
    unmask3 = numpy.zeros(len(pop),bool)
    unmask4 = numpy.zeros(len(pop),bool)
    unmask5 = numpy.zeros(len(pop),bool)
    unmask6 = numpy.zeros(len(pop),bool)
    unmask7 = numpy.zeros(len(pop),bool)
    unmask8 = numpy.zeros(len(pop),bool)
    unmask9 = numpy.zeros(len(pop),bool)
    unmask0 = numpy.zeros(len(pop),bool)
    for i in range(len(pop)):
        if float(pop[i])/max(pop) < 0.1:
            unmask1[i] = True
        elif float(pop[i])/max(pop) < 0.2:
            unmask2[i] = True
        elif float(pop[i])/max(pop) < 0.3:
            unmask3[i] = True
        elif float(pop[i])/max(pop) < 0.4:
            unmask4[i] = True
        elif float(pop[i])/max(pop) < 0.5:
            unmask5[i] = True
        elif float(pop[i])/max(pop) < 0.6:
            unmask6[i] = True
        elif float(pop[i])/max(pop) < 0.7:
            unmask7[i] = True
        elif float(pop[i])/max(pop) < 0.8:
            unmask8[i] = True
        elif float(pop[i])/max(pop) < 0.9:
            unmask9[i] = True
        else:
            unmask0[i] = True
    for i in range(-len(tree),0):
        if unmask1[tree[i].left] or unmask1[tree[i].right]:
            unmask1[i] = True
        if unmask2[tree[i].left] or unmask2[tree[i].right]:
            unmask2[i] = True
        if unmask3[tree[i].left] or unmask3[tree[i].right]:
            unmask3[i] = True
        if unmask4[tree[i].left] or unmask4[tree[i].right]:
            unmask4[i] = True
        if unmask5[tree[i].left] or unmask5[tree[i].right]:
            unmask5[i] = True
        if unmask6[tree[i].left] or unmask6[tree[i].right]:
            unmask6[i] = True
        if unmask7[tree[i].left] or unmask7[tree[i].right]:
            unmask7[i] = True
        if unmask8[tree[i].left] or unmask8[tree[i].right]:
            unmask8[i] = True
        if unmask9[tree[i].left] or unmask9[tree[i].right]:
            unmask9[i] = True
        if unmask0[tree[i].left] or unmask0[tree[i].right]:
            unmask0[i] = True
    treebuild(coords,tree,unmask1,'v',False,line,p,alpha=0.1)
    treebuild(coords,tree,unmask2,'v',False,line,p,alpha=0.2)
    treebuild(coords,tree,unmask3,'v',False,line,p,alpha=0.3)
    treebuild(coords,tree,unmask4,'v',False,line,p,alpha=0.4)
    treebuild(coords,tree,unmask5,'v',False,line,p,alpha=0.5)
    treebuild(coords,tree,unmask6,'v',False,line,p,alpha=0.6)
    treebuild(coords,tree,unmask7,'v',False,line,p,alpha=0.7)
    treebuild(coords,tree,unmask8,'v',False,line,p,alpha=0.8)
    treebuild(coords,tree,unmask9,'v',False,line,p,alpha=0.9)
    treebuild(coords,tree,unmask0,'v',False,line,p,alpha=1.0)
    return


def plotversion():
    print('plot.py')
    print('Created 08 February, 2008')
    print('by R. Padraic Springuel')
    print('Version %s modified %s' % (plotversionnum,plotmodified))
    print('Most recent modification by %s' % plotmodifier)
    return

