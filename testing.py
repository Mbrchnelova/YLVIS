import math


def get_nondoubhyptng(stretching_factor, index_vector, interval, N):
        I = interval
        zeta = float(index_vector)/ float(N)
        delta = stretching_factor

	s = 1.0 + math.tanh(delta*(zeta/I - 1.0))/math.tanh(delta)
	
        return s 


def get_hyptng(stretching_factor, index, interval, N):
	I = interval
	#si = 1.0 - math.tanh(stretching_factor * (1.0 - 2.0*float(index)/float(N))) / math.tanh(stretching_factor)
	zeta = float(index)/float(N)
        s = 1.0/2.0 * (1.0 + math.tanh(stretching_factor * (zeta/I - 1.0/2.0)) / math.tanh(stretching_factor/2.0))

	return s

stretching_factor = 2.750
xmax = 1.0
xmin = 0.0

s = 0.0
x = 0.0
N = 50
for i in range(0, N):
	index = float(i)
	interval = xmax - xmin
	s = get_hyptng(stretching_factor, index, interval, N)
	#print s


	s1 = get_nondoubhyptng(stretching_factor, index, interval, N)
	print i, ",", s, ",", s1
