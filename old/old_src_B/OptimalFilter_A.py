#!/usr/bin/env python
# encoding: utf-8
"""
OptimalFilter_A.py

Created by Fredrick Stakem on 2010-03-03.
Copyright (c) 2010 __Research__. All rights reserved.
"""

import pdb
import sys
import os
import numpy
import scipy
import pylab
import math
import scipy.stats
import scipy.fftpack
import scipy.signal
from enum import Enum

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
from IntReconstructor import IntReconstructor

# --------------------------------------------------------------------------------------
# TODO ->
# 6) Plot the filter frequency and phase response

# Globals
InterpolationType = Enum( 'Time', 'Distance' )

# Filesystem paramters
dataRoot = "/Users/fstakem/Data/Movements_5_1_08/"
root = "/Users/fstakem/Research/OptimalFiltering/"
logDir = root + "code/log/"
movement = "Stacking"
simulationNumber = 1
inputFile = dataRoot + movement + "/Simulation" + str(simulationNumber) + "/positionLog.txt"

# Test parameters
debug = False
samplingInterval = 10
predictionInterval = 100
drThreshold = .02
reconThreshold = 100
interpolationType = InterpolationType.Time
heartbeat = 500
delay = 100
jitter = 20
packetLoss = 0
networkParams = ":  " + str(delay) + " " + str(jitter) + " " + str(packetLoss)

# Filter parameters
numberOfTaps = 20
bands = [0, 1, 2, 50]
weight = [1.0, 0.0]
coefficients = scipy.signal.remez(numberOfTaps, bands, weight, Hz=100)
totalWeight = 0
for i in coefficients:
	totalWeight += i
amplifier = 1.0 / totalWeight
print coefficients
print amplifier

# Viewing parameters
plotInitialSignal = True
plotTxSnapSignal = False
plotRxSnapSignal = False
plotTxIntSignal = False
plotRxIntSignal = True
plotTxFilteredSignal = False
plotRxFilteredSignal = True
plotTimeDomain = True
plotFreqDomain = False
plotPhaseResponse = True
useDb = False
lowerBoundTime = 17000 		#17000
upperBoundTime = 22000		#22000
lowerBoundFreq = 0
upperBoundFreq = 100

# Output function
def exportData(filename, data):
	print "Exporting data to " + filename.split('/')[-1]
	file = open(filename, 'w')
	for sample in data:
		file.write(str(sample) + "\n")
	file.close()

# Import data
print "Importing data..."
importer = Importer()
inputData = importer.getInputData(inputFile, samplingInterval)
exportData(logDir + "InputData.txt", inputData)

# Create the prediction vectors
print "Creating the prediction vectors..."
predictor = DRPredictor()
predictedData = predictor.getPredictedData(inputData, predictionInterval, samplingInterval)
exportData(logDir + "PredictionData.txt", predictedData)

# Run the transmission algorithm
print "Simulating the transmission algorithm..."
transmitter = DRTransmitter(heartbeat)
DRTxPackets = transmitter.getTransmittedPackets(drThreshold, predictedData)
exportData(logDir + "DRTxPackets.txt", DRTxPackets)

# Simulate the transmission of the packets
print "Simulating the network..."
network = Network()
DRRxPackets = network.getReceivedPackets(DRTxPackets, delay, jitter, packetLoss)
exportData(logDir + "DRRxPackets.txt", DRRxPackets)

# Receive the packets
print "Receiving the packets..."
receiver = Receiver()
DRRxData = receiver.getFilteredData(DRRxPackets)
exportData(logDir + "DRRxData.txt", DRRxData)

# Snap reconstruct the transmitted and received data
print "Snap reconstructing the signals..."
snapReconstructor = SnapReconstructor()
DRTxSnapData = snapReconstructor.getReconstructedSignal(DRTxPackets, samplingInterval)
DRRxSnapData = snapReconstructor.getReconstructedSignal(DRRxData, samplingInterval)
exportData(logDir + "DRTxSnapData.txt", DRTxSnapData)
exportData(logDir + "DRRxSnapData.txt", DRRxSnapData)

# Interpolation reconstruct the transmitted and received data
print "Interpolation reconstructing the signals..."
intReconstructor = IntReconstructor()
DRTxIntData = intReconstructor.getReconstructedSignal(DRTxPackets, samplingInterval, 
    												  interpolationType, reconThreshold)
DRRxIntData = intReconstructor.getReconstructedSignal(DRRxData, samplingInterval, 
													  interpolationType, reconThreshold)
exportData(logDir + "DRTxIntData.txt", DRTxIntData)
exportData(logDir + "DRRxIntData.txt", DRRxIntData)

# Split data into components
print "Splitting the data into individual components..."
inputTime = []
x = []
y = []
z = []
transmittedSnapTime = []
txSnapX = []
txSnapY = []
txSnapZ = []
receivedSnapTime = []
rxSnapX = []
rxSnapY = []
rxSnapZ = []
transmittedIntTime = []
txIntX = []
txIntY = []
txIntZ = []
receivedIntTime = []
rxIntX = []
rxIntY = []
rxIntZ = []

for sample in inputData:
	inputTime.append(sample.time)
	x.append(sample.position.x)
	y.append(sample.position.y)
	z.append(sample.position.z)
	
for sample in DRTxSnapData:
	transmittedSnapTime.append(sample.time)
	txSnapX.append(sample.position.x)
	txSnapY.append(sample.position.y)
	txSnapZ.append(sample.position.z)
	
for sample in DRRxSnapData:
	receivedSnapTime.append(sample.time)
	rxSnapX.append(sample.position.x)
	rxSnapY.append(sample.position.y)
	rxSnapZ.append(sample.position.z)
	
for sample in DRTxIntData:
	transmittedIntTime.append(sample.time)
	txIntX.append(sample.position.x)
	txIntY.append(sample.position.y)
	txIntZ.append(sample.position.z)

for sample in DRRxIntData:
	receivedIntTime.append(sample.time)
	rxIntX.append(sample.position.x)
	rxIntY.append(sample.position.y)
	rxIntZ.append(sample.position.z)
	
# Filter the snap data with a FIR filter defined above
filteredTxX = scipy.signal.convolve(coefficients, txSnapX) * amplifier
filteredTxY = scipy.signal.convolve(coefficients, txSnapY) * amplifier
filteredTxZ = scipy.signal.convolve(coefficients, txSnapZ) * amplifier
#filteredTxX = scipy.signal.convolve(coefficients, txSnapX)
#filteredTxY = scipy.signal.convolve(coefficients, txSnapY)
#filteredTxZ = scipy.signal.convolve(coefficients, txSnapZ) 
timeFilteredTx = scipy.linspace(transmittedSnapTime[0], 
								transmittedSnapTime[0] + (len(filteredTxX) * samplingInterval), 
								len(filteredTxX))
timeFilteredTx = timeFilteredTx.tolist()
								
filteredRxX = scipy.signal.convolve(coefficients, rxSnapX) * amplifier
filteredRxY = scipy.signal.convolve(coefficients, rxSnapY) * amplifier
filteredRxZ = scipy.signal.convolve(coefficients, rxSnapZ) * amplifier
#filteredRxX = scipy.signal.convolve(coefficients, rxSnapX)
#filteredRxY = scipy.signal.convolve(coefficients, rxSnapY)
#filteredRxZ = scipy.signal.convolve(coefficients, rxSnapZ)
timeFilteredRx = scipy.linspace(receivedSnapTime[0], 
								receivedSnapTime[0] + (len(filteredRxX) * samplingInterval), 
								len(filteredRxX))
timeFilteredRx = timeFilteredRx.tolist()
								
# Do the fft on the signals -> output is complex number
print "Performing the fft..."
fftX = scipy.fft(x)
fftY = scipy.fft(y)
fftZ = scipy.fft(z)

fftTxSnapX = scipy.fft(txSnapX)
fftTxSnapY = scipy.fft(txSnapY)
fftTxSnapZ = scipy.fft(txSnapZ)

fftRxSnapX = scipy.fft(rxSnapX)
fftRxSnapY = scipy.fft(rxSnapY)
fftRxSnapZ = scipy.fft(rxSnapZ)

fftTxIntX = scipy.fft(txIntX)
fftTxIntY = scipy.fft(txIntY)
fftTxIntZ = scipy.fft(txIntZ)

fftRxIntX = scipy.fft(rxIntX)
fftRxIntY = scipy.fft(rxIntY)
fftRxIntZ = scipy.fft(rxIntZ)

fftFilteredTxX = scipy.fft(filteredTxX)
fftFilteredTxY = scipy.fft(filteredTxY)
fftFilteredTxZ = scipy.fft(filteredTxZ)

fftFilteredRxX = scipy.fft(filteredRxX)
fftFilteredRxY = scipy.fft(filteredRxY)
fftFilteredRxZ = scipy.fft(filteredRxZ)

# Calculate the magnitude and phase of the fft
print "Splitting up and reformatting the fft..."
freq = len(x) * scipy.fftpack.fftshift( scipy.fftpack.fftfreq( len(x) ) )
freq = freq.tolist()
freqTxSnap = len(fftTxSnapX) * scipy.fftpack.fftshift( scipy.fftpack.fftfreq( len(fftTxSnapX) ) )
freqTxSnap = freqTxSnap.tolist()
freqRxSnap = len(fftRxSnapX) * scipy.fftpack.fftshift( scipy.fftpack.fftfreq( len(fftRxSnapX) ) )
freqRxSnap = freqRxSnap.tolist()
freqTxInt = len(fftTxIntX) * scipy.fftpack.fftshift( scipy.fftpack.fftfreq( len(fftTxIntX) ) )
freqTxInt = freqTxInt.tolist()
freqRxInt = len(fftRxIntX) * scipy.fftpack.fftshift( scipy.fftpack.fftfreq( len(fftRxIntX) ) )
freqRxInt = freqRxInt.tolist()
freqFilteredTx = len(fftFilteredTxX) * scipy.fftpack.fftshift( scipy.fftpack.fftfreq( len(fftFilteredTxX) ) )
freqFilteredTx = freqFilteredTx.tolist()
freqFilteredRx = len(fftFilteredRxX) * scipy.fftpack.fftshift( scipy.fftpack.fftfreq( len(fftFilteredRxX) ) )
freqFilteredRx = freqFilteredRx.tolist()

fftMagX = 2 * scipy.fftpack.fftshift( abs(fftX) ) / len(fftX)
fftPhaseX = numpy.arctan2(fftX.imag, fftX.real) * (180/math.pi)
fftMagY = 2 * scipy.fftpack.fftshift( abs(fftY) ) / len(fftY)
fftPhaseY = numpy.arctan2(fftY.imag, fftY.real) * (180/math.pi)
fftMagZ = 2 * scipy.fftpack.fftshift( abs(fftZ) ) / len(fftZ)
fftPhaseZ = numpy.arctan2(fftZ.imag, fftZ.real) * (180/math.pi)

fftMagTxSnapX = 2 * scipy.fftpack.fftshift( abs(fftTxSnapX) ) / len(fftTxSnapX)
fftPhaseTxSnapX = numpy.arctan2(fftTxSnapX.imag, fftTxSnapX.real) * (180/math.pi)
fftMagTxSnapY = 2 * scipy.fftpack.fftshift( abs(fftTxSnapY) ) / len(fftTxSnapY)
fftPhaseTxSnapY = numpy.arctan2(fftTxSnapY.imag, fftTxSnapY.real) * (180/math.pi)
fftMagTxSnapZ = 2 * scipy.fftpack.fftshift( abs(fftTxSnapZ) ) / len(fftTxSnapZ)
fftPhaseTxSnapZ = numpy.arctan2(fftTxSnapZ.imag, fftTxSnapZ.real) * (180/math.pi)

fftMagRxSnapX = 2 * scipy.fftpack.fftshift( abs(fftRxSnapX) ) / len(fftRxSnapX)
fftPhaseRxSnapX = numpy.arctan2(fftRxSnapX.imag, fftRxSnapX.real) * (180/math.pi)
fftMagRxSnapY = 2 * scipy.fftpack.fftshift( abs(fftRxSnapY) ) / len(fftRxSnapY)
fftPhaseRxSnapY = numpy.arctan2(fftRxSnapY.imag, fftRxSnapY.real) * (180/math.pi)
fftMagRxSnapZ = 2 * scipy.fftpack.fftshift( abs(fftRxSnapZ) ) / len(fftRxSnapZ)
fftPhaseRxSnapZ = numpy.arctan2(fftRxSnapZ.imag, fftRxSnapZ.real) * (180/math.pi)

fftMagTxIntX = 2 * scipy.fftpack.fftshift( abs(fftTxIntX) ) / len(fftTxIntX)
fftPhaseTxIntX = numpy.arctan2(fftTxIntX.imag, fftTxIntX.real) * (180/math.pi)
fftMagTxIntY = 2 * scipy.fftpack.fftshift( abs(fftTxIntY) ) / len(fftTxIntY)
fftPhaseTxIntY = numpy.arctan2(fftTxIntY.imag, fftTxIntY.real) * (180/math.pi)
fftMagTxIntZ = 2 * scipy.fftpack.fftshift( abs(fftTxIntZ) ) / len(fftTxIntZ)
fftPhaseTxIntZ = numpy.arctan2(fftTxIntZ.imag, fftTxIntZ.real) * (180/math.pi)

fftMagRxIntX = 2 * scipy.fftpack.fftshift( abs(fftRxIntX) ) / len(fftRxIntX)
fftPhaseRxIntX = numpy.arctan2(fftRxIntX.imag, fftRxIntX.real) * (180/math.pi)
fftMagRxIntY = 2 * scipy.fftpack.fftshift( abs(fftRxIntY) ) / len(fftRxIntY)
fftPhaseRxIntY = numpy.arctan2(fftRxIntY.imag, fftRxIntY.real) * (180/math.pi)
fftMagRxIntZ = 2 * scipy.fftpack.fftshift( abs(fftRxIntZ) ) / len(fftRxIntZ)
fftPhaseRxIntZ = numpy.arctan2(fftRxIntZ.imag, fftRxIntZ.real) * (180/math.pi)

fftMagFilteredTxX = 2 * scipy.fftpack.fftshift( abs(fftFilteredTxX) ) / len(fftFilteredTxX)
fftPhaseFilteredTxX = numpy.arctan2(fftFilteredTxX.imag, fftFilteredTxX.real) * (180/math.pi)
fftMagFilteredTxY = 2 * scipy.fftpack.fftshift( abs(fftFilteredTxY) ) / len(fftFilteredTxY)
fftPhaseFilteredTxY = numpy.arctan2(fftFilteredTxY.imag, fftFilteredTxY.real) * (180/math.pi)
fftMagFilteredTxZ = 2 * scipy.fftpack.fftshift( abs(fftFilteredTxZ) ) / len(fftFilteredTxZ)
fftPhaseFilteredTxZ = numpy.arctan2(fftFilteredTxZ.imag, fftFilteredTxZ.real) * (180/math.pi)

fftMagFilteredRxX = 2 * scipy.fftpack.fftshift( abs(fftFilteredRxX) ) / len(fftFilteredRxX)
fftPhaseFilteredRxX = numpy.arctan2(fftFilteredRxX.imag, fftFilteredRxX.real) * (180/math.pi)
fftMagFilteredRxY = 2 * scipy.fftpack.fftshift( abs(fftFilteredRxY) ) / len(fftFilteredRxY)
fftPhaseFilteredRxY = numpy.arctan2(fftFilteredRxY.imag, fftFilteredRxY.real) * (180/math.pi)
fftMagFilteredRxZ = 2 * scipy.fftpack.fftshift( abs(fftFilteredRxZ) ) / len(fftFilteredRxZ)
fftPhaseFilteredRxZ = numpy.arctan2(fftFilteredRxZ.imag, fftFilteredRxZ.real) * (180/math.pi)


# Reformat frequency in Db if desired
if useDb:
	print "Recalculating the frequency response in db..."
	fftMagX = 20 * scipy.log10(fftMagX)
	fftMagY = 20 * scipy.log10(fftMagY)
	fftMagZ = 20 * scipy.log10(fftMagZ)
	
	fftMagTxSnapX = 20 * scipy.log10(fftMagTxSnapX)
	fftMagTxSnapY = 20 * scipy.log10(fftMagTxSnapY)
	fftMagTxSnapZ = 20 * scipy.log10(fftMagTxSnapZ)
	
	fftMagRxSnapX = 20 * scipy.log10(fftMagRxSnapX)
	fftMagRxSnapY = 20 * scipy.log10(fftMagRxSnapY)
	fftMagRxSnapZ = 20 * scipy.log10(fftMagRxSnapZ)
	
	fftMagTxIntX = 20 * scipy.log10(fftMagTxIntX)
	fftMagTxIntY = 20 * scipy.log10(fftMagTxIntY)
	fftMagTxIntZ = 20 * scipy.log10(fftMagTxIntZ)
	
	fftMagRxIntX = 20 * scipy.log10(fftMagRxIntX)
	fftMagRxIntY = 20 * scipy.log10(fftMagRxIntY)
	fftMagRxIntZ = 20 * scipy.log10(fftMagRxIntZ)
	
	fftMagFilteredTxX = 20 * scipy.log10(fftMagFilteredTxX)
	fftMagFilteredTxY = 20 * scipy.log10(fftMagFilteredTxY)
	fftMagFilteredTxZ = 20 * scipy.log10(fftMagFilteredTxZ)
	
	fftMagFilteredRxX = 20 * scipy.log10(fftMagFilteredRxX)
	fftMagFilteredRxY = 20 * scipy.log10(fftMagFilteredRxY)
	fftMagFilteredRxZ = 20 * scipy.log10(fftMagFilteredRxZ)
	
# Hook for debugging before data is plotted
if debug:
	pdb.set_trace()

# Plotting variable
print "Plotting the data..."
plotNumber = 1

# Plot the time domain signals
def setTimeAxis(time, listValues):
	if lowerBoundTime != -1 and upperBoundTime != -1:
		for i,t in enumerate(time):
			distance = abs(t - lowerBoundTime)
			if distance < samplingInterval:
				lowerIndex = i
			distance = abs(t - upperBoundTime)
			if distance < samplingInterval:
				upperIndex = i
				break
		#lowerIndex = time.index(lowerBoundTime)
		#upperIndex = time.index(upperBoundTime)
		newList = listValues[lowerIndex:upperIndex]
		pylab.axis([lowerBoundTime, upperBoundTime, min(newList), max(newList)])

if plotTimeDomain:
	if plotInitialSignal:
		pylab.figure(plotNumber)
		plotNumber += 1
		pylab.subplot(311)
		pylab.plot(inputTime, x)
		setTimeAxis(inputTime, x)
		pylab.title("Initial Signal" + networkParams)
		pylab.subplot(312)
		pylab.plot(inputTime, y)
		setTimeAxis(inputTime, y)
		pylab.subplot(313)
		pylab.plot(inputTime, z)
		setTimeAxis(inputTime, z)
		
	if plotTxSnapSignal:
		pylab.figure(plotNumber)
		plotNumber += 1
		pylab.subplot(311)
		pylab.plot(transmittedSnapTime, txSnapX)
		setTimeAxis(transmittedSnapTime, txSnapX)
		pylab.title("Transmitted Signal Snap Recon" + networkParams)
		pylab.subplot(312)
		pylab.plot(transmittedSnapTime, txSnapY)
		setTimeAxis(transmittedSnapTime, txSnapY)
		pylab.subplot(313)
		pylab.plot(transmittedSnapTime, txSnapZ)
		setTimeAxis(transmittedSnapTime, txSnapZ)

	if plotRxSnapSignal:
		pylab.figure(plotNumber)
		plotNumber += 1
		pylab.subplot(311)
		pylab.plot(receivedSnapTime, rxSnapX)
		setTimeAxis(receivedSnapTime, rxSnapX)
		pylab.title("Received Signal Snap Recon" + networkParams)
		pylab.subplot(312)
		pylab.plot(receivedSnapTime, rxSnapY)
		setTimeAxis(receivedSnapTime, rxSnapY)
		pylab.subplot(313)
		pylab.plot(receivedSnapTime, rxSnapZ)
		setTimeAxis(receivedSnapTime, rxSnapZ)
		
	if plotTxIntSignal:
		pylab.figure(plotNumber)
		plotNumber += 1
		pylab.subplot(311)
		pylab.plot(transmittedIntTime, txIntX)
		setTimeAxis(transmittedIntTime, txIntX)
		pylab.title("Transmitted Signal Int Recon" + networkParams)
		pylab.subplot(312)
		pylab.plot(transmittedIntTime, txIntY)
		setTimeAxis(transmittedIntTime, txIntY)
		pylab.subplot(313)
		pylab.plot(transmittedIntTime, txIntZ)
		setTimeAxis(transmittedIntTime, txIntZ)

	if plotRxIntSignal:
		pylab.figure(plotNumber)
		plotNumber += 1
		pylab.subplot(311)
		pylab.plot(receivedIntTime, rxIntX)
		setTimeAxis(receivedIntTime, rxIntX)
		pylab.title("Received Signal Int Recon" + networkParams)
		pylab.subplot(312)
		pylab.plot(receivedIntTime, rxIntY)
		setTimeAxis(receivedIntTime, rxIntY)
		pylab.subplot(313)
		pylab.plot(receivedIntTime, rxIntZ)
		setTimeAxis(receivedIntTime, rxIntZ)
		
	if plotTxFilteredSignal:
		pylab.figure(plotNumber)
		plotNumber += 1
		pylab.subplot(311)
		pylab.plot(timeFilteredTx, filteredTxX)
		setTimeAxis(timeFilteredTx, filteredTxX)
		pylab.title("Transmitted Signal Filtered" + networkParams)
		pylab.subplot(312)
		pylab.plot(timeFilteredTx, filteredTxY)
		setTimeAxis(timeFilteredTx, filteredTxY)
		pylab.subplot(313)
		pylab.plot(timeFilteredTx, filteredTxZ)
		setTimeAxis(timeFilteredTx, filteredTxZ)
		
	if plotRxFilteredSignal:
		pylab.figure(plotNumber)
		plotNumber += 1
		pylab.subplot(311)
		pylab.plot(timeFilteredRx, filteredRxX)
		setTimeAxis(timeFilteredRx, filteredRxX)
		pylab.title("Received Signal Filtered" + networkParams)
		pylab.subplot(312)
		pylab.plot(timeFilteredRx, filteredRxY)
		setTimeAxis(timeFilteredRx, filteredRxY)
		pylab.subplot(313)
		pylab.plot(timeFilteredRx, filteredRxZ)
		setTimeAxis(timeFilteredRx, filteredRxZ)
		
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
		pylab.title("Initial Signal" + networkParams)
		pylab.subplot(312)
		pylab.plot(freq, fftMagY)
		setFreqAxis(freq, fftMagY)
		pylab.subplot(313)
		pylab.plot(freq, fftMagZ)
		setFreqAxis(freq, fftMagZ)
		
	if plotTxSnapSignal:
		pylab.figure(plotNumber)
		plotNumber += 1
		pylab.subplot(311)
		pylab.plot(freqTxSnap, fftMagTxSnapX)
		setFreqAxis(freqTxSnap, fftMagTxSnapX)
		pylab.title("Transmitted Signal Snap Recon" + networkParams)
		pylab.subplot(312)
		pylab.plot(freqTxSnap, fftMagTxSnapY)
		setFreqAxis(freqTxSnap, fftMagTxSnapY)
		pylab.subplot(313)
		pylab.plot(freqTxSnap, fftMagTxSnapZ)
		setFreqAxis(freqTxSnap, fftMagTxSnapZ)

	if plotRxSnapSignal:
		pylab.figure(plotNumber)
		plotNumber += 1
		pylab.subplot(311)
		pylab.plot(freqRxSnap, fftMagRxSnapX)
		setFreqAxis(freqRxSnap, fftMagRxSnapX)
		pylab.title("Received Signal Snap Recon" + networkParams)
		pylab.subplot(312)
		pylab.plot(freqRxSnap, fftMagRxSnapY)
		setFreqAxis(freqRxSnap, fftMagRxSnapY)
		pylab.subplot(313)
		pylab.plot(freqRxSnap, fftMagRxSnapZ)
		setFreqAxis(freqRxSnap, fftMagRxSnapZ)
		
	if plotTxIntSignal:
		pylab.figure(plotNumber)
		plotNumber += 1
		pylab.subplot(311)
		pylab.plot(freqTxInt, fftMagTxIntX)
		setFreqAxis(freqTxInt, fftMagTxIntX)
		pylab.title("Transmitted Signal Int Recon" + networkParams)
		pylab.subplot(312)
		pylab.plot(freqTxInt, fftMagTxIntY)
		setFreqAxis(freqTxInt, fftMagTxIntY)
		pylab.subplot(313)
		pylab.plot(freqTxInt, fftMagTxIntZ)
		setFreqAxis(freqTxInt, fftMagTxIntZ)

	if plotRxIntSignal:
		pylab.figure(plotNumber)
		plotNumber += 1
		pylab.subplot(311)
		pylab.plot(freqRxInt, fftMagRxIntX)
		setFreqAxis(freqRxInt, fftMagRxIntX)
		pylab.title("Received Signal Int Recon" + networkParams)
		pylab.subplot(312)
		pylab.plot(freqRxInt, fftMagRxIntY)
		setFreqAxis(freqRxInt, fftMagRxIntY)
		pylab.subplot(313)
		pylab.plot(freqRxInt, fftMagRxIntZ)
		setFreqAxis(freqRxInt, fftMagRxIntZ)
		
	if plotTxFilteredSignal:
		pylab.figure(plotNumber)
		plotNumber += 1
		pylab.subplot(311)
		pylab.plot(freqFilteredTx, fftMagFilteredTxX)
		setFreqAxis(freqFilteredTx, fftMagFilteredTxX)
		pylab.title("Transmitted Signal Filtered" + networkParams)
		pylab.subplot(312)
		pylab.plot(freqFilteredTx, fftMagFilteredTxY)
		setFreqAxis(freqFilteredTx, fftMagFilteredTxY)
		pylab.subplot(313)
		pylab.plot(freqFilteredTx, fftMagFilteredTxZ)
		setFreqAxis(freqFilteredTx, fftMagFilteredTxZ)
		
	if plotTxFilteredSignal:
		pylab.figure(plotNumber)
		plotNumber += 1
		pylab.subplot(311)
		pylab.plot(freqFilteredRx, fftMagFilteredRxX)
		setFreqAxis(freqFilteredRx, fftMagFilteredRxX)
		pylab.title("Received Signal Filtered" + networkParams)
		pylab.subplot(312)
		pylab.plot(freqFilteredRx, fftMagFilteredRxY)
		setFreqAxis(freqFilteredRx, fftMagFilteredRxY)
		pylab.subplot(313)
		pylab.plot(freqFilteredRx, fftMagFilteredRxZ)
		setFreqAxis(freqFilteredRx, fftMagFilteredRxZ)

if plotTimeDomain or plotFreqDomain:
	pylab.show()