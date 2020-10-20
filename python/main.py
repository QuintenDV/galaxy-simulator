from NBodyIntegrator import NBodyIntegrator
from tree.tree import Tree
from physics import Physics
from time import time
if __name__ == "__main__":
	start = time()
	Tree.delta = 0.4
	physics = Physics(epsilon=0.01)
	integrator = NBodyIntegrator(
				timestep=0.1,
                integration_time=1000,
				n_save_points=1000,
				physics=physics)
	print("Begin integration")
	integrator.integrate()
	print("Done")
	stop = time()

	print( "elapsed time: ",(stop - start) )

