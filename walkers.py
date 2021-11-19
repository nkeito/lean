import numpy as np
import emcee
from python_utils.call_lean import call_lean

#assume simple model 2 parameters
def log_prior( theta ):
	qt, crossover_tolerance = theta
	if 0<qt<=2. and 0 < crossover_tolerance < 1.0:
		return 0.0
	return -np.inf

def log_probability( theta, opt_value, project_name ):
	lp = log_prior(theta)
	if not np.isfinite( lp ):
		return -np.inf

	return lp + np.log( call_lean( project_name, opt_value, **{"qt":theta[0], "crossover_tolerance":theta[1]} ) )

def log_prior_4( theta ):
	qt, crossover_tolerance,sma_lenght_fast,sma_lenght_slow = theta
	if 0<qt<=2. and 0 < crossover_tolerance < 1.0 and 2<sma_lenght_fast<100 and 2<sma_lenght_slow<100:
		return 0.0
	return -np.inf

def log_probability_4( theta, opt_value, project_name ):
	lp = log_prior_4(theta)
	if not np.isfinite( lp ):
		return -np.inf

	return lp + np.log( call_lean( project_name, opt_value, **{"qt":theta[0], "crossover_tolerance":theta[1], "sma_lenght_fast":theta[2],"sma_lenght_slow":theta[3]} ) )


