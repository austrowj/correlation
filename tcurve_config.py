"""tcurve_config.py

Usage:
  tcurve_config.py <data_dir>

Options:
  -h --help     Show this screen.

Written by Sungho Hong, Computational Neuroscience Unit, Okinawa Institute of Science and Technology.
"""


from numpy import linspace, sqrt
import pandas as pd

def generate_data_filename(x):
    import datetime, random
    return datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f') + ('+%d' % x)

### High var ML
# params = [pd.DataFrame({'c':0.3, 
#                         'mu': m,
#                         'sigma': sqrt(0.0004),
#                         'tcorr':5.0,
#                         'tstop': 180100,
#                         'Fs':5}, index=[ind]) 
#           for ind, m in enumerate(linspace(0.33, 0.4, 20))]

### Low var ML
# params = [pd.DataFrame({'c':0.3, 
#                         'mu': m,
#                         'sigma': sqrt(0.0001),
#                         'tcorr':5.0,
#                         'tstop': 180100,
#                         'Fs':5}, index=[ind]) 
#           for ind, m in enumerate(linspace(0.35, 0.384, 20))]
 
### Low var HHLS
# params = [pd.DataFrame({'c':0.3, 
#                         'mu': m,
#                         'sigma': sqrt(0.00052),
#                         'tcorr':5.0,
#                         'tstop': 180100,
#                         'Fs':5}, index=[ind]) 
#           for ind, m in enumerate(linspace(-0.1, 0.045, 30))]

### High var HHLS
params = [pd.DataFrame({'c':0.3, 
                        'mu': m,
                        'sigma': sqrt(0.002),
                        'tcorr':5.0,
                        'tstop': 180100,
                        'Fs':5}, index=[ind]) 
          for ind, m in enumerate(linspace(-0.15, 0.16, 30))]

if __name__ == '__main__':
    from docopt import docopt
    from os.path import join
    args = docopt(__doc__)
    
    fnames = [generate_data_filename(p.index[0])+'.h5' for p in params]
    for i, fname in enumerate(fnames):
        f = pd.HDFStore(join(args['<data_dir>'], fname))
        f['spec'] = params[i]
        f.flush()
        f.close()
    
    open(join(args['<data_dir>'],'files.txt'), 'w').write('\n'.join(fnames))
