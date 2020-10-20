from vector import Vector

class Particle:
    def __init__(self, position, velocity, mass):
        self.position = position
        self.velocity = velocity
        self.mass = mass

    def deactivate(self):
        self.position = Vector.newVector()
        self.velocity = Vector.newVector()
        self.mass = 0

    def __eq__(self, other):
        pos_norm = Vector.norm(self.get_position() - other.get_position())
        vel_norm = Vector.norm(self.get_velocity() - other.get_velocity())
        mass_diff = abs(self.get_mass() - other.get_mass())
        return pos_norm + vel_norm + mass_diff < 1e-8

    def __str__(self):
        x,y,z = self.position
        vel_norm = Vector.norm(self.velocity)
        return f"{x} {y} {z} {vel_norm}"

    def get_position(self):
        return self.position

    def get_velocity(self):
        return self.velocity

    def get_mass(self):
        return self.mass

    def set_position(self, position):
        self.position = position

    def set_velocity(self, velocity):
        self.velocity = velocity
