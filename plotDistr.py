# =============================================================================
# Plotting script to accompany HOT theory simulation.
# Connected Tree interval size distributions.
#
# Author:           Max Graves
# Last Revised:     21-MAR-2013
# =============================================================================

import pylab as pl
import argparse, os, glob, sys

# =============================================================================
# parse the cmd line
# =============================================================================
def parseCMD():
    """
    Parse cmd line.
    """
    helpString = ('This script plots connected tree interval size distributions\
            from the 1D HOT model.\
            It takes a value of N (number of sites) and L (characteristic scale).\
            This assumes that the Yield_N_L_D.txt files generated from the code\
            will exist in the same directory as this script, and that the number\
            of sparks laid is the same for each file with the same values of N\
            and L.')

    parser = argparse.ArgumentParser(description=helpString)
    parser.add_argument("fileN", help='Peak... file')
    return parser.parse_args()

# =============================================================================
def getD(f):
    """
    strips the D value out of the data file name.
    """
    k = f[:-4]
    i, t = -1, True
    newt = ''
    while t==True:
        if k[i].isdigit():
            newt += k[i]
        else:
            t = False
        i -= 1
    return newt[::-1]

# =============================================================================
# begin main
# =============================================================================
def main():

    # read in the forest as peak yield
    args = parseCMD()
    fileName = args.fileN
    forest = pl.loadtxt(fileName)

    # determine which sites were left unTreed at maximum yield
    sitesLeft = pl.array([])
    for i in xrange(forest.size):
        if forest[i]!=1:
            sitesLeft = pl.append(sitesLeft, i)
    sitesLeft = sitesLeft[::-1]

    # determine intervals and sort them in order of size
    intervals = pl.array([forest.size-1-sitesLeft[0]])
    for i in xrange(1,sitesLeft.size-1):
        sizeInt = sitesLeft[i]-sitesLeft[i+1]
        intervals = pl.append(intervals, sizeInt)
    intervals = pl.append(intervals, sitesLeft[-1])
    intervals = pl.sort(intervals)

    # assign each interval a number
    nums = pl.arange(1,sitesLeft.size+1)

    # main plot
    fig1 = pl.figure(1)
    ax = fig1.add_subplot(111)
    pl.ylabel('Interval Size', fontsize=20)
    pl.xlabel('(Sorted) Inverval Number', fontsize=20)

    # loop over and plot each file we find
    newt = getD(fileName)
    
    ax.plot(nums,intervals,label='(D=%s)'%(newt), marker='o', linewidth=0,
            markerfacecolor='None', markeredgecolor='Navy') 
 
    # put labels into legend
    ax.legend(loc='upper left',shadow=True)
    
    pl.show()

# =============================================================================
if __name__=='__main__':
    main()
