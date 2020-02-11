#Author: Kai Huang
#Date: 2015.04.07
import sys
import time
class Address:
	def __init__(self):
		self.valueMatrix = \
		[
			[0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 1, 2, 3, 4, 5],
			[0, 0, 0, 6, 7, 8, 9, 10],
			[0, 1, 6, 0, 11, 12, 13, 14],
			[0, 2, 7, 11, 0, 15, 16, 17],
			[0, 3, 8, 12, 15, 0, 18, 19],
			[0, 4, 9, 13, 16, 18, 0, 20],
			[0, 5, 10, 14, 17, 19, 20, 0]
		]
		self.permutation = [[3, 4, 5, 6, 7], [3, 4, 5, 7, 6], [3, 4, 6, 5, 7], [3, 4, 6, 7, 5], [3, 4, 7, 5, 6], [3, 4, 7, 6, 5], [3, 5, 4, 6, 7], [3, 5, 4, 7, 6], [3, 5, 6, 4, 7], [3, 5, 6, 7, 4], [3, 5, 7, 4, 6], [3, 5, 7, 6, 4], [3, 6, 4, 5, 7], [3, 6, 4, 7, 5], [3, 6, 5, 4, 7], [3, 6, 5, 7, 4], [3, 6, 7, 4, 5], [3, 6, 7, 5, 4], [3, 7, 4, 5, 6], [3, 7, 4, 6, 5], [3, 7, 5, 4, 6], [3, 7, 5, 6, 4], [3, 7, 6, 4, 5], [3, 7, 6, 5, 4], [4, 3, 5, 6, 7], [4, 3, 5, 7, 6], [4, 3, 6, 5, 7], [4, 3, 6, 7, 5], [4, 3, 7, 5, 6], [4, 3, 7, 6, 5], [4, 5, 3, 6, 7], [4, 5, 3, 7, 6], [4, 5, 6, 3, 7], [4, 5, 6, 7, 3], [4, 5, 7, 3, 6], [4, 5, 7, 6, 3], [4, 6, 3, 5, 7], [4, 6, 3, 7, 5], [4, 6, 5, 3, 7], [4, 6, 5, 7, 3], [4, 6, 7, 3, 5], [4, 6, 7, 5, 3], [4, 7, 3, 5, 6], [4, 7, 3, 6, 5], [4, 7, 5, 3, 6], [4, 7, 5, 6, 3], [4, 7, 6, 3, 5], [4, 7, 6, 5, 3], [5, 3, 4, 6, 7], [5, 3, 4, 7, 6], [5, 3, 6, 4, 7], [5, 3, 6, 7, 4], [5, 3, 7, 4, 6], [5, 3, 7, 6, 4], [5, 4, 3, 6, 7], [5, 4, 3, 7, 6], [5, 4, 6, 3, 7], [5, 4, 6, 7, 3], [5, 4, 7, 3, 6], [5, 4, 7, 6, 3], [5, 6, 3, 4, 7], [5, 6, 3, 7, 4], [5, 6, 4, 3, 7], [5, 6, 4, 7, 3], [5, 6, 7, 3, 4], [5, 6, 7, 4, 3], [5, 7, 3, 4, 6], [5, 7, 3, 6, 4], [5, 7, 4, 3, 6], [5, 7, 4, 6, 3], [5, 7, 6, 3, 4], [5, 7, 6, 4, 3], [6, 3, 4, 5, 7], [6, 3, 4, 7, 5], [6, 3, 5, 4, 7], [6, 3, 5, 7, 4], [6, 3, 7, 4, 5], [6, 3, 7, 5, 4], [6, 4, 3, 5, 7], [6, 4, 3, 7, 5], [6, 4, 5, 3, 7], [6, 4, 5, 7, 3], [6, 4, 7, 3, 5], [6, 4, 7, 5, 3], [6, 5, 3, 4, 7], [6, 5, 3, 7, 4], [6, 5, 4, 3, 7], [6, 5, 4, 7, 3], [6, 5, 7, 3, 4], [6, 5, 7, 4, 3], [6, 7, 3, 4, 5], [6, 7, 3, 5, 4], [6, 7, 4, 3, 5], [6, 7, 4, 5, 3], [6, 7, 5, 3, 4], [6, 7, 5, 4, 3], [7, 3, 4, 5, 6], [7, 3, 4, 6, 5], [7, 3, 5, 4, 6], [7, 3, 5, 6, 4], [7, 3, 6, 4, 5], [7, 3, 6, 5, 4], [7, 4, 3, 5, 6], [7, 4, 3, 6, 5], [7, 4, 5, 3, 6], [7, 4, 5, 6, 3], [7, 4, 6, 3, 5], [7, 4, 6, 5, 3], [7, 5, 3, 4, 6], [7, 5, 3, 6, 4], [7, 5, 4, 3, 6], [7, 5, 4, 6, 3], [7, 5, 6, 3, 4], [7, 5, 6, 4, 3], [7, 6, 3, 4, 5], [7, 6, 3, 5, 4], [7, 6, 4, 3, 5], [7, 6, 4, 5, 3], [7, 6, 5, 3, 4], [7, 6, 5, 4, 3]]
		self.addressDict = {0:0}

	def GetSubgraphAddress(self, adjacencyMatrix):
		kPart1 = [0, 1, 2]
		subgraphAddress = sys.maxint
		adjacentyMatrixAddresses = []

		for kPart2 in self.permutation:
			k = kPart1 + kPart2
			adjacentyMatrixAddress = self.GetAddress(adjacencyMatrix, k)
			adjacentyMatrixAddresses.append(adjacentyMatrixAddress)
			if adjacentyMatrixAddress < subgraphAddress:
				subgraphAddress = adjacentyMatrixAddress

		return subgraphAddress, adjacentyMatrixAddresses

	def GetAddress(self, adjacencyMatrix, k = [0, 1, 2, 3, 4, 5, 6, 7]):
		address = 0
		for i in xrange(1, 8):
			for j in xrange(i + 1, 8):
				address += adjacencyMatrix[k[i]][k[j]] << self.valueMatrix[i][j]
		return 2 * address

	def GenerateSubgraphAddressDict(self, lastI, lastJ, adjacencyMatrix):#Excluding the matrix full of 0
		for i in xrange(lastI, 8):
			for j in xrange(i + 1, 8):
				if (i == 1 and  j == 2) or (i == lastI and j <= lastJ):
					continue
				adjacencyMatrix[i][j] = 1
				adjacencyMatrix[j][i] = 1
				startTime = time.time()
				subgraphAddress, adjacentyMatrixAddresses = self.GetSubgraphAddress(adjacencyMatrix)
				for adjacentyMatrixAddress in adjacentyMatrixAddresses:
					self.addressDict[adjacentyMatrixAddress] = subgraphAddress
				endTime = time.time()
				print endTime - startTime
				self.GenerateSubgraphAddressDict(i, j, adjacencyMatrix)
				adjacencyMatrix[i][j] = 0
				adjacencyMatrix[j][i] = 0

	def GetAddressDict(self):
		return self.addressDict

	def NextPermutaion(arr):
	    if len(arr) < 2: 
	    	return arr
	    partition = -1
	    for i in range(len(arr) - 2, -1, -1):
	        if arr[i] < arr[i + 1]:
	            partition = i
	            break
	    if partition == -1: 
	    	return None
	    for i in range(len(arr) - 1, partition, -1):
	        if arr[i] > arr[partition]:
	            arr[i], arr[partition] = arr[partition], arr[i]
	            break
	    arr[partition + 1:] = arr[partition + 1:][::-1]
	    return arr
