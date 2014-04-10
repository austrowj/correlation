"""
This is a simple clone of [PyNN](http://neuralensemble.org/PyNN/) that provides the
PyNN-like interface for setting up a simple network model in NEURON.

Written by Sungho Hong, Computational Neuroscience Unit, Okinawa Institute of Science and Technology.
"""

__version__ = '0.2'

from neuron import h

import logging
log = logging.getLogger('mypynn')

### Setting up ###
def setup(**kwargs):
    """docstring for setup"""
    h.load_file("stdrun.hoc")
    if 'gui' in kwargs and kwargs['gui']==True: 
        h.load_file("nrngui.hoc")
        from neuron import gui
    
    h.steps_per_ms = kwargs['steps_per_ms']
    h.tstop = kwargs['tstop']
    
    if kwargs['threads']>1:
        pc = h.ParallelContext()
        pc.nthread(kwargs['threads'])
    
    if 'templates' in kwargs:
        for fname in kwargs['templates']:
            h.load_file(fname)
    return h

def load_template(fname):
    h.load_file(fname)

### Run controls ###
def init():
    log.info("Initializing..")
    h.init()
    log.info("Initialized..")

def run():
    log.info("Start running..")
    h.run()
    log.info("End running..")

def nrnquit():
    h.quit()

### Network ###
class Population(object):
    def __init__(self, Ncells, cell_template, label=''):
        super(Population, self).__init__()
        self.cells = [cell_template() for i in range(Ncells)]
        self.ncells = Ncells
        self.label = label
        self.rec_cells = None
    
    def record(self, cells='all'):
        """Adds spike recorders."""
        log.info('Adding spike recorders.')
        if cells=='all':
            self.rec_cells = range(len(self.cells))
        else:
            self.rec_cells = cells
        self.apc = [(h.Vector(), 
                     h.APCount(0.5, sec=self.cells[i].soma)) 
                    for i in self.rec_cells]
        for tspike, apc in self.apc: 
            apc.thresh = -10
            apc.record(tspike)
            
    def printSpikes(self, fname=None):
        import pandas as pd
        
        spiketimes = pd.concat([pd.DataFrame({'cell':i+1,
                      'spiketime': self.apc[i][0].to_python()}) 
                          for i in range(self.ncells)])
        
        spiketimes['tstop'] = h.tstop
        if fname:
            store = pd.HDFStore(fname)
            store['spiketimes'] = spiketimes
            store.close()
        else:
            return spiketimes

### Stimulus ###
from stimulus import GaussianNoiseCurrentSource
