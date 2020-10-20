from NBodyIntegrator import NBodyIntegrator
from tree.tree import Tree
from physics import Physics
from integrators.leapfrog import Leapfrog
from time import time
if __name__ == "__main__":
	start = time()
	Tree.delta = 0.4
	physics = Physics(epsilon=0.01)
	leapfrog_integrator = Leapfrog(0.1, physics)
	integrator = NBodyIntegrator(
				timestep=0.1,
                integration_time=1000,
				n_save_points=1000,
				physics=physics,
				integrator=leapfrog_integrator)
	print("Begin integration")
	integrator.integrate()
	print("Done")
	stop = time()

	print( "elapsed time: ",(stop - start) )

