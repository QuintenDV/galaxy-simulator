from particle import Particle
from vector import Vector
from constants import Constants as const
import numpy as np
from itertools import repeat

class Physics:
    def __init__(self, epsilon=0):
        self.epsilon = epsilon

    def system_energy(self, particles):
        E_kin = sum(map(self.E_kinetic, particles))
        E_pot = sum(map(self.E_potential, particles, repeat(particles)))
        E_pot /= 2
        return E_kin + E_pot

    def particle_energy(self, particle, others):
        E_kin = self.E_kinetic(particle)
        E_pot = self.E_potential(particle, others)
        return E_kin + E_pot

    def E_kinetic(self, particle):
        E_kin = 0.5 * particle.get_mass() \
                     * Vector.norm(particle.get_velocity()) ** 2
        return E_kin

    # Only particles
    def E_potential(self, particle, others):
        E_pot = 0
        m = particle.get_mass()
        p = particle.get_position()
        for other in others:
            if (particle == other):
                continue
            M = other.get_mass()
            P = other.get_position()
            distance_sq = Vector.norm( p - P )**2
            E_pot -= const.G*m*M \
                    / np.sqrt( self.epsilon**2 + distance_sq)
        return E_pot * 100

    def acceleration(self, particle, objects):
        # If the branch is a single particle we check if it's the same particle we're calculating the a for
        # the same problem could occur if this particle's mass included in a com we use, but for normal values of delta
        # branches so close by should be split up until the particle ends up in the check above */
        a = Vector.newVector()
        p = particle.get_position()
        for obj in objects:
            if obj.is_particle() and obj.particles[0] == particle:
                continue
            P = obj.get_center_of_mass()
            M = obj.get_mass()
            distance_sq = Vector.norm(p - P) **2
            a += -const.G * M * (p - P) \
                / ( self.epsilon**2 + distance_sq )**1.5
        return a