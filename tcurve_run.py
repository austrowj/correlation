"""tcurve_run.py

Usage:
  tcurve_run.py <data_dir> <ipython_dir>
  tcurve_run.py <data_dir> --serial

Options:
  -h --help     Show this screen.
  --serial      Serial run (warning: slow)
  
Written by Sungho Hong, Computational Neuroscience Unit, Okinawa Institute of Science and Technology.
"""


def run_each(fname):
    import subprocess as sp
    import os
    NEURON = '/Applications/NEURON/nrn/x86_64/bin/nrniv'
    return sp.call([NEURON, '-python', 'tcurve_network.py', fname])


if __name__ == '__main__':
    from docopt import docopt
    from os.path import join, exists
    
    args = docopt(__doc__)
    dpath = args['<data_dir>']
    fnames = open(join(dpath,'files.txt')).read().split('\n')
    fnames = [join(dpath, fname) for fname in fnames]
    
    if args['--serial']:
        r = map(run_each, fnames)
    else:
        from IPython.parallel import Client
        ipypath = args['<ipython_dir>']
        ipypath = join(ipypath,'security','ipcontroller-client.json')
        # print ipypath + str(exists(ipypath))
        lview = Client(ipypath).load_balanced_view()
        r = lview.map_sync(run_each, fnames)
    
    for x in r:
        print x # check the result.
