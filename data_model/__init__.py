"""
data_model implements PSTH class used for data processing.

Written by Sungho Hong, Computational Neuroscience Unit, Okinawa Institute of Science and Technology.
"""

__version__ = '0.2'

import pandas as pd
from numpy import array, zeros, arange, allclose
import cgmutil
reload(cgmutil)
from cgmutil import cgm_bulk, acgm_bulk

import logging
log = logging.getLogger('data_processing')

class PSTH(object):
  def __init__(self, spiketimes, dt=1.0):
    """PSTH(spiketimes, dt)"""
    self.spiketimes = spiketimes
    
    dt = float(dt)
    cells = spiketimes.cell.unique()
    tstop = spiketimes.tstop.iloc[0]
    x = zeros((int(tstop/dt), cells.size))
    x = pd.DataFrame(x, columns=cells, index=arange(0,x.shape[0])*dt)
    spikeindex = (spiketimes.spiketime/float(dt)).astype(int)
    for i in cells:
      x[i][spikeindex[spiketimes.cell==i]] = 1
    
    self._spiketrains = x
    self.cells = cells
    self.tstop = tstop
    
  def plot_raster(self, axes):
    axes.plot(self.spiketimes.spiketime, self.spiketimes.cell, '.k', ms=2.0)
    for direction in ("right", "top"):
      axes.spines[direction].set_visible(False)
    axes.get_xaxis().tick_bottom()
    axes.get_yaxis().tick_left()
    # axesylabel("Neuron id")  
    axes.set_xlim([0, self.tstop])
      
  @property
  def spiketrains(self):
    return self._spiketrains
  
  def ccf(self, L=200, shift=250, max_shift=10, pview=None):
    x0, xp0 = cgm_bulk(array(self.spiketrains).T,
                       L=L, 
                       shift=shift, 
                       max_shift=max_shift,
                       pview=pview)
    return x0 - xp0

  def acf(self, L=200, shift=250, max_shift=10, pview=None):
    from cgmutil import acgm_bulk
    x0, xp0 = acgm_bulk(array(self.spiketrains).T,
                        L=L, 
                        shift=shift, 
                        max_shift=max_shift,
                        pview=pview)
    return x0 - xp0
  
  def spike_triggered(self, signal, Fs, L=200):
    from cgmutil import compute_sta
    
    if int(self.tstop*Fs) != signal.shape[0]: raise RuntimeError
    wsize = int(L*Fs);
    n = 0
    sta = 0.0
    
    for i in self.cells:
      spiketimes_this_cell = self.spiketimes[self.spiketimes.cell==i].spiketime
      log.debug(str(spiketimes_this_cell))
      log.debug('Fs = ' + str(Fs))
      spikeindex = (self.spiketimes[self.spiketimes.cell==i].spiketime*Fs)
      log.debug(str(spikeindex))
      spikeindex = spikeindex.astype(int)
      sta1, n1 = compute_sta(spikeindex.values, signal[i].values, window_size=wsize)
      n = n + n1
      sta = sta + float(n1)/n*(sta1-sta)
    
    self.sta = sta  
    return sta
  
  @property
  def rate(self):
    nspikes = float(self.spiketimes.shape[0])
    return nspikes/self.tstop/self.cells.size*1e3
  
  def spike_rate(self, span=6, smoothed=True):
    from numpy import convolve, ones
    spike_rate_raw = self.spiketrains.sum(axis=1)
    if smoothed==False:
      spike_rate = spike_rate_raw
    else:
      window = ones(span)/span
      spike_rate = convolve(window, spike_rate_raw, mode="same")
    return spike_rate
  

