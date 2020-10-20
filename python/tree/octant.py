from vector import Vector
from enum import Enum, unique

# A cube has 8 octants. They are uniquely defined by their position
# along the xyz-axes, given that the origin is at the center of the cube.
# In this context they can be represented by an integer (see`Octant`
# Enum) or a vector that points from the origin of the cube to the
# center of the octant (see `_Direction` class).

# This class has 8 static direction vectors, one for each octant
# The index of each vector corresponds to the enum value in the
# `Octant` Enum.
# Example:
#   The octant located in the positive x and y direction and the
#   negative z direction corresponds to the direction vector:
#       (1, 1, -1), at index 3.
# NOTE: this is a separate private class because Enums can't
# hold static class variables
class _Direction:
    directions = [
        Vector.newVector(-1, -1, -1),
        Vector.newVector( 1, -1, -1),
        Vector.newVector(-1,  1, -1),
        Vector.newVector( 1,  1, -1),
        Vector.newVector(-1, -1,  1),
        Vector.newVector( 1, -1,  1),
        Vector.newVector(-1,  1,  1),
        Vector.newVector( 1,  1,  1),
    ]

# Example:
#   The octant located in the positive x and y direction and the
#   negative z direction corresponds XposYposZneg and has value 3,
#   which corresponds to the index of the vector in `_Direction`
@unique
class Octant(Enum):
    XnegYnegZneg = 0
    XposYnegZneg = 1
    XnegYposZneg = 2
    XposYposZneg = 3
    XnegYnegZpos = 4
    XposYnegZpos = 5
    XnegYposZpos = 6
    XposYposZpos = 7

    def from_direction(direction):
        octant_value = (direction[0] > 0) \
                 + 2 * (direction[1] > 0) \
                 + 4 * (direction[2] > 0)
        return Octant(octant_value)

    def as_direction(octant):
        return _Direction.directions[octant.value]