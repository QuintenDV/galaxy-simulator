from particle import Particle
from vector import Vector
import numpy as np

class LeapfrogParticle(Particle):
    def __init__(self, position, velocity, mass):
        super().__init__(position, velocity, mass)
        self.half_step_velocity = np.copy(velocity)

class Leapfrog:
    def __init__(self, timestep, physics):
        self.h = timestep
        self.physics = physics

    def update_particle(self, particle, others, tree):
        ml = tree.makeMassList(particle)
        # Bug here: velocity is always one full timestep behind
        # TODO clean this up a bit
        temp_vel = particle.half_step_velocity + self.h*self.physics.acceleration(particle, ml)
        temp_r_half = particle.get_position() + self.h*(temp_vel)
        particle.set_velocity( (temp_vel + particle.half_step_velocity) / 2 )
        particle.set_position( temp_r_half )
        particle.half_step_velocity = temp_vel
        return particle

    def load_particles(self, input_file):
        with open(input_file) as ins:
            n_particles = int(ins.readline().strip())
            particles = np.empty((n_particles,),dtype=LeapfrogParticle)

            for ln, line in enumerate(ins):
                x, y, z, vx, vy, vz, m = (float(n) for n in line.strip().split(' '))
                particles[ln] = LeapfrogParticle(Vector.newVector(x, y, z), Vector.newVector(vx, vy, vz), m)
                particles[ln].half_step_velocity = Vector.newVector(vx, vy, vz)
        return particles

    def create_initial_conditions(self, particles, tree):
        for particle in particles:
            massListInit = tree.makeMassList(particle) # list van branches

            a_n = self.physics.acceleration(particle, massListInit)
            particle.set_position(
                particle.get_position()
                + 0.5 * self.h * particle.get_velocity() # first-order term
                + 1.0/8 * self.h**2 * a_n) # second order term
