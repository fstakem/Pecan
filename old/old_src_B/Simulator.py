#!/usr/bin/env python
# encoding: utf-8
"""
Simulator.py

Created by Fredrick Stakem on 2010-03-12.
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
from SnapLimitReconstructor import SnapLimitReconstructor
from IntReconstructor import IntReconstructor

# Globals
InterpolationType = Enum( 'Time', 'Distance' )

# Output function
def exportData(filename, data):
	file = open(filename, 'w')
	for sample in data:
		file.write(str(sample) + "\n")
	file.close()
	
# Split up data
def splitData(data):
	time = []
	x = []
	y = []
	z = []
	for sample in data:
		time.append(sample.time)
		x.append(sample.position.x)
		y.append(sample.position.y)
		z.append(sample.position.z)
		
	return [time, x, y, z]
	
# Find the distance error
def findDistanceError(dataSetA, dataSetB):
	error = []
	setA, setB = stripFront(dataSetA, dataSetB)
	setA, setB = stripEnd(setA, setB)

	if len(setA) != len(setB):
		print "Error: the lists are not the same length."
		
	for i, sample in enumerate(setA):
		error.append( abs( setA[i].distance(setB[i]) ) )

	return error
	
def findDistanceBetweenSamples(dataSet, threshold, spacing):
	jump = []
	for i in range(spacing, len(dataSet)):
		distance = dataSet[i].distance(dataSet[i-spacing])
		if distance > threshold:
			jump.append(distance)
		
	return jump
	
def findCorrelation(dataSetA, dataSetB):
	correlation = []
	result = stripFront(dataSetA, dataSetB)
	result = stripEnd(result[0], result[1])

	if len(result[0]) != len(result[1]):
		print "Error: the lists are not the same length."

	setA = splitData(result[0])
	setB = splitData(result[1])
	correlationX = scipy.signal.correlate(setA[1], setB[1])
	correlationY = scipy.signal.correlate(setA[2], setB[2])
	correlationZ = scipy.signal.correlate(setA[3], setB[3])
		
	return [correlationX, correlationY, correlationZ]
	
def calculateStats(dataSet):
	if type(dataSet) != numpy.ndarray:
		dataSet = numpy.array(dataSet)
	
	mean = dataSet.mean()
	std = dataSet.std()
	median = numpy.median(dataSet)
	
	return (mean, std, median)
	
def stripFront(dataSetA, dataSetB):
	timeA = dataSetA[0].time
	timeB = dataSetB[0].time
	setA = dataSetA
	setB = dataSetB
	if timeA > timeB:
		i = 0
		while dataSetB[i].time != timeA and i < len(dataSetB) - 1:
			i += 1
		setB = dataSetB[i:]
	elif timeA < timeB:
		i = 0
		while dataSetA[i].time != timeB and i < len(dataSetA) - 1:
			i += 1
		setA = dataSetA[i:]
		
	return [setA, setB]
	
def stripEnd(dataSetA, dataSetB):
	timeA = dataSetA[-1].time
	timeB = dataSetB[-1].time
	setA = dataSetA
	setB = dataSetB
	if timeA > timeB:
		i = -1
		while dataSetA[i].time != timeB:
			i -= 1
		setA = dataSetA[:i+1]
	elif timeA < timeB:
		i = -1
		while dataSetB[i].time != timeA:
			i -= 1
		setB = dataSetB[:i+1]
		
	return [setA, setB]
	
# Perform the fft
def fft(data, inDb):
	fftData = scipy.fft(data)
	freq = len(data) * scipy.fftpack.fftshift( scipy.fftpack.fftfreq( len(data) ) )
	freq = freq.tolist()
	fftMag = 2 * scipy.fftpack.fftshift( abs(fftData) ) / len(fftData)
	fftPhase = numpy.arctan2(fftData.imag, fftData.real) * (180/math.pi)
	
	if inDb:
		fftMag = 20 * scipy.log10(fftMag)
		
	return [freq, fftMag, fftPhase]
	
def amplifyData(data, gain):
	amplifiedData = []
	for sample in data:
		newSample = Sample(sample)
		newSample.position.x *= gain
		newSample.position.y *= gain
		newSample.position.z *= gain
		amplifiedData.append(newSample)
		
	return amplifiedData
	
# Crop data to bounds	
def cropData(x, y, lowerBound, upperBound):
	if len(x) != len(y):
		print "Error: lists must be of same length"
		return
		
	lowerIndex = 0
	upperIndex = len(x)
	lowerDiff = abs(x[0] - x[1]) * 100
	upperDiff = abs(x[0] - x[1]) * 100
	
	for i, v in enumerate(x):
		diff = abs(lowerBound - v)
		if diff < lowerDiff:
			lowerDiff = diff
			lowerIndex = i
			
		diff = abs(upperBound - v)
		if diff < upperDiff:
			upperDiff = diff
			upperIndex = i
	
	return [ x[lowerIndex:upperIndex], y[lowerIndex:upperIndex] ]
	
# Main simulator	
def transmitData(inputFile, logDir, predictionInterval, samplingInterval, 
                 heartbeat, drThreshold, delay, jitter, packetLoss):
	# Import data
	print "Importing data..."
	importer = Importer()
	rawInputData = importer.getInputData(inputFile, samplingInterval)
	exportData(logDir + "RawInputData.txt", rawInputData)
	
	# Filtering input data
	print "Filtering data..."
	samplingFreq = int(1e3/samplingInterval)
	taps = 80
	bands = [0.0, 10, 11, 50.0]
	weights = [1, 0]
	coefficients = scipy.signal.remez(taps, bands, weights, Hz=samplingFreq)
	gain = 1.0 / sum(coefficients)
	filteredInputData = filterData(rawInputData, logDir, "cc", samplingInterval, coefficients)[0]
	filteredInputData = amplifyData(filteredInputData, gain)
	exportData(logDir + "FilteredInputData.txt", filteredInputData)

	# Create the prediction vectors
	print "Creating the prediction vectors..."
	predictor = DRPredictor()
	predictedData = predictor.getPredictedData(filteredInputData, predictionInterval, samplingInterval)
	exportData(logDir + "PredictionData.txt", predictedData)

	# Run the transmission algorithm
	print "Simulating the transmission algorithm..."
	transmitter = DRTransmitter(heartbeat)
	drTxPackets = transmitter.getTransmittedPackets(drThreshold, predictedData)
	exportData(logDir + "DRTxPackets.txt", drTxPackets)

	# Simulate the transmission of the packets
	print "Simulating the network..."
	network = Network()
	drRxPackets = network.getReceivedPackets(drTxPackets, delay, jitter, packetLoss)
	exportData(logDir + "DRRxPackets.txt", drRxPackets)

	# Receive the packets
	print "Receiving the packets..."
	receiver = Receiver()
	drRxFilteredPackets = receiver.getFilteredData(drRxPackets)
	exportData(logDir + "DRRxData.txt", drRxFilteredPackets)

	return [rawInputData, filteredInputData, predictedData, drTxPackets, 
	        drRxPackets, drRxFilteredPackets]

def snapReconstructData(packetData, logDir, fileEnding, samplingInterval):
	# Snap reconstruct the transmitted and received data
	print "Snap reconstructing the signals..."
	snapReconstructor = SnapReconstructor()
	snapData = snapReconstructor.getReconstructedSignal(packetData, samplingInterval)
	exportData(logDir + "SnapData_" + fileEnding + ".txt", snapData)
	
	return [snapData]
	
def snapLimitReconstructData(packetData, logDir, fileEnding, samplingInterval, 
						     interpolationType, reconThreshold, snapLimit):
	# Snap limit reconstruct the transmitted and received data
	print "Snap limit reconstructing the signals..."
	snapLimitReconstructor = SnapLimitReconstructor()
	snapData = snapLimitReconstructor.getReconstructedSignal(packetData, samplingInterval,
	 														 interpolationType, reconThreshold,
															 500, snapLimit)
	exportData(logDir + "SnapLimitData_" + fileEnding + ".txt", snapData)
	
	return [snapData]
	
def filterData(reconData, logDir, fileEnding, samplingInterval, coefficients):
	# Filter the reconstructed data
	print "Filtering the data..."
	filteredData = []
	time, x, y, z = splitData(reconData)
	xFiltered = scipy.signal.convolve(coefficients, x)
	yFiltered = scipy.signal.convolve(coefficients, y)
	zFiltered = scipy.signal.convolve(coefficients, z)
	
	numberToDrop = len(coefficients) - 1
	time = time[numberToDrop:]
	xFiltered = xFiltered[numberToDrop:]
	yFiltered = yFiltered[numberToDrop:]
	zFiltered = zFiltered[numberToDrop:]
	
	for i, v in enumerate(time):
		sample = Sample()
		sample.time = time[i]
		sample.position.x = xFiltered[i]
		sample.position.y = yFiltered[i]
		sample.position.z = zFiltered[i]
		filteredData.append(sample)
	
	filteredData = filteredData[:-200]
	exportData(logDir + "FilteredData_" + fileEnding + ".txt", filteredData)
	
	return [filteredData]
	
def convergeData(packetData, logDir, fileEnding, samplingInterval,
  			     interpolationType, reconThreshold):
	# Interpolation reconstruct the transmitted and received data
	print "Interpolation reconstructing the signals..."
	intReconstructor = IntReconstructor()
	convergedData = intReconstructor.getReconstructedSignal(packetData, samplingInterval, 
	    												    interpolationType, reconThreshold, 500)
	exportData(logDir + "ConvergedData_" + fileEnding + ".txt", convergedData)
	
	return [convergedData]
	
	
	
	