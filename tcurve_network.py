"""tcurve_network.py

Construction of the network and simulation.

Written by Sungho Hong, Computational Neuroscience Unit, Okinawa Institute of Science and Technology.
"""
from mypynn import *

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger('network building')

def main(fname):
    import numpy as n
    import pandas as pd
    
    f = pd.HDFStore(fname)
    spec = f['spec'].iloc[0]  # load the specifications for the simulation and network.
    
    if f['spec'].index[0] == 0: # Only one simuation will save the noise. 
        save_noise = True
    else:
        save_noise = False
    
    setup(steps_per_ms = 5,
              tstop = spec['tstop'],
              threads = 1,
              gui=True,
              templates = ['cell_templates/current_driven_cells.hoc'])
    
    log.info('Building cells.... Wait.')
    Ncell = 100
    p = Population(Ncell, h.L1ML)     # for the integrator
    # p = Population(Ncell, h.L1HHLS) # for the coincidence detector
    log.info('Done making cells.')

    cin = spec['c']
    sigmatot = spec['sigma']
    stim_gen = lambda x, m, s: GaussianNoiseCurrentSource(
                        seed=x,
                        mu=m,
                        sigma=s,
                        tcorr=spec['tcorr'],
                        start=0,
                        stop=h.tstop) # generator for the Guassian noise
    
    indv_stims = [stim_gen(i+2, 0, n.sqrt(1-cin)*sigmatot)
                          for i in range(p.ncells)] # individual noise. Seed = 2..Ncell+2
    
    common_stim = stim_gen(1, spec['mu'], n.sqrt(cin)*sigmatot) # common noise. Seed=1
    
    for s, c in zip(indv_stims, p.cells): s.inject(c)
    for c in p.cells: common_stim.inject(c)
    p.record()
    
    init()
    run()
    
    spikes = p.printSpikes()
    log.info('Getting all the spikes')
    
    cells = n.arange(Ncell)+1
    
    f['spiketimes'] = spikes
    f.flush()
    f.close()
    
    if save_noise:
        import os
        from numpy import array, sqrt
        noisei = pd.DataFrame(array([x.signal.to_python() for x in indv_stims]).T, columns=cells)
        noisec = pd.DataFrame(common_stim.signal.to_python())
        noise = pd.DataFrame(sqrt(1-cin)*noisei.values + sqrt(cin)*noisec.values, 
                             noisei.index, noisei.columns) # Noise normalized by the stdev
        
        log.info('Getting the noises')
        f = pd.HDFStore(os.path.join(os.path.dirname(fname), 'noises.h5'))
        f['noise'] = noise
        f.flush()
        f.close()

if __name__ == '__main__':
    import sys
    fname, = [x for x in sys.argv if '.h5' in x] # Get the name of the file with specifications.
    log.info('Processing %s' % fname)
    main(fname)
    nrnquit()
