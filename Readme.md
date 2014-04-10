This is a cleaned-up version of the model, simulation, and analysis codes for our publication:

Hong, S., Ratté, S., Prescott, S.A., and De Schutter, E. (2012). Single neuron firing properties impact correlation-based population coding. J Neurosci 32, 1413–1428. ([pubmed link](http://www.ncbi.nlm.nih.gov/pubmed/22279226))

The codes here are particularly about Figure 3A. Other simulations in the paper can be done by simple modifications mostly in the configuration part.


### Dependence

* NEURON + Python
* Cython

and Python modules,

* ipython (>0.13, with the parallel computing modules)
* numpy
* scipy.signal
* pandas (with HDF support)
* docopt

### Preparation

1. Compile the mod files and copy the relevant files so that NEURON can load the mechanisms in the top directory.
2. Go to data_model directory and run

~~~
python setup.py build_ext --inplace
~~~

### How to run the simulation

1. Create a directory that the data will be saved.
2. Make a list of simulation parameters as in tcurve_config.py and run it.
3. Run the simulations with tcurve_run.py
4. Run tcurve_stats.py to compute the firing rate, auto- and cross-correlation, prediction for cross-correlation.

### Example

~~~
# First, we start the ipython parallel computing with 10 nodes.
$ ipcluster --n=10 --profile=mpi --profile-dir=IPYDIR &                      
$ mkdir data_hhls_highvar  # Make a directory to contain the data.
$ python tcurve_config.py data_hhls_highvar  # Prepare the directory for simulation.
$ python tcurve_run.py data_hhls_highvar IPYDIR  # Run the simulations
$ python tcurve_stats.py rate hhls_highvar.h5 IPYDIR # Compute firing rates.
$ python tcurve_stats.py xcov hhls_highvar.h5 IPYDIR # Compute cross-covariances.
$ python tcurve_stats.py acov hhls_highvar.h5 IPYDIR # Compute auto-covariances.
$ python tcurve_stats.py pcov hhls_highvar.h5 IPYDIR # Compute the STA predictions of the cross-covariances.
~~~

All the codes are written by Sungho Hong, Computational Neuroscience Unit, Okinawa Institute of Science and Technology.
