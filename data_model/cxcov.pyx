#cxcov.pyx contains xcorr3 that computes the unbiased cross-correlogram strictly according to the definition.
#
#Written by Sungho Hong, Computational Neuroscience Unit, Okinawa Institute of Science and Technology.

import numpy as np
cimport numpy as np
cimport cython

DTYPE = np.double
ctypedef np.double_t DTYPE_t

@cython.boundscheck(False)
def xcorr3(np.ndarray[DTYPE_t, ndim=1] a, np.ndarray[DTYPE_t, ndim=1] b, unsigned int L=200):
  cdef unsigned int N = a.size
  cdef unsigned int LL = 2*L + 1
  cdef int i
  cdef int j
  cdef np.ndarray[DTYPE_t, ndim=1] c = np.zeros(LL, dtype=DTYPE)

  for j in range(L):
    i = -j-1
    c[<unsigned int>(i+L)] = np.dot(a[0:<unsigned int>(N+i)], b[<unsigned int>(-i):N])/(N+i)
    i = j+1
    c[<unsigned int>(i+L)] = np.dot(a[<unsigned int>(i):N], b[0:<unsigned int>(N-i)])/(N-i)
  
  c[L] = np.dot(a, b)/N
  
  return c
