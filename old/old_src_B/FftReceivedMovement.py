#!/usr/bin/env python
# encoding: utf-8
"""
FftReceivedMovement.py

Created by Fredrick Stakem on 2010-02-25.
Copyright (c) 2010 __Research__. All rights reserved.
"""

import pdb
import numpy
import scipy
import pylab
import math
import scipy.stats
import scipy.fftpack

from Vector import Vector
from Sample import Sample
from PredictionSample import PredictionSample
from Packet import Packet
from Importer import Importer
from DRPredictor import DRPredictor
from DRTransmitter import DRTransmitter
from SynchTransmitter import SynchTransmitter
from Reconstructor import Reconstructor
from Network import Network
from Receiver import Receiver
from SnapReconstructor import SnapReconstructor


# Filesystem paramters
dataRoot = "/Users/fstakem/Data/Movements_5_1_08/"
root = "/Users/fstakem/Research/OptimalFiltering/"
movement = "Stacking"
#movement = "TieShoes"
simulationNumber = 1
inputFile = dataRoot + movement + "/Simulation" + str(simulationNumber) + "/positionLog.txt"

# Test parameters
debug = False
samplingInterval = 10
predictionInterval = 100
threshold = .03
heartbeat = 500
delay = 150
jitter = 80
packetLoss = 0

# Viewing parameters
plotInitialSignal = True
plotTxSignal = True
plotRxSignal = True
plotTimeDiff_I_Tx_Signal = False
plotTimeDiff_I_Rx_Signal = False
plotTimeDiff_Rx_Tx_Signal = False
plotFreqDiff_I_Tx_Signal = False
plotFreqDiff_I_Rx_Signal = False
plotFreqDiff_Tx_Rx_Signal = False
plotTimeDomain = True
plotFreqDomain = True
plotPhaseResponse = True
useDb = False
lowerBoundTime = -1 		#17000
upperBoundTime = -1		#22000
lowerBoundFreq = 0
upperBoundFreq = 100

# Import data
print "Importing data..."
importer = Importer()
inputData = importer.getInputData(inputFile, samplingInterval)

# Create the prediction vectors
print "Creating the prediction vectors..."
predictor = DRPredictor()
predictedData = predictor.getPredictedData(inputData, predictionInterval, samplingInterval)

# Run the transmission algorithm
print "Simulating the transmission algorithm..."
transmitter = DRTransmitter(heartbeat)
DRTxPackets = transmitter.getTransmittedPackets(threshold, predictedData)

# Simulate the transmission of the packets
print "Simulating the network..."
network = Network()
DRRxPackets = network.getReceivedPackets(DRTxPackets, delay, jitter, packetLoss)

# Receive the packets
print "Receiving the packets..."
receiver = Receiver()
DRRxData = receiver.getFilteredData(DRRxPackets)

# Reconstruct the transmitted and received data
print "Reconstructing the signals..."
reconstructor = SnapReconstructor()
DRTxData = reconstructor.getReconstructedSignal(DRTxPackets, samplingInterval)
DRRxReconData = reconstructor.getReconstructedSignal(DRRxData, samplingInterval)

# Split data into components
inputTime = range(0, len(inputData) * samplingInterval, samplingInterval)
x = []
y = []
z = []
transmittedTime = []
txX = []
txY = []
txZ = []
receivedTime = []
rxX = []
rxY = []
rxZ = []

for sample in inputData:
	x.append(sample.position.x)
	y.append(sample.position.y)
	z.append(sample.position.z)
	
for sample in DRTxData:
	transmittedTime.append(sample.time)
	txX.append(sample.position.x)
	txY.append(sample.position.y)
	txZ.append(sample.position.z)
	
for sample in DRRxReconData:
	receivedTime.append(sample.time)
	rxX.append(sample.position.x)
	rxY.append(sample.position.y)
	rxZ.append(sample.position.z)
	
# Find the difference in signals in the time domain
print "Finding the error in time domain signals..."
time_I_Tx = []
diff_X_Tx = []
diff_Y_Tx = []
diff_Z_Tx = []

time_I_Rx = []
diff_X_Rx = []
diff_Y_Rx = []
diff_Z_Rx = []

time_Tx_Rx = []
diff_Tx_X_Rx = []
diff_Tx_Y_Rx = []
diff_Tx_Z_Rx = []

for i, t1 in enumerate(inputTime):
	for j, t2 in enumerate(transmittedTime):
		if t1 == t2:
			time_I_Tx.append(t1)
			diff_X_Tx.append( abs(x[i] - txX[j]) )
			diff_Y_Tx.append( abs(y[i] - txY[j]) )
			diff_Z_Tx.append( abs(z[i] - txZ[j]) )

	for j, t3 in enumerate(receivedTime):
		if t1 == t3:
			time_I_Rx.append(t1)
			diff_X_Rx.append( abs(x[i] - rxX[j]) )
			diff_Y_Rx.append( abs(y[i] - rxY[j]) )
			diff_Z_Rx.append( abs(z[i] - rxZ[j]) )

for i, t1 in enumerate(transmittedTime):
	for j, t2 in enumerate(receivedTime):
		if t1 == t2:
			time_Tx_Rx.append(t1)
			diff_Tx_X_Rx.append( abs(txX[i] - rxX[j]) )
			diff_Tx_Y_Rx.append( abs(txY[i] - rxY[j]) )
			diff_Tx_Z_Rx.append( abs(txZ[i] - rxZ[j]) )
			
# Do the fft on the signals -> output is complex number
print "Performing the fft..."
fftX = scipy.fft(x)
fftY = scipy.fft(y)
fftZ = scipy.fft(z)

fftTxX = scipy.fft(txX)
fftTxY = scipy.fft(txY)
fftTxZ = scipy.fft(txZ)

fftRxX = scipy.fft(rxX)
fftRxY = scipy.fft(rxY)
fftRxZ = scipy.fft(rxZ)

# Calculate the magnitude and phase of the fft
print "Splitting up and reformatting the fft..."
freq = len(x) * scipy.fftpack.fftshift( scipy.fftpack.fftfreq( len(x) ) )
freq = freq.tolist()
freqTx = len(fftTxX) * scipy.fftpack.fftshift( scipy.fftpack.fftfreq( len(fftTxX) ) )
freqTx = freqTx.tolist()
freqRx = len(fftRxX) * scipy.fftpack.fftshift( scipy.fftpack.fftfreq( len(fftRxX) ) )
freqRx = freqRx.tolist()

fftMagX = 2 * scipy.fftpack.fftshift( abs(fftX) ) / len(fftX)
fftPhaseX = numpy.arctan2(fftX.imag, fftX.real) * (180/math.pi)
fftMagY = 2 * scipy.fftpack.fftshift( abs(fftY) ) / len(fftY)
fftPhaseY = numpy.arctan2(fftY.imag, fftY.real) * (180/math.pi)
fftMagZ = 2 * scipy.fftpack.fftshift( abs(fftZ) ) / len(fftZ)
fftPhaseZ = numpy.arctan2(fftZ.imag, fftZ.real) * (180/math.pi)

fftMagTxX = 2 * scipy.fftpack.fftshift( abs(fftTxX) ) / len(fftTxX)
fftPhaseTxX = numpy.arctan2(fftTxX.imag, fftTxX.real) * (180/math.pi)
fftMagTxY = 2 * scipy.fftpack.fftshift( abs(fftTxY) ) / len(fftTxY)
fftPhaseTxY = numpy.arctan2(fftTxY.imag, fftTxY.real) * (180/math.pi)
fftMagTxZ = 2 * scipy.fftpack.fftshift( abs(fftTxZ) ) / len(fftTxZ)
fftPhaseTxZ = numpy.arctan2(fftTxZ.imag, fftTxZ.real) * (180/math.pi)

fftMagRxX = 2 * scipy.fftpack.fftshift( abs(fftRxX) ) / len(fftRxX)
fftPhaseRxX = numpy.arctan2(fftRxX.imag, fftRxX.real) * (180/math.pi)
fftMagRxY = 2 * scipy.fftpack.fftshift( abs(fftRxY) ) / len(fftRxY)
fftPhaseRxY = numpy.arctan2(fftRxY.imag, fftRxY.real) * (180/math.pi)
fftMagRxZ = 2 * scipy.fftpack.fftshift( abs(fftRxZ) ) / len(fftRxZ)
fftPhaseRxZ = numpy.arctan2(fftRxZ.imag, fftRxZ.real) * (180/math.pi)

# Find the difference in signals in the frequency domain
print "Finding the noise in the frequency domain signals..."
freq_I_Tx = []
freqDiff_X_Tx = []
freqDiff_Y_Tx = []
freqDiff_Z_Tx = []

freq_I_Rx = []
freqDiff_X_Rx = []
freqDiff_Y_Rx = []
freqDiff_Z_Rx = []

freq_Tx_Rx = []
freqDiff_Tx_X_Rx = []
freqDiff_Tx_Y_Rx = []
freqDiff_Tx_Z_Rx = []

freqResolution = 1

for i, f1 in enumerate(freq):
	for j, f2 in enumerate(freqTx):
		if abs(f1 - f2) < freqResolution:
			freq_I_Tx.append(f1)
			freqDiff_X_Tx.append( abs(fftMagX[i] - fftMagTxX[j]) )
			freqDiff_Y_Tx.append( abs(fftMagY[i] - fftMagTxY[j]) )
			freqDiff_Z_Tx.append( abs(fftMagZ[i] - fftMagTxZ[j]) )

	for j, f3 in enumerate(freqRx):
		if abs(f1 - f3) < freqResolution:
			freq_I_Rx.append(f1)
			freqDiff_X_Rx.append( abs(fftMagX[i] - fftMagRxX[j]) )
			freqDiff_Y_Rx.append( abs(fftMagY[i] - fftMagRxY[j]) )
			freqDiff_Z_Rx.append( abs(fftMagZ[i] - fftMagRxZ[j]) )

for i, f1 in enumerate(freqTx):
	for j, f2 in enumerate(freqRx):
		if abs(f1 - f2) < freqResolution:
			freq_Tx_Rx.append(f1)
			freqDiff_Tx_X_Rx.append( abs(fftMagTxX[i] - fftMagRxX[j]) )
			freqDiff_Tx_Y_Rx.append( abs(fftMagTxY[i] - fftMagRxY[j]) )
			freqDiff_Tx_Z_Rx.append( abs(fftMagTxZ[i] - fftMagRxZ[j]) )

# Reformat frequency in Db if desired
if useDb:
	fftMagX = 20 * scipy.log10(fftMagX)
	fftMagY = 20 * scipy.log10(fftMagY)
	fftMagZ = 20 * scipy.log10(fftMagZ)
	
	fftMagTxX = 20 * scipy.log10(fftMagTxX)
	fftMagTxY = 20 * scipy.log10(fftMagTxY)
	fftMagTxZ = 20 * scipy.log10(fftMagTxZ)
	
	fftMagRxX = 20 * scipy.log10(fftMagRxX)
	fftMagRxY = 20 * scipy.log10(fftMagRxY)
	fftMagRxZ = 20 * scipy.log10(fftMagRxZ)
		
	freqDiff_X_Tx = 20 * scipy.log10(freqDiff_X_Tx)
	freqDiff_Y_Tx = 20 * scipy.log10(freqDiff_Y_Tx)
	freqDiff_Z_Tx = 20 * scipy.log10(freqDiff_Z_Tx)

	freqDiff_X_Rx = 20 * scipy.log10(freqDiff_X_Rx)
	freqDiff_Y_Rx = 20 * scipy.log10(freqDiff_Y_Rx)
	freqDiff_Z_Rx = 20 * scipy.log10(freqDiff_Z_Rx)

	freqDiff_Tx_X_Rx = 20 * scipy.log10(freqDiff_Tx_X_Rx)
	freqDiff_Tx_Y_Rx = 20 * scipy.log10(freqDiff_Tx_Y_Rx)
	freqDiff_Tx_Z_Rx = 20 * scipy.log10(freqDiff_Tx_Z_Rx)

# Hook for debugging before data is plotted
if debug:
	pdb.set_trace()
	
# Plotting variable
plotNumber = 1

# Plot the time domain signals
def setTimeAxis(time, listValues):
	if lowerBoundTime and upperBoundTime != -1:
		lowerIndex = time.index(lowerBoundTime)
		upperIndex = time.index(upperBoundTime)
		newList = listValues[lowerIndex:upperIndex]
		pylab.axis([lowerBoundTime, upperBoundTime, min(newList), max(newList)])
			
if plotTimeDomain:
	if plotInitialSignal:
		pylab.figure(plotNumber)
		plotNumber += 1
		pylab.subplot(311)
		pylab.plot(inputTime, x)
		setTimeAxis(inputTime, x)
		pylab.subplot(312)
		pylab.plot(inputTime, y)
		setTimeAxis(inputTime, y)
		pylab.subplot(313)
		pylab.plot(inputTime, z)
		setTimeAxis(inputTime, z)
	
	if plotTxSignal:
		pylab.figure(plotNumber)
		plotNumber += 1
		pylab.subplot(311)
		pylab.plot(transmittedTime, txX)
		setTimeAxis(transmittedTime, txX)
		pylab.subplot(312)
		pylab.plot(transmittedTime, txY)
		setTimeAxis(transmittedTime, txY)
		pylab.subplot(313)
		pylab.plot(transmittedTime, txZ)
		setTimeAxis(transmittedTime, txZ)
	
	if plotRxSignal:
		pylab.figure(plotNumber)
		plotNumber += 1
		pylab.subplot(311)
		pylab.plot(receivedTime, rxX)
		setTimeAxis(receivedTime, rxX)
		pylab.subplot(312)
		pylab.plot(receivedTime, rxY)
		setTimeAxis(receivedTime, rxY)
		pylab.subplot(313)
		pylab.plot(receivedTime, rxZ)
		setTimeAxis(receivedTime, rxZ)
		
	if plotTimeDiff_I_Tx_Signal:
		pylab.figure(plotNumber)
		plotNumber += 1
		pylab.subplot(311)
		pylab.plot(time_I_Tx, diff_X_Tx)
		setTimeAxis(time_I_Tx, diff_X_Tx)
		pylab.subplot(312)
		pylab.plot(time_I_Tx, diff_Y_Tx)
		setTimeAxis(time_I_Tx, diff_Y_Tx)
		pylab.subplot(313)
		pylab.plot(time_I_Tx, diff_Z_Tx)
		setTimeAxis(time_I_Tx, diff_Z_Tx)
	
	if plotTimeDiff_I_Rx_Signal:
		pylab.figure(plotNumber)
		plotNumber += 1
		pylab.subplot(311)
		pylab.plot(time_I_Rx, diff_X_Rx)
		setTimeAxis(time_I_Rx, diff_X_Rx)
		pylab.subplot(312)
		pylab.plot(time_I_Rx, diff_Y_Rx)
		setTimeAxis(time_I_Rx, diff_Y_Rx)
		pylab.subplot(313)
		pylab.plot(time_I_Rx, diff_Z_Rx)
		setTimeAxis(time_I_Rx, diff_Z_Rx)
		
	if plotTimeDiff_Rx_Tx_Signal:
		pylab.figure(plotNumber)
		plotNumber += 1
		pylab.subplot(311)
		pylab.plot(time_Tx_Rx, diff_Tx_X_Rx)
		setTimeAxis(time_Tx_Rx, diff_Tx_X_Rx)
		pylab.subplot(312)
		pylab.plot(time_Tx_Rx, diff_Tx_Y_Rx)
		setTimeAxis(time_Tx_Rx, diff_Tx_Y_Rx)
		pylab.subplot(313)
		pylab.plot(time_Tx_Rx, diff_Tx_Z_Rx)
		setTimeAxis(time_Tx_Rx, diff_Tx_Z_Rx)
	
# Plot the fft of the signal
def setFreqAxis(frequency, listValues):
	lowerDiff = 5
	upperDiff = 5
	lowerIndex = 0
	upperIndex = 10
	for i, value in enumerate(frequency):
		diff = abs(lowerBoundFreq - value)
		if diff < lowerDiff:
			lowerDiff = diff
			lowerIndex = i
		diff = abs(upperBoundFreq - value)	
		if diff < upperDiff:
			upperDiff = diff
			upperIndex = i

	newList = listValues[lowerIndex:upperIndex]
	pylab.axis([lowerBoundFreq, upperBoundFreq, min(newList), max(newList)])
			
if plotFreqDomain:
	if plotInitialSignal:
		pylab.figure(plotNumber)
		plotNumber += 1
		pylab.subplot(311)
		pylab.plot(freq, fftMagX)
		setFreqAxis(freq, fftMagX)
		pylab.subplot(312)
		pylab.plot(freq, fftMagY)
		setFreqAxis(freq, fftMagY)
		pylab.subplot(313)
		pylab.plot(freq, fftMagZ)
		setFreqAxis(freq, fftMagZ)

	if plotTxSignal:
		pylab.figure(plotNumber)
		plotNumber += 1
		pylab.subplot(311)
		pylab.plot(freqTx, fftMagTxX)
		setFreqAxis(freqTx, fftMagTxX)
		pylab.subplot(312)
		pylab.plot(freqTx, fftMagTxY)
		setFreqAxis(freqTx, fftMagTxY)
		pylab.subplot(313)
		pylab.plot(freqTx, fftMagTxZ)
		setFreqAxis(freqTx, fftMagTxZ)

	if plotRxSignal:
		pylab.figure(plotNumber)
		plotNumber += 1
		pylab.subplot(311)
		pylab.plot(freqRx, fftMagRxX)
		setFreqAxis(freqRx, fftMagRxX)
		pylab.subplot(312)
		pylab.plot(freqRx, fftMagRxY)
		setFreqAxis(freqRx, fftMagRxY)
		pylab.subplot(313)
		pylab.plot(freqRx, fftMagRxZ)
		setFreqAxis(freqRx, fftMagRxZ)
		
	if plotFreqDiff_I_Tx_Signal:
		pylab.figure(plotNumber)
		plotNumber += 1
		pylab.subplot(311)
		pylab.plot(freq_I_Tx, freqDiff_X_Tx)
		setFreqAxis(freq_I_Tx, freqDiff_X_Tx)
		pylab.subplot(312)
		pylab.plot(freq_I_Tx, freqDiff_Y_Tx)
		setFreqAxis(freq_I_Tx, freqDiff_Y_Tx)
		pylab.subplot(313)
		pylab.plot(freq_I_Tx, freqDiff_Z_Tx)
		setFreqAxis(freq_I_Tx, freqDiff_Z_Tx)	
		
	if plotFreqDiff_I_Rx_Signal:
		pylab.figure(plotNumber)
		plotNumber += 1
		pylab.subplot(311)
		pylab.plot(freq_I_Rx, freqDiff_X_Rx)
		setFreqAxis(freq_I_Rx, freqDiff_X_Rx)
		pylab.subplot(312)
		pylab.plot(freq_I_Rx, freqDiff_Y_Rx)
		setFreqAxis(freq_I_Rx, freqDiff_Y_Rx)
		pylab.subplot(313)
		pylab.plot(freq_I_Rx, freqDiff_Z_Rx)
		setFreqAxis(freq_I_Rx, freqDiff_Z_Rx)
		
	if plotFreqDiff_Tx_Rx_Signal:
		pylab.figure(plotNumber)
		plotNumber += 1
		pylab.subplot(311)
		pylab.plot(freq_Tx_Rx, freqDiff_Tx_X_Rx)
		setFreqAxis(freq_Tx_Rx, freqDiff_Tx_X_Rx)
		pylab.subplot(312)
		pylab.plot(freq_Tx_Rx, freqDiff_Tx_Y_Rx)
		setFreqAxis(freq_Tx_Rx, freqDiff_Tx_Y_Rx)
		pylab.subplot(313)
		pylab.plot(freq_Tx_Rx, freqDiff_Tx_Z_Rx)
		setFreqAxis(freq_Tx_Rx, freqDiff_Tx_Z_Rx)
	
if debug:
	pdb.set_trace()
		
pylab.show()




