"""
cgmutil.py

Written by Sungho Hong, Computational Neuroscience Unit, Okinawa Institute of Science and Technology.
"""

import cxcov
from numpy import array, zeros, arange, newaxis, roll
from numpy import sort, cov, sqrt, convolve

import logging
log = logging.getLogger('data_processing')

def cgm_shift(x1, x2, L=200, shift=250, max_shift=10):
  Nshift = min(x1.size/shift, max_shift)
  cs = cxcov.xcorr3(x1, x2, L=L)
  es = array([cxcov.xcorr3(x1, roll(x2,-shift*(i+1)), L=L) for i in range(Nshift)])
  esm = es.mean(axis=0)
  # esv = es.var(axis=0)
  return cs, esm

def cgm_bulk(x, L=200, shift=250, max_shift=10, pview=None):
  xs = x.sum(axis=0)
  ccs, ees = cgm_shift(xs, xs, L=L, shift=shift, max_shift=max_shift)
  nn = x.shape[0]    
  for i in range(nn):
    ccd, eed = cgm_shift(x[i], x[i], L=L, shift=shift, max_shift=max_shift)
    ccs = ccs-ccd
    ees = ees-eed
  nn = nn*(nn-1.0)
  return ccs/nn, ees/nn

def acgm_bulk(x, L=200, shift=250, max_shift=10, pview=None):
  xs = x.sum(axis=0)
  nn = x.shape[0]
  ccs = 0.
  ees = 0.
  for i in range(nn):
    ccd, eed = cgm_shift(x[i], x[i], L=L, shift=shift, max_shift=max_shift)
    ccs = ccs+ccd
    ees = ees+eed
  return ccs/nn, ees/nn

def compute_sta(tspike, stim, window_size=2000):
  tspike0 = tspike[tspike>window_size]
  tspike0 = tspike0[tspike0<stim.size-2]
  c = tspike0[:,newaxis] + arange(-window_size,1)[newaxis,:]
  sts = stim[c]
  if len(tspike0)>0:
    return sts.mean(axis=0), tspike0.size
  else: return 0.0, 0

def compute_stc(tspike, stim, window_size=2000):
  from numpy.random import random_integers
  tspike0 = tspike[tspike>window_size]
  tspike0 = tspike0[tspike0<stim.size-2]
  stimn = stim/stim.std()
  ind_prior = sort(random_integers(window_size, high=tspike0.max(), size=tspike0.size))
  # print stimn.std()
  stc = cov(array([stimn[k-window_size:k+1] for k in tspike0]).T)-cov(array([stimn[k-window_size:k+1] for k in ind_prior]).T)
  return stc

