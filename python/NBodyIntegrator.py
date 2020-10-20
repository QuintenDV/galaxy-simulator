from tree.tree import Tree
from itertools import repeat

import numpy as np

class NBodyIntegrator:
    def __init__(self, timestep, integration_time, n_save_points, physics,
                integrator,
                input_file="resources/input_example.txt",
                output_file="resources/output.txt"):
        self.h = timestep
        self.integration_time = integration_time
        self.n_save_points = n_save_points
        self.physics = physics
        self.integrator = integrator
        self.output_file = output_file

        print(f"timestep: {self.h}")
        print(f"time: {self.integration_time}")
        print(f"n_step: {int(self.integration_time / self.h)}")

        # Holds a reference to all the particles. This is constant
        self.orig_particles = self.integrator.load_particles(input_file)
        # A sublist of all currently active particles in the simulation
        self.particles = np.copy(self.orig_particles) # shallow copy

        self.tree = Tree.create_root(self.particles)
        self.tree.grow()

        self.integrator.create_initial_conditions(self.particles, self.tree)

        # Initial energy of the system
        self.E0 = self.physics.system_energy(self.particles)
        # Current energy of the system
        self.E = self.E0
        # energy of particles that have escaped the simulation area
        self.energy_escaped = 0
        # acculated error on the energy
        self.E_err = 0

    def integrate(self):
        self._write_header()
        self.current_step = 0
        from time import time
        while self._integration_condition():
            a = time()
            self.step()
            b = time()
            self._update_energy()
            c = time()
            self.save_results_to_file()
            d = time()
            self.current_step += 1

    def _write_header(self):
        with open(self.output_file, 'w') as ostr:
            ostr.write(f"# {self.get_number_of_particles()} {self.n_save_points}\n")

    def _integration_condition(self):
        return self.current_step * self.h <= self.integration_time \
               and self.get_number_of_particles() > 0

    def step(self):
        self.drop_escaped_particles()
        if self.get_number_of_particles() == 0:
            return

        self.tree = Tree.create_root(self.particles)
        self.tree.grow()
        self._update_all_particles()

    def drop_escaped_particles(self):
        particles_to_drop = self.tree.get_out_of_bounds_particles()
        if len(particles_to_drop) == 0:
            return

        self._capture_escaped_energy(particles_to_drop)
        self._deactivate_escaped_particles(particles_to_drop)
        self.particles = np.delete( self.particles,
            np.argwhere( np.isin(self.particles, particles_to_drop) ))

    def _capture_escaped_energy(self, particles_to_drop):
        for particle in particles_to_drop:
            self.energy_escaped += self.physics.particle_energy(particle, self.particles)

    def _deactivate_escaped_particles(self, particles_to_drop):
        for particle in particles_to_drop:
            particle.deactivate()

    def _update_all_particles(self):
        # apply the `self.integrator.update_particle` function to each
        # element of `self.particles`. Pass `self.particles` and `self.tree`
        # as parameters to the function by using `repeat`.
        map_result = map( self.integrator.update_particle, self.particles,
                          repeat(self.particles), repeat(self.tree))
        # Convert back to a numpy array
        self.particles = np.array(list( map_result ))

    def _update_energy(self):
        if not self._is_output_step():
            return
        self.E = 0
        self.E = self.physics.system_energy(self.particles)
        self.E += self.energy_escaped
        self.E_err = self._energy_error()

    def _energy_error(self):
        return abs( (self.E - self.E0) / self.E0 ) * 1e9

    def _is_output_step(self):
        return self.current_step \
            % (int( self.integration_time / self.h ) // self.n_save_points) \
            == 0

    def save_results_to_file(self):
        if not self._is_output_step():
            return
        print(f"saving step {self.current_step}", end="\r")
        output = []
        output.append(f"{self.current_step:d}")
        output += [str(p) for p in self.orig_particles]
        output.append(f"{self.E_err}\n")

        with open(self.output_file, 'a') as ostr:
            ostr.write( " ".join(output) )

    def get_number_of_particles(self):
        return self.particles.size