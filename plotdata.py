# Testing some stuff
# Kendall

from pylab import *
import numpy as n
from numpy import rec
import struct
from math import pi
import types
try:
    import asciidata as ad
except:
    print('Warning: asciidata not available.')
import os

def fixline(line):
    """fix a string containing a line from the various
    ASCII output files of BEC"""
    #can't read e.g. 1D2, but I can read 1E2
    line = line.replace('D', 'E')
    #crappy hack to fix reading crappy files
    line = line.replace('0-', 'E-')
    line = line.replace('0+', 'E-')

    return line
    
class Plot:
    """Class for encapulating data for individual plots in StarGrapht"""
  
    def __init__(self, dirname, filename):
        self.plotdata = PlotData(dirname, filename)
        self.dirname = dirname
        self.filename = filename
        self.nickname = filename
        
    def get_plotdata(self):
        return self.plotdata
    
    def get_dirname(self):
        return self.dirname
    
    def get_filename(self):
        return self.filename
    
    def get_nickname(self):
        return self.nickname
    
    def set_nickname(self, value):
        self.nickname = value
        
    

class PlotData:
    """Class for reading *.plot[12] files and making
    different plots"""

    def __init__(self, dirname, filename):
    
        self.dirname = dirname
        self.filename = filename
        self.load_data(dirname, filename)
        
        
    def load_data(self, dirname, filename):
        """initialize by reading from filename"""
        f = open(os.path.join(dirname, filename), 'r')

        #initialize arrays
        self.time    = []
        self.Tc      = []
        self.Yc      = []
        self.LH      = []
        self.LHe     = []
        self.M       = []
        self.Teff    = []
        self.L       = []
        self.rhoc    = []
        self.LC      = []
        self.Lnu     = []
        self.MdotWind= []
        self.Tmax    = []
        self.rhoTmax = []
        self.MTmax   = []

        #fill arrays
        for line in f:
            #can't read e.g. 1D2, but I can read 1E2
            line = fixline(line)
            
            parts = line.split()
            self.time    += [float(parts[0])]
            self.Tc      += [float(parts[1])]
            self.Yc      += [float(parts[2])]
            self.LH      += [float(parts[3])]
            self.LHe     += [float(parts[4])]
            self.Teff    += [float(parts[7])]
            self.L       += [float(parts[8])]
            self.rhoc    += [float(parts[9])]
            self.LC      += [float(parts[10])]
            self.Lnu     += [float(parts[11])]
            self.MdotWind+= [float(parts[12])]
            self.Tmax    += [float(parts[13])]
            self.rhoTmax += [float(parts[14])]
            self.MTmax   += [float(parts[15])]
            
        f.close()
        
    def reload_data(self):
        self.load_data(self.dirname, self.filename)

    '''
    def hrd(self):
        """Plot a HR-diagram"""
        #print "hrd method called" 
        figure(123)
        plot(n.log10(n.array(self.Teff)), self.L)
        xlabel('logT')
        ylabel('logL')
        xlim(xlim()[::-1]) #reverses the x-axis
        show()

    def lum(self):
        """Plot a luminosity diagram"""
        #print "lum method called"
        figure(456)
        plot(self.time, self.L, 'k-', self.time, self.LH, 'r--', self.time, self.LHe, 'y-', self.time, self.LC, 'c--', self.time, self.Lnu, 'b-')
        legend( ('total lum', 'H lum', 'He lum', 'C lum', 'Nu lum') )
        xlabel('Time (10^7 years)')
        ylabel('logL')

        show()
    
    def rcplot(self):
        #print "rcplot method called"
        figure(678)
        plot(self.rhoc, self.Tmax, 'b-', self.rhoc, self.Tc, 'r--')
        xlabel('')
        ylabel('')
        legend( ('max T', 'central T') )
        show()
     '''
        




#testPlot = Plot("5.0.plot1")


#testPlot.hrd()
#testPlot.lum()
#testPlot.rcplot()
