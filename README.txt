Simple numerical model of a cylindrical piston hammer. The ideal is a pneumatic piston beneath a table with airflow forcing it to oscillate, striking a table as it extends. The table then holds electronics to be tested for resistance to failure due to vibrations. 

All of this work was done as a prototype in 2 nights after work.
The starting_point is just a simple model using ideal gas physics to model a cylinder. It basically showed that if the cylinder radius is too large, increasing the pressure of the inlet air supply will NOT increase the speed of the cylinder expanding. The airflow must increase as well.

The second file was to model the impact of the cylinder hitting a table. It gave surprisingly accurate pictures of what the rms acceleration given by accelerometers on the table showed. This file is bad, but I don't care. I keep passing around a dictionary and makes the code unweildy. If this was more than a prototype I would refactor it to a class structure and modify encapsulated variables. 
