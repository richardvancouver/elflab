""" Implementation of plotting live data from measurements, utilizing multi-processing

"""
# Global flags
DEBUG_INFO = True

# import modules
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class PlotLive:
    """ Implementation of plotting live data from measurements"""
    
    # Computing-related constants
    MAXFLOATS = 10000000     # The maximum number of float numbers to be stored
    SMALL = 1.e-12       # a very small non-zero
    
    # Graph-related constants
    LW = 2      # line width
    OVERRANGE = 0.01     # percentage to over-range the axes
    MARKERPOOL = ["x", "+", "o", "s", "^", "D", "*"]     # pools of plotting markers
    COLOURPOOL = ["b", "g", "r", "k", "y", "m"]     # pools of colours
    
    # The constructor
    def __init__(self, pipeEnd, nrows=1, ncols=1, xyLabels=[[("", "")]], smaplingInterval=100):
                # self, (one end of a Pipe), (No. of rows of subplots), (No. of cols), (list of variables to plot in each subplots), (list of labels), sampling interval in ms
        # Save constants
        self.pipeEnd = pipeEnd
        self.nrows = nrows
        self.ncols = ncols
        self.xyLabels = xyLabels
        self.samplingInterval = samplingInterval
        
        # Calculate derived constants
        self.maxPoints = self.MAXFLOATS // (nrows * ncols * 2)      # maximum number of datapoints
        self.styles = xyLabels.copy()       # plotting style strings for each sub-plot
        for i in range(nrows):
            for j in range(ncols):
                k = i*nrows + j
                self.styles[i][j] = self.COLOURPOOL[k % len(self.COLOURPOOL)] + self.MARKERPOOL[k % len(self.MARKERPOOL)]
        if DEBUG_INFO:
            print("##### Debug Info: class PlotLive #####\n------------------------\n    styles ==\n{}\n------------------------".format(self.styles))
        
        # Initialise the plotted data
        self.nPoints = 0
        self.xys = np.empty([nrows, ncols, 2, self.maxPoints], dtype=float)
        
        # Initialise the record of extrema of x's and y's for each sub plots
        self.xyLims = np.empty((nrows, ncols, 2, 2))
        self.xyLims[:,:,:,0].fill(float("inf"))
        self.xyLims[:,:,:,1].fill(float("-inf"))
        
        # Initialise the plots
        self.fig, self.subs= plt.subplots(nrows, ncols, squeeze=False)
        self.lines = []      # list of Line2D objects
        # ____Plot empty sub-plots, set the plot styles and save the Line2D objects
        for i in range(nrows):
            linerow = []
            for j in range(ncows):
                self.line, = self.subs[i][j].plot([], [], styles[i][j], lw=self.LW)
                self.subs[i][j].set_xlabel(xyLabels[i][j][0])
                self.subs[i][j].set_ylabel(xyLabels[i][j][1])
                self.subs[i][j].set_xlim(1., -1.)
                self.subs[i][j].set_ylim(1., -1.)
                self.subs[i][j].grid()
                linerow.append(line)
            self.lines.append(linerow)
            
    # Generator to inquire data from the pipe
    def inquireXys(self):
        while self.nPoint < self.maxPoints:
            self.pipeEnd.send(True)
            dataPoint = self.pipeEnd.recv()     # dataPoint: a 2D list of (x, y) for each sub-plot
            yield dataPoint
        else:
        
    # Function to update the plots
    def update(self, dataPoint):
                     # dataPoint[i][j] = (x, y) for sub-plot(i,j)
        k = self.nPoints
        self.nPoints += 1
        rescale = False
        for i in range(self.nrows):
            for j in range(self.ncols):
                self.xys[i, j, 0, k] = x = dataPoint[i][j][0]
                self.xys[i, j, 1, k] = y = dataPoint[i][j][1]
                xMin, xMax = xyLims[i, j, 0] 
                yMin, yMax = xyLims[i, j, 1]
                # Test whether x, y are out of range
                if rescale or (x < xMin) or (x > xMax) or (y < yMin) or (y > yMax):
                    rescale = True
                    
                    xMin = min(x, xMin)
                    xMax = max(x, xMax)
                    yMin = min(y, yMin)
                    yMax = max(y, yMax)
                    
                    self.xyLims[i, j, 0] = xMin, xMax
                    self.xyLims[i, j, 1] = yMin, yMax
                    
                    delX = OVERRANGE * (xMax - xMin + SMALL)
                    delY = OVERRANGE * (yMax - yMin + SMALL)
                    
                    self.subs[i][j].set_xlim (xMin - delX, xMax + delX)
                    self.subs[i][j].set_ylim (yMin - delY, yMax + delY)
                # Update the subplot    
                self.lines[i][j].set_data(self.xys[i, j, 0, :k+1], self.xys[i, j, 1, :k+1])
                
        # Rescale if necessary
        if rescale:
            self.fig.canvas.draw()
        return self.lines

    # Function to animate the plot
    def startPlotting(self)
        self.ani = animation.FuncAnimation(self.fig, run, data_gen, blit=True, interval=10,
    repeat=False)
        plt.show()