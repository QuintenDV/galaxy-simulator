# galaxy-simulator

A python project for numerically solving the equations of motion in simple astrophysical simulations.

This is based on a project I did in University for a physics course. The project was originally in c++ and the code was absolutely horrible. I converted some of the c++ code to python and rewrote some things from scratch. It is still a work in progress and the performance is not was it should be. It's about 10 times slower than it's (singlethreaded) c++ counterpart. I could look into multiprocessing but I think there is more to be gained by working more efficiently with numpy arrays.

## What is does
The input is a text file with the initial conditions of the system. The system contains stars, modelled by points, with a position (3D-vector), a velocity (3D-vector) and a mass.  Once initialized, time progresses by discrete steps. After every timestep, the particles' positions and velocities are updated based on the equations of motion of classical mechanics.  

### example
![example_gif](example.gif)

## Somewhat more detailed explanation
After each timestep all particles need to be updated. A particled is affected by the gravitational pull of all the other particles in the system. So for each particle, the force exerted on it by all the other particles is calculated. Once these accelerations are calculate, the positions and velocites of all particles can be updated.

Because all particles exert forces on each other, calculating these forces required calculating ~_N<sup>2</sup>_ square roots for each timestep.  

There are ways to reduce the workload will still getting accuracy results. One of these methods is called the Tree Method. I'm not going to go into too much detail but in order to reduce the _N<sup>2</sup>_ complexity we will treat the more distant neighbours of stars as aggregates. We construct the tree and calculate the center of mass and mass of each branch. Now, when we want to calculate the force on a certain particle, we traverse the tree. If the center of mass of the branch is close to the particle, we will go down a level and check its branches. It a branch is far away we calculate the force based on its center of mass. This basically reduces the complexity to _N_ log _N_.  

The ingrator used here is a [leapfrog integrator](https://en.wikipedia.org/wiki/Leapfrog_integration).
