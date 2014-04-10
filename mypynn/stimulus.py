"""
mypynn.stimulus deals with the intracellular injection of dynamic stimuli into model neurons.

written by Sungho Hong, Computational Neuroscience Unit, Okinawa Institute of Science and Technology
"""

from neuron import h
from numpy import sqrt
import logging
log = logging.getLogger('external_stimuli')

### ###
class Clamp(object):
  def __init__(self, sec=sec):
    super(Clamp, self).__init__()
    self.pipette = None
    self._slots = {}
    self.location = '%s' % sec.name()
    for k in self.slots: self._slots[k] = None
  
  def update_stats(self, **stat):
    """ update variables about the stimulus statistics"""
    for key in stat: self.stats[key] = stat[key]
    for key in self.stats: 
      self.__dict__[key] = self.stats[key]
      log.debug('%s = %s' % (key, self.__dict__[key]))
    
    self.config_pipette()
    log.info('%s: Stimulus stats are set.' % self.location)
  
  def prepare_stim(self, slot, vec, delay=0):
    self._slots[slot] = vec
    x = eval('self.pipette._ref_%s' % slot)
    self._slots[slot].play(x, 1.0/h.steps_per_ms)
    
    if None in self._slots.values():
      for k in self._slots:
        if self._slots[k] == None:
          log.debug('WARNING: %s: the input source the for %s at is missing.' % (self.location, k))
    else: log.info('%s: All input sources are set.' % self.location)


class DynamicCurrentPatch(Clamp):
  """ Dynamic gaussian current injection via """
  slots = ['amp']
  def __init__(self, sec=sec, **stat):
    super(DynamicCurrentPatch, self).__init__(sec)
    self.pipette = h.CIClamp(0.5, sec=sec)
    self.stats = {'mu':0., 'sigma':1., 'tcorr':5.} # default
    self.update_stats(**stat)
  
  def config_pipette(self):
    self.pipette.mu = self.mu
    self.pipette.gain = self.sigma*sqrt(2.0*h.steps_per_ms/self.tcorr) # correct sigma for steps_per_ms.


class GaussianNoiseCurrentSource(object):
    def __init__(self, **kwargs):
        super(GaussianNoiseCurrentSource, self).__init__()
        for k in kwargs: self.__dict__[k] = kwargs[k]
        self.randgen = h.Random(self.seed)
        self.randgen.normal(0.0, 1.0)
        self.signal = h.Vector(int(self.stop*h.steps_per_ms)) # prepare the vectors to play.
        self.signal.setrand(self.randgen) # assign the random number genetor to the vectors.
        self.electrodes = []
        
    def inject(self, cell):
        self.electrodes.append(DynamicCurrentPatch(cell.soma)) # somatic injection
        self.electrodes[-1].update_stats(
            mu=self.mu, 
            sigma=self.sigma,
            delay=self.start,
            stop =self.stop,
            tcorr=self.tcorr
        ) #update stats
        self.electrodes[-1].prepare_stim('amp', self.signal)
    
    def update_stats(self, **stat):
        for key in stat:
          self.__dict__[key] = stat[key]
        for x in self.electrodes: x.update_stats(**stat)
