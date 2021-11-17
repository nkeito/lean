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