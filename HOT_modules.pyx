# =============================================================================
# Script to convert Python data structures to C data structures using
# Cython.  This does a large portion of the work for the 1D HOT model.
#
# Author:           Max Graves
# Last Revised:     4-MAR-2013
# =============================================================================

from __future__ import division
import numpy as np
cimport numpy as np
import random

DTYPEi = np.int
DTYPEf = np.float64
ctypedef np.int_t DTYPE_i
ctypedef np.float64_t DTYPE_f

cimport cython
@cython.boundscheck(False)
def slice_samp(np.ndarray[DTYPE_f, ndim=1] Pk, int N = 10):
    """
    Adapted from http://en.wikipedia.org/wiki/Slice_sampling
    Returns an array of integers between 1 and len(Pk), corresponding
    to the probability distribution passed (Pk). Defaults to N=10
    """
    cdef np.ndarray[DTYPE_i, ndim=1] values = np.zeros(N, dtype=int)
    cdef np.ndarray[DTYPE_i, ndim=1] ks = np.arange(1,len(Pk)+1)
    cdef np.ndarray[DTYPE_i, ndim=1] included
    cdef DTYPE_i choice
    
    Pk = np.array(Pk) / (1.*sum(Pk))
    cdef DTYPE_i u = random.uniform(0,max(Pk))
    print 'u: ',u
    for n in xrange(N):
        included = np.where(Pk>=u)[0]
        choice = random.randint(0,included.size)
        values[n] = ks[choice]
        u = random.uniform(0, Pk[choice])
    return values

# =============================================================================
cimport cython
@cython.boundscheck(False)
def testSparks(np.ndarray[DTYPE_i, ndim=1] sparks, 
        np.ndarray[DTYPE_i, ndim=1] forest, int damage, int N):
    """
    Loops over forest a set amount of times and determines the
    damage done for the placement of each spark.
    Returns a total damage which needs to be averaged.
    """
    cdef int sparkNum = 0

    for f in sparks:
        if (forest[f] == 2):
            continue
        elif forest[f] == 1:
            damage += 1

            j = 1
            if j-1 >= 0:
                while forest[f-j] == 1:
                    damage += 1
                    j += 1
                    # don't go past first tree
                    if f-j == -1:
                        break   # out of while loop
            j = 1
            if j+1 < N:
                while forest[f+j] == 1:
                    damage += 1
                    j += 1
                    # don't go past last tree
                    if f+j-1 == N-1:
                        break   # out of while loop
        else:
            print 'CAME OUT OF LOOP'
        sparkNum += 1
    return damage
            
# =============================================================================
def buildProb(int N, double L):
    """
    Takes length of array and a variable for the exponent
    of an exponential function.  Returns a len(N) array.
    """
    cdef np.ndarray[DTYPE_f, ndim=1] P = np.zeros(N, dtype=DTYPEf)

    for i in xrange(N):
        P[i] = np.exp((-1.0*i)/(1.0*L))

    return P

# =============================================================================
cimport cython
@cython.boundscheck(False)
def buildForest(np.ndarray[DTYPE_i, ndim=1] sparks, int N, double L, int D):
    """
    Takes in the sparks (array).  Then, creates an array of site locations
    and places trees (one at a time) in the forest in this pseudo-random
    order.  Each time a new tree is placed, the sparks are placed individually
    into the forest.  If the trees are next to a tree on fire,
    then they set fire.  Else they stay good.
    Returns a len(N) array of the density of trees in the forest.
    """
    # set array to hold the yield
    cdef np.ndarray[DTYPE_f, ndim=1] avgYield = np.zeros(N, dtype=DTYPEf)

    cdef int lenS = len(sparks)
    cdef int r, j, tempTreeLoc, currentBest
    cdef float damage
    cdef int numTrees = 1

    # build forest sites
    cdef np.ndarray[DTYPE_i, ndim=1] forest = 2*np.ones(N, dtype=DTYPEi)
    cdef np.ndarray[DTYPE_i, ndim=1] unTreed = np.arange(N, dtype=DTYPEi)

    for blah in xrange(N):
        # loop through until all sites are 'treed'
        tempTreeYield = 0
        for d in xrange(D):
            # Try out D different places to put trees
            r = random.choice(unTreed)
            #if d>0:
            #    prevTreeloc = r
            if d==0:
                currestBest = r

            tempTreeLoc = r

            forest[r] = 1

            # Lay the sparks
            damage = 0
            damage = testSparks(sparks, forest, damage, N)
            forest[r] = 2
            
            # record yield
            tempTreeYield_t = (numTrees - 1.0*damage/lenS)
            if tempTreeYield_t > tempTreeYield:
                tempTreeYield = tempTreeYield_t
                currentBest = tempTreeLoc
            
        # plant the tree with the best results
        maxYield = tempTreeYield
        chosenSite = currentBest
        forest[chosenSite] = 1

        # Record Yield of best site
        avgYield[numTrees-1] = maxYield

        # delete untreed location from array holding untreed sites
        if numTrees != N:
            unTreed = np.delete(unTreed, np.where(unTreed == chosenSite)[0][0])
            numTrees += 1

        if numTrees %1000 == 0:
            print numTrees

    avgYield /= 1.0*N

    # print the peak yield
    peakYield = np.max(avgYield)

    return avgYield, peakYield
# =============================================================================
