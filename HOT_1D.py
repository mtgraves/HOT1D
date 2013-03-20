# =============================================================================
# HOT theory model in 1-D for forest fires.
#
# Author:               Max Graves
# Date Last Revised:    21-MAR-2013
# =============================================================================

import pyximport; pyximport.install()
import numpy as np
import HOT_modules as critters
import pylab as pl
import os, argparse, random

# =============================================================================
# parse the cmd line
# =============================================================================
helpString = ('HOT theory model for 1D.')

parser = argparse.ArgumentParser(description=helpString)
parser.add_argument('-N','--sites', type=int, default=10000,
        help='enter the number of sites you ran the code for')
parser.add_argument('-L','--charLen', type=int, default=2000,
        help='enter the value of L you ran the code for')
parser.add_argument('-D','--tries', type=int, default=1,
        help='enter the number of times you want to plant a tree')
args = parser.parse_args()

# =============================================================================
def main():

    # define constants
    N, L, D = args.sites, args.charLen, args.tries
    Density = np.arange(N+1)/(1.0*N)

    # define (normalized) probability of a spark at ith site
    P = critters.buildProb(N,L)
    P /= sum(P)

    # decide where to place 100 sparks according to distribution
    sparks = critters.slice_samp(P, 100)

    # plant trees and see how things go
    Yield, peak = critters.buildForest(sparks, N, L, D)

    # zero density when zero trees have been added
    Yield = np.insert(Yield,0,0)
   
    # write final yield vs. density data to disk
    if os.path.exists('./data/'):
        os.chdir('./data/')
    else:
        os.mkdir('./data/')
        os.chdir('./data/')
    
    fileName = 'Yield_N%s_L%s_D%s.txt'% (N,L,D)
    fid = open(fileName, 'w')
    fid.write('# %-20s\t%s\n'%('Density','Yield'))
    fid.write('#\t%.6f\twas the peak Yield\n'%peak)
    zipped = zip(Density,Yield)
    np.savetxt(fid, zipped, fmt='%-20s\t%s')
    fid.close()
    print 'New data has been saved as ',fileName

    print 'peak yield:  ',peak

# =============================================================================
if __name__=='__main__':
    main()
