from tree.octant import Octant
from vector import Vector
import numpy as np
from constants import Constants as const
from particle import Particle
from massive_object import MassiveObject

class Tree:
    delta = 0.4

    def __init__(self, level, center):
        self.level = level
        self.center_of_cube = center
        self.center_of_mass = Vector.newVector()
        self.mass = 0

        self.particles = []
        self.branches = []

        self.width = const.k / (2**level)


    def create_root(particles):
        tree = Tree(
            level  = 0,
            center = Vector.newVector()
            )
        tree.set_particles(particles)
        tree.initTree()
        tree.check_out_of_bounds()
        return tree

    def check_out_of_bounds(self):
        particles = self.get_out_of_bounds_particles()
        if particles:
            print(f"{len(particles)} particles are out of bounds at beginning of simulation. Aborting")
            exit(1)

    def initTree(self):
        self.mass = self._calculate_mass()
        self.center_of_mass = self._calculate_center_of_mass()

    def _calculate_mass(self):
        mass = np.sum([p.get_mass() for p in self.particles])
        return mass

    def _calculate_center_of_mass(self):
        if self.mass <= 0:
            return Vector.newVector()

        com = Vector.newVector()
        for p in self.particles:
            com += p.get_mass() * p.get_position()
        com = com / self.mass
        return com

    def grow(self):
        if self.is_particle():
            return

        octants, grouped_particles = self._group_particles_by_octant()
        self.branches = self._create_new_branches(octants)
        self._populate_branches(grouped_particles)
        self._init_branches()
        self._grow_branches()

    def is_particle(self):
        return len(self.particles) == 1

    def _group_particles_by_octant(self):
        by_octant = dict()

        for p_index,particle in enumerate(self.particles):
            octant = self._get_particle_octant(particle)
            if octant not in by_octant:
                by_octant[octant] = []
            by_octant[octant].append(particle)

        octants, grouped_particles = zip(*by_octant.items())
        return octants, grouped_particles

    def _get_particle_octant(self, particle):
        direction = particle.get_position() \
                  - self.center_of_cube
        # `direction` is a vector that points into the direction
        # of the octant that contains the current particle
        octant = Octant.from_direction(direction)
        return octant

    def _create_new_branches(self, octants):
        return [self._create_branch_at_octant(octant)
                for octant in octants]

    def _create_branch_at_octant(self, octant):
        center_of_new_branch = self.center_of_cube \
                             + ( Octant.as_direction(octant)
                                * self.width / 4 )
        return Tree(
            level  = self.level+1,
            center = center_of_new_branch)

    def _populate_branches(self, grouped_particles):
        for branch_index, particles in enumerate(grouped_particles):
            self.branches[branch_index].set_particles(
                particles)
                # np.array(particles)) # This is slower :(

    def _init_branches(self):
        for branch_index,_ in enumerate(self.branches):
            self.branches[branch_index].initTree()

    def _grow_branches(self):
        for branch_index,_ in enumerate(self.branches):
            self.branches[branch_index].grow()

    def makeMassList(self, particle):
        # the massList contains every mass + center of mass that interacts with the particle p, based on the delta value condition
        massList = self.branches
        i = 0
        while i != len(massList):
            d = Vector.norm(particle.get_position() - massList[i].get_center_of_mass())
            if not massList[i].is_particle() and 2 * massList[i].width / d > Tree.delta:
                # the expression after && makes sure we don't try to split up a single particle
                lowerBranches = massList[i].get_branches()
                massList = massList[:i] + massList[i+1:] + lowerBranches
                # no i++ because the deleting element i made element i+1 the new i element
            else:
                i+=1
        return massList

    def get_out_of_bounds_particles(self):
        return [particle
                for particle in self.particles
                if self._is_out_of_bounds(particle)]

    def _is_out_of_bounds(self, particle):
        loc = particle.get_position()
        return any(abs(loc) > self.width)
        # return abs(loc[0]) >= const.k or abs(loc[1]) >= const.k or abs(loc[2]) >= const.k

    def set_particles(self, particles):
        self.particles = particles

    def get_branches(self):
        return self.branches

    def get_center_of_mass(self):
        return self.center_of_mass

    def get_mass(self):
        return self.mass