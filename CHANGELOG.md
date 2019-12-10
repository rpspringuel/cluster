# CHANGELOG
This is the CHANGELOG.md for the cluster project.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Prior to v3.0.0 changes were logged individually in each file with each file
having its own version number as well.  This was a legacy of the fact that some
pieces were originally developed individually and without the use of version
control software.  All those individual version numbers are integrated into this
change log and sorted by date, leading to numbers that repeat or are apparently
out of order.  Which file was modified is thus appended to the version number
for those eary version numbers.

## [Unreleased]

## [3.0.0] - 2019-12-10
### Fixed
-The Minkowski distances were doing integer division in the exponent, leading to
 the distances of 2nd order and higher always being evaluated with an exponent
 of 0 (and thus forcing the distance to 1.0).  Forcing the exponent to use
 float division (by wrapping the `p` parameter in `float`) fixes it.

### Added
-Python 3.7 Compatibility

### Removed
-As part of the rationalization of the version number, the individual version
 functions have been removed from each file.
-Legacy functions are removed from the Python 3.7 files.


## [2.0.0 - test/__init__.py] - 2019-10-22
### Changed
-Update all tests to work with Python 2.7.16, numpy 1.16.4, cPickle 1.17

## [2.5.3 - hierarch/__init__.py] - 2010-08-13
### Added
-WPGMA linkage method to aggtreecluster.

## [1.1.1 - test/__init__.py] - 2010-08-11
### Removed
-Modal links on centroids require too much time to test with a random test data
 set.  Those tests have been removed until a test data set that can be processed
 in a reasonable time is developed.

## [1.1 - test/__init__.py] - 2010-07-28
### Changed
-Adapted hierarch tests to accomodate new centroid based functionality.

## [2.5.2 - hierarch/__init__.py] - 2010-07-26
### Fixed
-Speed up in aggtreecluster for centroid links by reducing number of distances
 calculated.  Now distances to current clusters are the only ones calculated,
 rather than to all clusters.  This behavior is different from what the other
 links are doing, but necessary because centroid links have to calculate each
 distance seperately while the other use numpy column and row operations to
 calculate all distances simultaneously.

## [2.5.1 - hierarch/__init__.py] - 2010-07-26
### Fixed
-in aggtreecluster centroid methods: dec needed to be an array in order for
 indexing methods to work properly, it had previously been a list

## [2.5 - hierarch/__init__.py] - 2010-07-25
### Added
-mode based centroids support.

## [1.0.1 - test/__init__.py] - 2010-07-25
### Fixed
-Bugfix in warning about plot functions (argument order was incorrect).

## [2.4.5 - hierarch/__init__.py] - 2010-07-24
### Changed
-Modification to aggtreecluster for faster medoid calculations.

## [2.0.4 - partition.py] - 2010-07-09
#### Fixed
-in cmeans_noise

## [2.4.4 - hierarch/__init__.py] - 2010-07-09
### Fixed
- Bugfix in AggTree.aliases.

### Changed
-Removed alias flag in AggTree.ancestors and AggTree.decendants.

## [1 - test/__init__.py] - 2010-07-09
### Added
-Finished partition tests.  The only functions not tested now are those with
 picture returns.  Those will require different testing procedures which I don't
 know how to do yet.

## [2.0.3 - partition.py] - 2010-07-02
### Fixed
-in cmeans_noise.

## [0.8 - test/__init__.py] - 2010-07-02
### Added
-Finished hierach tests for functions which don't have picture returns.

## [1.8.1 - distances.py] - 2010-06-25
### Fixed
-in distance.

## [2.4.3 - hierarch/__init__.py] - 2010-06-25
### Fixed
-Documentation noted that centroid linkage for aggtreecluster cannot handle
 multivalued modes.

## [0.0 - _support.py] - 2010-06-25
### Added
Initial creation date.

## [2.3.2 - stats.py] - 2010-06-25
### Changed
-Removed Statisitcs dependencies.

## [2.0.2 - partition.py] - 2010-06-25
### Changed
-Removed Statistics dependencies.

## [2.4.3 - hierarch/__init__.py] - 2010-06-25
### Changed
-Removal of Statistics dependancies.

## [0.7 - test/__init__.py] - 2010-06-25
### Added
-Added script functionality to module.

## [2.4.2 - hierarch/__init__.py] - 2010-06-22
### Fixed
-Bugfix in append method related to new type abilities.

### Changed
-Modification to cophenetic method to allow it to compute multiple kinds of
 cophenetic distances.

## [1.3.4] - 2010-06-21
### Changed
-Module exceptions moved to top level

## [2.0.1 - partition.py] - 2010-06-21
### Changed
-Updated error statements.

## [2.3.1 - stats.py] - 2010-06-21
### Changed
-Updated error statements.

## [2.4.1 - hierarch/__init__.py] - 2010-06-21
### Changed
-More error handling updates.
-Updated class definitions to use newstyle so that type() works the way I want
 it to on my classes.

## [1.8 - distances.py] - 2010-06-18
### Changed
-Updated error handling and added warnings.

## [2.4 - hierarch/__init__.py] - 2010-06-18
### Changed
-Updated error handling.
-modified Ward's method to provide an example of its use.

### Added
-dynamic Lance-Williams manipulation

## [0.6 - test/__init__.py] - 2010-06-18
### Added
-Finished writing stats tests.

## [2.3.1 - hierarch/__init__.py] - 2010-06-16
### Added
-Added 5th tie-breaking algorigthm.

### Fixed
-Bug fixing in how aggtreecluster handles provided distancematrixes.

## [2.3 - hierarch/__init__.py] - 2010-06-16
### Added
-expand tie-breaking algorithms in aggtreecluster.  4 mechanisms are now
 provided: None (ties are resolved based on the age based search order), random
 (ties are resolved randomly), aggr (ties are resolved to create the largest new
 group possible), and doc (ties are resolved to create the smallest new group
 possible)

## [0.5 - test/__init__.py] - 2010-06-11
### Added
-Wrote some stats and hierarch tests.

## [2.2 - hierarch/__init__.py] - 2010-06-04
### Changed
-Slight tweak to AggTree.scale to reduce number of function evaluations
 (formerly min(distances) and max(distances) had to be evaluted each time
 through the loop).
-Modification of aggtreecluster to increase speed of search algorithm.  New
 algorithm realizes ~7-8 fold increase in speed by extracting only the lower
 half of search from distance matrix and making it a flat array.  This allows
 the use of numpy.nanmin(search) to find the minimum, a simple boolean test to
 find all occurances of that minimum, and a single loop over search which only
 needs to do something when the boolean test is true.

## [2.1 - hierarch/__init__.py] - 2010-05-30
### Added
-Added __eq__ methods for AggNode and AggTree.  This allows for basic
 equivalence testing of trees.
-Added assigned list for AggTree.  This lists all nodes which have been joined
 together to create a cluster and allowed the elimination of an explicit loop in
 the __init__ method for AggTree through use of an "in" statement.
 
### Changed
-Reworte append method for AggTree so that it no longer uses the __init__
 method.  This should make the method much faster on large trees.

## [1.7 - distances.py] - 2010-05-28
### Fixed
-Bug fix in Minkowski.

## [2.3 - stats.py] - 2010-05-28
### Added
-Added deprecation warnings.

## [0.4 - test/__init__.py] - 2010-05-28
### Added
-Legacy tests written.

## [2.2 - stats.py] - 2010-05-27
### Changed
-Finished rewriting and testing fuzzy_silhouette.  Renamed silhouette to
 old_silhouette, restored its use of clusterid, and labeled it a legacy
 function.  Renamed fuzzy_silhouette to silhouette.

## [2.1.2 - stats.py] - 2010-05-26
### Changed
-More rewriting of fuzzy_silhouette.  Preliminary tests show silhouette and
 fuzzy_silhouette disagreeing.  Need to figure out why.

## [2.1.1 - stats.py] - 2010-05-25
### Changed
-Rewriting fuzzy_silhouette based on some precieved problems in the original
 ideas.  Came up with a better idea for calculating a, but still need to come up
 with an equivalent idea for calculating b.

## [2.1 - stats.py] - 2010-05-23
### Fixed
-fix inappropirate use of weight in silhouette

### Changed
-Modified levscheck to include a test for values greater than 1 or less than 0
 and made the rounding percision a user accessible variable.
-Renamed levels to clusterid_to_levs and created levs_to_clusterid.
-Modified silhouette to make its inputs conform to the preference for levs over
 clusterid

### Added
-First pass at writing fuzzy_silhouette.

## [0.3 - test/__init__.py] - 2010-05-23
### Added
-Made a separate test function for legacy functions.

### Changed
-Modifications to use numpy.allclose instead of ==.

## [1.3.1 - hierarch/plot.py] - 2010-05-19
### Changed
-Changed treebuild to provide special handling for legend labels.  Old behavior
 treated labels as a keyword argument to be passed to pylab.plot, which leads to
 a legend entry for each line in the dendrogram.  new behavior only passes the
 label keyword for the first line to be plotted by treebuild.

## [1.3.3 - __init__.py] - 2010-05-06
### Changed
-Modification to test interface for legacy functions.  Legacy functions are not
 tested by default but the new option allows for them to be tested if desired.

## [1.3.2 - __init__.py] - 2010-05-06
### Added
-New functionality in test

## [0.2 - test/__init__.py] - 2010-05-06
### Changed
-Revising file structure to add functionality to test functions.

## [1.3.1 - __init__.py] - 2010-04-27
### Fixed
-minor bug in clusterversion

### Added
-test function.

## [0.1 - test/__init__.py] - 2010-04-27
### Added
-Initial version.  Mostly creating file structure.

## [1.3 - hierarch/plot.py] - 2010-04-22
### Fixed
-Fixed a problem with datasort when the heavy argument is specicied to provide
 for a default weight argument and to manage weight and pop better.

## [1.2 - hierarch/plot.py] - 2009-06-04
### Fixed
-Fixed a problem with datasort when the heavy argument is specified.

## [2 - partition.py] - 2009-06-02
### Removed
-Eliminated transpose argument from functions.  This behavior can be duplicated
 by use of numpy's transpose function on arguments and the results.

## [2 - hierarch/__init__.py] - 2009-06-02
### Removed
-Eliminated transpose argument from functions.  This behavior can be duplicated
 by use of numpy's transpose function on arguments and the results.

## [2 - stats.py] - 2009-06-02
### Removed
-Eliminated transpose argument from functions.  This behavior can be duplicated
 by use of numpy's transpose function on arguments and the results.  The
 follwoing functions were not updated because they are considered legacy:
 old_singleclustercentroid, old_clustercentroids, old_SSE, SSE, point_SSE

## [1.8.3 - hierarch/__init__.py] - 2009-05-28
### Added
-Passed aggtreecluster's verbose argument to fulldistancematrix.

## [1.8.2 - hierarch/__init__.py] - 2009-05-18
### Fixed
-Documentation typos fixed.

### Removed
-Eliminated 'te' option which is no longer supported in distances from
 aggtreecluster.

## [1.15 - stats.py] - 2009-03-28
### Added
-Added verbose option to distancematrix and fulldistancematrix.

## [1.8.1 - hierarch/__init__.py] - 2009-03-12
### Fixed
-Corrected an indentation error that made aggtreecluster only work when verbose
 was true.

## [1.14 - stats.py] - 2009-03-06
### Fixed
-Updated to handle the new axis functioning of _support.mode.

## [1.13.1 - stats.py] - 2009-03-04
### Added
-Modified SEmatirx to handle multi-modal centroids.

## [1.8 - hierarch/__init__.py] - 2009-03-02
### Changed
-Changed "method" variable in aggtreecluster to "link" to avoid naming conflicts
 with the "method" variable in the stats algorithms where it refers to how a
 cetroid is found.  This helps to maintain consistency in naming throughout the
 package.

## [1.13 - stats.py] - 2009-02-27
### Added
-Added mode to the list of available measures of central tendancy for
 singleclustercentroid.  This required some rewrite of clustercentroids and
 still requires some reworking of SEmatrix.

## [1.12 - stats.py] - 2009-02-25
### Added
-Wrote SEmatrix.

## [1.7 - hierarch/__init__.py] - 2009-02-24
### Added
-Added save method to AggTree and wrote loadaggtree to allow for saving and
 loading of an agglomeratice tree clustering solution.  This enables the user to
 vary the post processing of a solution without having to rerun the clustering
 each time.

## [1.11 - stats.py] - 2009-02-20
### Changed
-Changed singleclustercentroid and clustercentroids to allow for the passing of
 the distance matrix to them when using medoid methods rather than forcing a
 recalculation of it.

## [1.6.5 - hierarch/__init__.py] - 2009-02-20
### Fixed
-Changed a 'continue' to 'break' in the distance matrix search algorithm.  This
 increases the speed of the search because now the fact that the matrix is
 symmetric about its main diaganol is being exploited to limit the search to
 only the lower half.

## [1.6 - distances.py] - 2009-02-12
### Added
-Added sqeuclidian so that I can avoid having to change the source code when
 trying to replicate older work that used this distance.

## [1.5.2 - distances.py] - 2009-02-13
### Fixed
-Changed occuranes of 'a*0+...', 'b*0+...', and 'a*b*0+...' to
 '~numpy.isnan(a)*...', '~numpy.isnan(b)*...', and
 '~numpy.isnan(a)*~numpy.isnan(b)*...' respectively.  While textually longer it
 is more conceptually what is meant to be accomplished (i.e. the removal of nan
 values from the math) and has the advantage of not getting confused by inf
 values in the data set.

## [1.5.1 - distances.py] - 2009-02-12
### Fixed
-Bug fix in jaccard.  It wasn't calculating the distance correctly for
 non-binary data.  Also corrected some of it's handling of nan (i.e. missing
 data.

## [1.6.4 - hierarch/__init__.py] - 2009-02-05
### Added
-Added verbose option to aggtreecluster.

## [1.6.3 - hierarch/__init__.py] - 2009-02-02
### Fixed
-Reworked search algorithm for the minimum value of the distance matrix. 
 Instead of manually assigning a "upperlimit" to values that should not be
 checked, and then simply looking for the minimum value, the search algorithm is
 now more intelligent and doesn't look at the values that should not be checked. 
 The disadvantage is that the loop is now in python.

## [1.5 - distances.py] - 2008-09-24
### Fixed
-Fixed computation of kendall distance.

### Changed
-Modified all distance functions to yield normalized distances.  This
 consolidated some distance functions which had both a normalized and a
 nonnormalized version (peuclidian/euclidian, pcityblock/cityblock).

## [1.2 - partition.py] - 2008-04-08
### Added
-Added cmeans_noise.

## [1.6.2 - hierarch/__init__.py] - 2008-04-01
### Added
-Header for divtreecluster created.  Started some work but ran into a problem I
 hadn't considered before.  Until all members of the splinter group are known, I
 need to hang onto the current form of the distance matrix.  Need to figure out
 how to handle that before going any further.

## [1.4.1 - distances.py] - 2008-03-11
### Fixed
-Fixed spelling of function name 'jaccard'.

## [1.6.1 - hierarch/__init__.py] - 2008-03-11
### Fixed
-Bug fix: The way the tie breaking rule in aggtreecluster was being implemented
 led to n1 and n2 not being reassigned negative values when appropriate when no
 tie breaking condition was set (i.e. aggr is None).  Fixed this by adding an
 else statement to the if not (aggr is None) clause.

## [1.1.1 - partition.py] - 2008-03-11
### Fixed
-Fixed bug in cmeans that made it incapable of handling initial=None when p==1.
-Fixed bug in cmeans that resulted from the changing of for loops to function
 calls.

## [1.6 - hierarch/__init__.py] - 2008-03-07
### Added
-Defined DivTree class.

## [1.5 - hierarch/__init__.py] - 2008-03-06
### Changed
-In thinking about implementing a divisive hierarchical clustering scheme, I
 realized that there was an incompatibility between how the Node and Tree
 classes worked and how the divisive hierarchical clustering scheme would be
 implemented.  This led to a renaming of Node, Tree, and treecluster to AggNode,
 AggTree, and aggtreecluster respectively to specify that they were for
 agglomerative hierarchical clustering specifically.  The version history below
 has been modified to use these new names for clarity's sake. 

### Added
-Defined the DivNode class.

## [1.1.4 - hierarch/__init__.py] - 2008-03-05
### Added
-Added a tie breaking rule based on the new cluster size to aggtreecluster and
 the ability to control how that tie breaking rule is implemented.

## [1.4 - distances.py] - 2008-02-25
### Fixed
-Documentation revisions.

### Added
-Added minkowski and chebychev.

## [1.3 - distances.py] - 2008-02-22
### Fixed
-Fixed several documentation typos.

### Added
-Added rogerstanimoto, sokalsneathsym, jaccard, dice, & sokalsneathasym.

## [1.1.3 - hierarch/__init__.py] - 2008-02-21
### Added
-Implemented the use of the Lance-Williams formula in aggtreecluster.  Since
 said formula isn't valid for all possible methods of calculating the centroid,
 the old centroid link code still exists for handling those cases.  Adding the
 use of the Lance-Williams update forumla also allowed the addition of four new
 links: Ward's, Gower's, flexible, and a direct manipulation of all
 Lance-Williams coefficients.

## [1.1.2 - hierarch/__init__.py] - 2008-02-20
### Added
-Started looking into using the lance-williams formula for calculating cluster
 proximity.  Plan to implement this after doing some more research on what the
 coeficcients are for different methods.  This will unify the distance matrix
 update step of aggtreecluster.

## [1.1.1 - hierarch/__init__.py] - 2008-02-18
### Fixed
-Debugging AggTree.ancestors.

## [1.3 - __init__.py] - 2008-02-11
### Added
-hierarch.plot import statement.

## [1.1 - hierarch/plot.py] - 2008-02-11
### Added
-Finished porting functions from ClusterPlot.

## [1.0 - hierarch/plot.py] - 2008-02-08
### Added
-Started porting functions from ClusterPlot and editing them to reference this
 package's functions instead of Pycluster.

## [1.1 - hierarch/__init__.py] - 2008-02-07
### Added
-Added ancestors and aliases methods to AggTree class.

### Fixed
-Modified decendants method to allow for aliases to be returned if desired.

## [1.2 - __init__.py] - 2008-02-06
### Added
- hierarch import statement.

## [1.10.1 - stats.py] - 2008-02-06
### Fixed
-Documentation revisions.

## [1 - hierarch/__init__.py] - 2008-02-06
### Changed
-Finished aggtreecluster.

### Added
-Added pop property and decendants method to AggTree class.

## [0.2 - hierarch/__init__.py] - 2008-02-05
### Added
-Finished defining AggTree class.
-Started work on aggtreecluster.

## [0.1 - hierarch/__init__.py] - 2008-02-04
### Added
-Added string aliasing to AggNode class.
-Continued defining AggTree class.

## [0 - hierarch/__init__.py] - 2008-02-01
### Added
-Initial creation date.
-Defined AggNode class.
-Started defining AggTree class.

## [1.10 - stats.py] - 2008-01-31
### Added
-Wrote levscompare.

## [1.1 - partition.py] - 2008-01-30
### Changed
-Changed some for loops to a numpy.apply_along_axis call instead.

## [1 - partition.py] - 2008-01-28
### Fixed
-kmeans documentation revision.

### Added
-Wrote cmeans.

## [1.9 - stats.py] - 2008-01-28
### Added
-Added point_SSE and debugged SSE.

## [1.2.5 - distances.py] - 2008-01-25
### Fixed
-Typo in documentation.

## [0.1.1 - partition.py] - 2008-01-25
### Fixed
-Debugging kmeans.

## [1.1 - __init__.py] - 2008-01-24
### Added
-partition import statement.

## [0.1 - partition.py] - 2008-01-24
### Changed
-Modified kmeans to inculde a check for empty clusters after assignment and to
 correct for it when present.

## [1.8 - stats.py] - 2008-01-24
### Added
-Added full range of averaging type functions from _support for finding the
 cluster centroid in singleclustercentroid.

## [1.7.1 - stats.py] - 2008-01-23
### Changed
-Revised calls of _support.median to take advantage of new axis control.

## [0 - partition.py] - 2008-01-22
### Added
-Initial creation date.
-Started work on kmeans.

## [1.7 - stats.py] - 2008-01-16
### Changed
-Edited singleclustercentroid, clustercentroids, & SSE to contain an exponent
 which determines the influence of the weights in levs.  This brings those
 functions into line with formulas 9.1 & 9.2 in Tan, Steinbach, & Kumar (2006),
 Data Mining, Pearson Education Inc., Boston.
-Updated silhouette's documentation to explain why it uses clusterid instead of
 levs.

## [1.0.3 - __init__.py] - 2008-01-02
### Changed
-Documentation update.

## [1.0.2 - __init__.py] - 2007-12-30
### Changed
-Documentation update and reformat to docstring standards.

## [1.6 - stats.py] - 2007-12-30
### Fixed
-Documentation update and reformat to docstring standards.

### Removed
-Removed weightedmedian definition in favor of using _support.median.

### Changed
-Renamed SSE to old_SSE.

### Added
-Wrote SSE that employs the levs array.

## [1.2.4 - distances.py] - 2007-12-29
### Fixed
-Documentation reformated using docstring conventions.

## [1.2.3 - distances.py] - 2007-12-17
### Fixed
-Cleaned up and reformated documentation comments to follow numpy/scipy
 conventions even though they are still comments in the code rather than a
 docstring.  Will convert to a docstring at a later date once I've figured out
 how to do that properly.

## [1.5.2 - stats.py] - 2007-12-11
### Fixed
-Cleanup of old_singleclustercentroid to use scipy.stats.stats.nanmedian and
 scipy.stats.stats.nanmean

## [1.5.1 - stats.py] - 2007-12-06
### Fixed
-Debugging weightedmedian, levels, fuzzy_clustercentroids, & levscheck.

### Changed
-Renamed singleclustercentroid to old_singleculstercentroid.
-Renamed clustercentroids to old_clutercentroids.
-Renamed fuzzy_singleclustercentroid to singleclustercentroid.
-Renamed fuzzy_culstercentroids to clutercentroids.

## [1.5 - stats.py] - 2007-12-05
### Fixed
-Debugging weightedmedian and fuzzy_singleclustercentroid.

### Added
-Wrote levels, fuzzy_clustercentroids, levscheck.

## [1.4 - stats.py] - 2007-12-04
### Added
-Wrote fuzzy_singleclustercentroid.

## [1.3 - stats.py] - 2007-12-03
### Added
-Wrote weightedmedian.

## [1.2 - stats.py] - 2007-11-29
### Added
-Wrote clustercentroids.
-Ported SSE from ClusterStats.

## [1.1.2 - stats.py] - 2007-11-28
### Fixed
-Debugging singleclustercentroid.

## [1.1.1 - stats.py] - 2007-11-26
### Added
-Worked out how to find medians.

## [1.1 - stats.py] - 2007-11-16
### Added
-Started singleclustercentroid.  Still need to figure out how to find medians.

## [1.0.1 - __init__.py] - 2007-11-15
### Changed
-limited distances import statements so that only disambiguation function,
 distance, is brought into cluster name space.  This restricts direct access to
 the individual distance functions, but said access can be restored by
 uncommenting the appropriate line in this program.  Said access, however,
 should not be needed under normal use of this package.  This convention will be
 followed for all disambiguated functions in the future. 

## [1.2.2 - distances.py] - 2007-11-15
### Added
-Added a overlap checker to distances that makes sure that the two vectors have
 at least one dimension on which both have values.

## [1.0 - stats.py] - 2007-11-15
### Added
-Finished distancematrix.
-Wrote fulldistancematrix.
-Ported silhouette, members from ClusterStats.

## [1.0 - __init__.py] - 2007-11-14
###Added
-Initial creation date
-import statements for distances and stats

## [1.2.1 - distances.py] - 2007-11-14
### Fixed
-Debugging kendall so that it can deal with ranking ties.
-Debugging masking.

## [0.0 - stats.py] - 2007-11-14
### Added
-Initial creation date.
-Started work on distancematrix.

## [1.2 - distances.py] - 2007-11-12
### Added
-Type checking/handling implemented in preperation for mask implementation.
 Note: because all external calls are expected to be to distance, and not any of
 the actual distance functions, only distance contains type checking/handling.
-Masking implemented.
-Weighting implemented.

## [1.1.1 - distances.py] - 2007-11-08
### Added
-Added comments/help for each function.

### Fixed
-Debugging.

## [1.1 - distances.py] - 2007-11-07
### Added
-spearman, peuclidian, acosine, & kendall added.

## [1.0 - distances.py] - 2007-11-06
### Added
-Initial creation.
-distance, euclidian, cityblock, hamming, pearson, abspearson, upearson,
 absupearson written.
