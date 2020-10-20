from NBodyIntegrator import NBodyIntegrator
from tree.tree import Tree
from physics import Physics
from integrators.leapfrog import Leapfrog
from time import time

if __name__ == "__main__":
	Tree.delta = 0.4
	epsilon = 0.01
	timestep = 0.1
	integration_time = 1000
	n_save_points = 1000

	start = time()

	physics = Physics(epsilon=0.01)
	leapfrog_integrator = Leapfrog(timestep, physics)
	integrator = NBodyIntegrator(
				timestep=timestep,
                integration_time=integration_time,
				n_save_points=n_save_points,
				physics=physics,
				integrator=leapfrog_integrator,
				input_file="resources/input_100p.txt")

	print("Begin integration")
	integrator.integrate()
	print("Done")
	stop = time()

	print( f"elapsed time: {(stop - start)}s" )

