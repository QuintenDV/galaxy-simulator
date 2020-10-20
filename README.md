# galaxy-simulator

A python project for numerically solving the equations of motion in simple astrophysical simulations.

This is based on a project I did in University for a physics course. The project was originally in c++ and the code was absolutely horrible. I converted some of the c++ code to python and rewrote some things from scratch. It is still a work in progress and the performance is not was it should be. It's about 10 times slower than its (singlethreaded) c++ counterpart. I could look into multiprocessing but I think there is more to be gained by working more efficiently with numpy arrays.

## What it does
The input is a text file with the initial conditions of the system. The system contains stars, modelled as points, with a position (3D-vector), a velocity (3D-vector) and a mass.  Once initialized, time progresses by discrete steps. After every timestep, the particles' positions and velocities are updated based on the equations of motion of classical mechanics.

There is a script that can visualize the output with matplotlib.

### example
![example_gif](example.gif)
![example_gif](example2.gif)

## Somewhat more detailed explanation
After each timestep all particles need to be updated. A particled is affected by the gravitational pull of all the other particles in the system. So for each particle, the force exerted on it by all the other particles is calculated. Once these accelerations are calculated, the positions and velocites of all particles can be updated.

Because all particles exert forces on each other, calculating these forces requires calculating ~_N<sup>2</sup>_ square roots for each timestep, which is not desirable.  

There are ways to reduce the workload while still getting accurate results. One of these methods is called the Tree Method. I'm not going to go into too much detail but in order to reduce the _N<sup>2</sup>_ complexity we will treat the more distant neighbours of stars as aggregates. We construct the tree and calculate the center of mass and mass of each branch. Now, when we want to calculate the force on a certain particle, we traverse the tree. If the center of mass of the branch is close to the particle, we will go down a level and check its branches, recursively, until we hit a leaf node that contains only one particle and calculate the acceleration induces by that particle. If a branch is far away we calculate the force based on the center of mass of that branch, essentially approximating the interacting with multiple particles at one particle at the center of mass of the branch. This basically reduces the complexity to _N_ log _N_.  

The integrator used here is a [leapfrog integrator](https://en.wikipedia.org/wiki/Leapfrog_integration).
