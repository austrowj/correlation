"""tcurve_stats.py

Usage:
  tcurve_stats.py <stat> <save_file> <data_dir> <ipython_dir>
  tcurve_stats.py <stat> <save_file> <data_dir> --serial

Options:
  -h --help     Show this screen.
  --serial      Serial run

Written by Sungho Hong, Computational Neuroscience Unit, Okinawa Institute of Science and Technology.
"""

def compute_rate_each(fname):
    import pandas as pd
    import data_model as dm
    index = pd.HDFStore(fname)['spec'].index[0]
    x  = pd.HDFStore(fname)['spiketimes']    
    y = dm.PSTH(x)
    return (index, y.rate)

def compute_xcov_each(fname):
    import pandas as pd
    import data_model as dm
    import data_model.timewindow as tw
    from numpy import dot
    
    index = pd.HDFStore(fname)['spec'].index[0]
    x  = pd.HDFStore(fname)['spiketimes']    
    y = dm.PSTH(x)
    
    ccg = y.ccf(max_shift=2)
    ccv = dot(ccg, tw.triangle(200,401))
    
    return (index, ccv)

def compute_acov_each(fname):
    import pandas as pd
    import data_model as dm
    import data_model.timewindow as tw
    from numpy import dot
    
    index = pd.HDFStore(fname)['spec'].index[0]
    x  = pd.HDFStore(fname)['spiketimes']    
    y = dm.PSTH(x)
    
    ccg = y.acf(max_shift=2)
    ccv = dot(ccg, tw.triangle(200,401))
    
    return (index, ccv)

def compute_pcov_each(fname):
    import pandas as pd
    import data_model as dm
    reload(dm)
    import data_model.timewindow as tw
    from numpy import dot, convolve
    import os
    from scipy.signal import resample
    
    index = pd.HDFStore(fname)['spec'].index[0]
    Fs = pd.HDFStore(fname)['spec'].iloc[0]['Fs']
    c = pd.HDFStore(fname)['spec'].iloc[0]['c']
    dname = os.path.dirname(fname)
    x  = pd.HDFStore(fname)['spiketimes']
    y = dm.PSTH(x)
    s = pd.HDFStore(os.path.join(dname, 'noises.h5'))['noise']
    sta = y.spike_triggered(s, Fs)
    ccx = convolve(sta[::-1],sta)
    ccx = resample(ccx, 401)
    ccx = ccx*y.rate*y.rate*1e-6*c
    pcv = dot(ccx, tw.triangle(200,401))
    
    return (index, pcv)


if __name__ == '__main__':
    from docopt import docopt
    from os.path import join, exists
    import pandas as pd
    
    args = docopt(__doc__)
    stat = args['<stat>']
    dpath = args['<data_dir>']
    savefile = args['<save_file>']
    
    fnames = open(join(dpath,'files.txt')).read().split('\n')
    fnames = [join(dpath, fname) for fname in fnames]
    
    if 'h5' not in savefile: savefile = savefile + '.h5'
    if not exists(savefile):
        f = pd.HDFStore(savefile, 'w')
        f['stats'] = pd.concat([pd.HDFStore(fname)['spec'] for fname in fnames])
        f.flush()
        f.close()
    
    f = pd.HDFStore(savefile, 'r+')
    stats = f['stats']
    stats[stat] = pd.np.NaN
    
    if stat == 'rate':
        fcomp = compute_rate_each
    if stat == 'xcov':
        fcomp = compute_xcov_each
    if stat == 'acov':
        fcomp = compute_acov_each
    if stat == 'pcov':
        fcomp = compute_pcov_each
    
    if args['--serial']:
        rvs = map(fcomp, fnames)
    else:
        from IPython.parallel import Client
        ipypath = args['<ipython_dir>']
        ipypath = join(ipypath,'security','ipcontroller-client.json')
        lview = Client(ipypath).load_balanced_view()
        rvs = lview.map_sync(fcomp, fnames)
    
    for i, s in rvs:
        stats[stat][i] = s
    
    f['stats'] = stats
    print f['stats']
    
    f.close()
        