import numpy as np

class Vector:
    def newVector(x=0, y=0, z=0):
        return np.array([x,y,z], dtype=float)

    def norm(vector):
        return np.linalg.norm(vector)