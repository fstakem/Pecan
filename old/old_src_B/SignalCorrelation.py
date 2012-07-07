#!/usr/bin/env python
# encoding: utf-8
"""
OptimalFilter_A.py

Created by Fredrick Stakem on 2010-03-03.
Copyright (c) 2010 __Research__. All rights reserved.
"""

import pdb
import numpy
import scipy
import pylab
import math
import scipy.stats
import scipy.fftpack
import scipy.signal

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
plotTxSignal = False
plotRxSignal = False
plotCorrelation_I_Tx = True
plotCorrelation_I_Rx = True
plotCorrelation_Tx_Rx = True
plotTimeDomain = True
plotFreqDomain = False
plotPhaseResponse = True
useDb = True
lowerBoundTime = 17000 		#17000
upperBoundTime = 22000		#22000
lowerBoundFreq = 0
upperBoundFreq = 400

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
	
# Find the correlation between signals
time_X_Tx = range(0, (len(inputTime) + len(transmittedTime) - 1) * samplingInterval, samplingInterval)
correlation_X_Tx = scipy.signal.correlate(x, txX)
correlation_Y_Tx = scipy.signal.correlate(y, txY)
correlation_Z_Tx = scipy.signal.correlate(z, txZ)

time_X_Rx = range(0, (len(inputTime) + len(receivedTime) - 1) * samplingInterval, samplingInterval)
correlation_X_Rx = scipy.signal.correlate(x, rxX)
correlation_Y_Rx = scipy.signal.correlate(y, rxY)
correlation_Z_Rx = scipy.signal.correlate(z, rxZ)

time_Tx_Rx_x = range(0, (len(transmittedTime) + len(receivedTime) - 1) * samplingInterval, samplingInterval)
correlation_Tx_Rx_x = scipy.signal.correlate(txX, rxX)
correlation_Tx_Rx_y = scipy.signal.correlate(txY, rxY)
correlation_Tx_Rx_z = scipy.signal.correlate(txZ, rxZ)
				
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
				
	if plotCorrelation_I_Tx:
		pylab.figure(plotNumber)
		plotNumber += 1
		pylab.subplot(311)
		pylab.plot(time_X_Tx, correlation_X_Tx)
		pylab.subplot(312)
		pylab.plot(time_X_Tx, correlation_Y_Tx)
		pylab.subplot(313)
		pylab.plot(time_X_Tx, correlation_Z_Tx)
	
	if plotCorrelation_I_Rx:
		pylab.figure(plotNumber)
		plotNumber += 1
		pylab.subplot(311)
		pylab.plot(time_X_Rx, correlation_X_Rx)
		pylab.subplot(312)
		pylab.plot(time_X_Rx, correlation_Y_Rx)
		pylab.subplot(313)
		pylab.plot(time_X_Rx, correlation_Z_Rx)

	if plotCorrelation_Tx_Rx:
		pylab.figure(plotNumber)
		plotNumber += 1
		pylab.subplot(311)
		pylab.plot(time_Tx_Rx_x, correlation_Tx_Rx_x)
		pylab.subplot(312)
		pylab.plot(time_Tx_Rx_x, correlation_Tx_Rx_y)
		pylab.subplot(313)
		pylab.plot(time_Tx_Rx_x, correlation_Tx_Rx_z)
		
	
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
	
if debug:
	pdb.set_trace()
		
pylab.show()






