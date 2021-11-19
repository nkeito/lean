#from python_utils.call_lean import call_lean
import emcee
import sys
import corner
import numpy as np
from python_utils.walkers import log_probability, log_probability_4
import multiprocessing
from schwimmbad import MPIPool
from multiprocessing import Pool

if __name__ == '__main__':
	
	

	project_name = "sma_oct27"
	opt_value = "compounding_annual_return"
	nwalkers = 32
	walks = 500


	


	with Pool(processes=4) as pool:


		pos = np.array([1.,.5,11,40]) + 1e-4 * np.random.randn(nwalkers, 4)
		nwalkers, ndim = pos.shape

		filename = 	"4_dims_history.h5"
		backend = emcee.backends.HDFBackend(filename)
		backend.reset(nwalkers, ndim)

		sampler = emcee.EnsembleSampler(
				nwalkers, ndim, log_probability_4, pool=pool,args=(opt_value,project_name), backend=backend
			)
		sampler.run_mcmc(pos, walks, progress=True);
	
	flat_samples = sampler.get_chain(discard=50, thin=15, flat=True)
	fig = corner.corner( flat_samples, labels=["qt","crossover_tolerance", "sma_lenght_fast","sma_lenght_slow"], truths=[1., .5,11,40])
	fig.show()
	fig.savefig("test.png")
	
	#
	"""
	with MPIPool() as pool:

		if not pool.is_master():
			pool.wait()
			sys.exit(0)
		

		pos = np.array([1.,.5]) + 1e-4 * np.random.randn(nwalkers, 2)
		nwalkers, ndim = pos.shape

		filename = "_tutorial.h5"
		backend = emcee.backends.HDFBackend(filename)
		backend.reset(nwalkers, ndim)

		sampler = emcee.EnsembleSampler(
    			nwalkers, ndim, log_probability, args=(opt_value,project_name), backend=backend, pool=pool
    		)
		
		sampler.run_mcmc(pos, walks, progress=True);

		flat_samples = sampler.get_chain(discard=50, thin=15, flat=True)

	
		

	

	

	fig = corner.corner( flat_samples, labels=["qt","crossover"], truths=[1., .5])
	fig.show()
	fig.savefig("test.png")
	"""



	


