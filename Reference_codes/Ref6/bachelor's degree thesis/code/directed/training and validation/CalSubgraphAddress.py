#Author: Kai Huang
#Date: 2015.04.07

ValueMatrix = \
[
	[0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 1, 2, 4, 8, 16, 32],
	[0, 1, 0, 64, 128, 256, 512, 1024],
	[0, 2, 64, 0, 2048, 4096, 8192, 16384],
	[0, 4, 128, 2048, 0, 32768, 65536, 131072],
	[0, 8, 256, 4096, 32768, 0, 262144, 524288],
	[0, 16, 512, 8192, 65536, 262144, 0, 1048576],
	[0, 32, 1024, 16384, 131072, 524288, 1048576, 0]
]

def ArgMinAddress(adjacencyMatrix):
	kPart1 = [0, 1, 2]
	kPart2 = [3, 4, 5, 6, 7]
	k = kPart1 + kPart2
	minAddress = GetAddress(k, adjacencyMatrix)
	while True:
		kPart2 = NextPermutaion(kPart2)
		if kPart2 != None:
			k = kPart1 + kPart2
			address = GetAddress(k, adjacencyMatrix)
			if address < minAddress:
				minAddress = address
		else:
			break
	return minAddress

def GetAddress(k, adjacencyMatrix):
	address = 0.0
	for i in xrange(1, 8):
		for j in xrange(1, 8):
			address += ValueMatrix[i][j] * adjacencyMatrix[k[i]][k[j]]
	return address

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
