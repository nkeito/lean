import emcee
import corner

if __name__ == '__main__':
	filename = "tutorial.h5"
	reader = emcee.backends.HDFBackend(filename)
	samples = reader.get_chain(discard=100, flat=True, thin=15)
	print("flat chain shape: {0}".format(samples.shape))
	fig = corner.corner(samples, labels=["qt","crossover_tolerance"], truths=[.5, 1.]);
	fig.savefig( "test.png" )
