# import pickle

# rfile = open("./temp data/PathsDict1970_1979.txt")
# test = pickle.load(rfile)
# for i in test:
# 	for j in test[i]:
# 		for path in test[i][j]:
# 			print path[0], path[-1]
# 			break

# from svmutil import *
# # Read data in LIBSVM format
# y, x = svm_read_problem('./heart_scale')
# m = svm_train(y[:200], x[:200], '-c 4')
# p_label, p_acc, p_val = svm_predict(y[200:], x[200:], m)

import pickle

rfile = open("./temp data/Vectors1970_1979")
test = pickle.load(rfile)
print test
