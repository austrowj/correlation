TITLE Dynamic current injection with temporal correlation.

COMMENT
This model implements the current injection with the exponentially filtered signal amp with the time constant tcorr. If amp is the Gaussian noise, the current will become a Ornstein-Uhlenbeck process if the gain is appropriately scaled as sigma*sqrt(2.0*h.steps_per_ms/tcorr) where sigma and steps_per_ms are the stdev and update frequency of the noise. Also, one can add a DC component given by mu.

Written by Sungho Hong, Computational Neuroscience Unit, Okinawa Institute of Science and Technology.
ENDCOMMENT

NEURON {
	POINT_PROCESS CIClamp
	RANGE amp, i, n, tcorr, mu, gain
	ELECTRODE_CURRENT i
  THREADSAFE
}

UNITS {
	(nA) = (nanoamp)
}

PARAMETER {
	amp (nA)
	tcorr = 5 (ms)
	mu = 0 (nA)
	gain = 1
}

ASSIGNED { i (nA) }

STATE { n }

INITIAL {
	i = 0
}

BREAKPOINT {
  SOLVE states METHOD cnexp
  i = n + mu : DC current mu is simply added.
}

DERIVATIVE states {
  n' = -n/tcorr + gain*amp
}
