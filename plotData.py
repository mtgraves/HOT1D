# =============================================================================
# Plotting script to accompany HOT theory simulation.
#
# Author:           Max Graves
# Last Revised:     21-MAR-2013
# =============================================================================

import pylab as pl
import argparse, os, glob, sys

# =============================================================================
# parse the cmd line
# =============================================================================
helpString = ('This script plots the data from the 1D HOT model.\
        It takes a value of N (number of sites) and L (characteristic scale).\
        This assumes that the Yield_N_L_D.txt files generated from the code\
        will exist in the same directory as this script, and that the number\
        of sparks laid is the same for each file with the same values of N\
        and L.')

parser = argparse.ArgumentParser(description=helpString)
parser.add_argument('-N','--sites', type=int,
        help='enter the number of sites you ran the code for')
parser.add_argument('-L','--charLen', type=int,
        help='enter the value of L you ran the code for')
args = parser.parse_args()

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

    L, N = args.charLen, args.sites
    
    if (L==None or N==None):
        print '======HOT ERROR======='
        print 'Need to enter N and L values you submitted jobs for'
        sys.exit()

    os.chdir('./data/')
    files = (glob.glob('*L%s_*'%L) or glob.glob('*N%s_*'%N))
    if files==[]:
        print '======HOT ERROR======='
        print './data/ directory doesnt have one of your values of N or L.'
        sys.exit()

    # main plot
    fig1 = pl.figure(1)
    ax = fig1.add_subplot(111)
    pl.ylabel('Average Yield', fontsize=20)
    pl.xlabel('Density', fontsize=20)

    # inset
    dx=fig1.add_axes([0.19, 0.59, .35, .3])

    # determine what to plot in the inset by taking slightly
    #   less than what is in the lowest peak (assume from D=1)
    try:
        estFile = open('Yield_N10000_L2000_D1.txt','r')
        estLines = estFile.readlines();
        peak = estLines[1].split()
        insetMin = float(peak[1])-0.03
        dataMin = insetMin*N
    except:
        print '=======WARNING======='
        print 'Cannot find D=1 file in ./data directory'
        print 'Defaulting to inset dimensions, may not look good'
        insetMin = 0.95
        dataMin = N*0.95
        sys.exit()

    # Format inset plot axis
    pl.xlabel('Average Yield', fontsize=10)
    pl.ylabel('Density', fontsize=10)
    pl.ylim(insetMin)
    pl.xlim(insetMin)
    pl.title('Zoomed in',fontsize=10)
    pl.grid(True)
    pl.tight_layout()

    for f in files:
        # loop over and plot each file we find
        newt = getD(f)
        Density,Yield = pl.loadtxt(f, unpack=True)
        estFile = open(f,'r')
        estLines = estFile.readlines();
        peak = estLines[1].split()
        estFile.close()

        dx.plot(Density[int(dataMin):N],Yield[int(dataMin):N])
        ax.plot(Density,Yield,label='(D=%s): peak=%s'%(newt,peak[1])) 
 
    # put labels into legend
    ax.legend(loc='lower center',shadow=True)
    
    pl.show()

# =============================================================================
if __name__=='__main__':
    main()
