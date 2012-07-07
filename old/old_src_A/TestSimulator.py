#!/usr/bin/env python
# encoding: utf-8
"""
TestSimulator.py

Created by Fredrick Stakem on 2010-05-20.
Copyright (c) 2010 __Research__. All rights reserved.
"""
# Import libraries
#------------------------------------------------------------------------------
import Simulator as s
import pdb
import numpy
import scipy
import scipy.signal
import pylab
import time
import math
from enum import Enum
from Globals import *

# Filesystem paramters
#------------------------------------------------------------------------------
dataRoot = "/Users/fstakem/Data/Movements_5_1_08/"
root = "/Users/fstakem/Research/PhD/2010_Research/SeperateConvergence/code/"
libDir = root + "lib/"
logDir = root + "log/"
outputDir = root + "output/"

# Simulation data
#------------------------------------------------------------------------------
movement = "Stacking"
simulation = 1
inputFile = dataRoot + movement + "/Simulation" + str(simulation) + \
			"/positionLog.txt"

# Transmission parameters
#------------------------------------------------------------------------------
predictionInterval = 100
samplingInterval = 10
heartbeat = 500
drThreshold = 0.025
convergenceType = InterpolationType.Time

# Network parameters
#------------------------------------------------------------------------------
delay = 100
jitter = 40
packetLoss = 0

# Reconstruction parameters
#------------------------------------------------------------------------------
convergenceTime = 50
longConvergenceTime = 100

# Calculation parameters
#------------------------------------------------------------------------------
jumpThreshold = 0
jumpSpacing = 1

# Simulate the transmission and reconstruction algorithms
#------------------------------------------------------------------------------
startTimeTotal = time.time()
transmittedData = []
simNumber = inputFile.split('/')[-2][-1]

data = s.transmitData(inputFile, logDir, predictionInterval,
					  samplingInterval, heartbeat, drThreshold,
					  delay, jitter, packetLoss)
snapData = s.snapReconstructData(data[5], 
								 logDir, 
								 simNumber, 
								 samplingInterval)[0]								
convergeData = s.convergeData(data[5], logDir, simNumber, samplingInterval,
			   				  convergenceTime)[0]								
varConvergeData = s.varConvergeData(data[5], logDir, simNumber, samplingInterval,
								    convergenceTime, longConvergenceTime)[0]

data.append(snapData)
data.append(convergeData)
data.append(varConvergeData)

print "Total time spent simulating the transmission: " + str(time.time() - \
															 startTimeTotal)
print

# Set the variables for the data
#------------------------------------------------------------------------------
initialData = data[1]
snapData = data[6]
convergeData = data[7]
varConvergeData = data[8]

# Calculate the results and statistics
#------------------------------------------------------------------------------
inputJump = s.calculateStats( s.findDistanceBetweenSamples(initialData,
										 				   jumpThreshold,
										 				   jumpSpacing) )										
snapError = s.calculateStats( s.findDistanceError(initialData,
								    			  snapData) )
snapJump = s.calculateStats( s.findDistanceBetweenSamples(snapData,
									 				   	  jumpThreshold,
									 				   	  jumpSpacing) )
convergeError = s.calculateStats( s.findDistanceError(initialData,
													  convergeData) )
convergeJump = s.calculateStats( s.findDistanceBetweenSamples(convergeData,
															  jumpThreshold,
															  jumpSpacing) )
varConvergeError = s.calculateStats( s.findDistanceError(initialData,
														 varConvergeData) )
varConvergeJump = s.calculateStats( s.findDistanceBetweenSamples(varConvergeData,
																 jumpThreshold,
																 jumpSpacing) )
																
# Output the statistics
#------------------------------------------------------------------------------
print "Jump:"
print "\tInput:\t\t" + str(inputJump)
print "\tSnap:\t\t" + str(snapJump)
print "\tConverge:\t" + str(convergeJump) 
print "\tVar Converge:\t" + str(varConvergeJump)
print "Error:"
print "\tSnap:\t\t" + str(snapError) 
print "\tConverge:\t" + str(convergeError)
print "\tVar Converge:\t" + str(varConvergeError)


# Seperate the singals for plotting
#------------------------------------------------------------------------------
initialTime, initialX, initialY, initialZ = s.splitData(initialData)
snapTime, snapX, snapY, snapZ = s.splitData(snapData)
convergeTime, convergeX, convergeY, convergeZ = s.splitData(convergeData)
varConvergeTime, varConvergeX, varConvergeY, varConvergeZ = s.splitData(varConvergeData)

lowerBound = 19000
upperBound = 25000
initialTime, initialX = s.cropData(initialTime, initialX, lowerBound, upperBound)
snapTime, snapX = s.cropData(snapTime, snapX, lowerBound, upperBound)
convergeTime, convergeX = s.cropData(convergeTime, convergeX, lowerBound, upperBound)
varConvergeTime, varConvergeX = s.cropData(varConvergeTime, varConvergeX, lowerBound, upperBound)
																	
# Plot the signals
#------------------------------------------------------------------------------
figure = 1
pylab.figure(figure)
pylab.plot(initialTime, initialX, 'k-')
pylab.plot(snapTime, snapX, 'b-')
pylab.plot(convergeTime, convergeX, 'r-')
pylab.plot(varConvergeTime, varConvergeX, 'g-')

figure = 2
pylab.figure(figure)
pylab.plot(varConvergeTime, varConvergeX, 'g-')

pylab.show()










