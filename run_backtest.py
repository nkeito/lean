#from python_utils.call_lean import call_lean
import emcee
import corner
import numpy as np
from python_utils.walkers import log_probability
import multiprocessing
from multiprocessing import Pool, cpu_count

if __name__ == '__main__':
	
	pos = np.array([1.,.5]) + 1e-4 * np.random.randn(32, 2)

	nwalkers, ndim = pos.shape

	project_name = "sma_oct27"
	opt_value = "compounding_annual_return"

	
	filename = "tutorial.h5"
	backend = emcee.backends.HDFBackend(filename)
	backend.reset(nwalkers, ndim)

	sampler = emcee.EnsembleSampler(
    			nwalkers, ndim, log_probability, args=(opt_value,project_name), backend=backend
    		)
	sampler.run_mcmc(pos, 500, progress=True);

	flat_samples = sampler.get_chain(discard=50, thin=15, flat=True)

	fig = corner.corner( flat_samples, labels=["qt","crossover"], truths=[1., .5])
	fig.show()
	fig.savefig("test.png")


	"""
	with Pool() as pool:
		pos = np.array([1.,.5]) + 1e-4 * np.random.randn(32, 2)

		filename = str(multiprocessing.current_process().name)+"_"+"tutorial.h5"
		backend = emcee.backends.HDFBackend(filename)
		backend.reset(nwalkers, ndim)


		sampler = emcee.EnsembleSampler(
    			nwalkers, ndim, log_probability, pool=pool,args=(opt_value,project_name), backend=backend
    		)
		sampler.run_mcmc(pos, 500, progress=True);
		flat_samples = sampler.get_chain(discard=50, thin=15, flat=True)
		fig = corner.corner( flat_samples, labels=["qt","crossover"], truths=[1., .5])
		fig.show()
		fig.savefig("test.png")
	
	"""


	


