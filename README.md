# helico-gprMax
This repository aims to show how to generate gprMax input files using NumPy arrays, and how to perform simulation using these input files. The models generated and performed are inspired by an airborne ice Radar setup from ETHZ. This work takes place is a master thesis project. The ultimate goal of these simulations is to determine if a shielding between the GPR and the helicopter would be effective and if so, what geometry and properties it should have. 
 
Public description of the project : https://vaw.ethz.ch/en/research/glaciology/research-projects.html
 
# The setup
The setup is composed of a python file `InitSimulation.py` and a `Makefile`. The folder `inout_files` stores  input and output files, as well as the figures. This repository should be downloaded and placed into the gprMax folder. For example :
 
`home/user/gprMax/helico-gprMax`
 
 You must have a gprMax environment correctly installed : https://github.com/gprMax/gprMax
 
# How it works
All the programs as well as the simulations are launched using the `Makefile`.
 
## Makefile system
A `Makefile` is simply a list of commands that your computer will run into a terminal. Different programs can be launched at the same time, or separately if needed. Everything is controlled by few keywords. The conda environment `gprMax` must be activated.

- Typing `make init` : runs the script `InitSimulation.py`
- Typing `make run` : launches gprMax simulation using the input file generated.
- Typing `make plot` : plots the result using the gprMax build in function `plot_Bscan`
- Typing `make clean`: cleans up `inout_files` folder from `.out`, `.in`, `.txt` and `.h5` files

For now, it is only possible to run one simulation at the time. (to be continued...)
 
## Generate models
The models can be generated using simple NumPy arrays. Any kind of geometry can be generated, on few conditions:
1. The array is composed of integer (not permittivity values)
2. Every integer correspond to a specific material
3. All materials are described in a text file (see the file for the structure)
4. The order of the materials matters

## gprMax simulations
The documentation of gprMax give some simple commands to run simulations. For example:
 
`python -m gprMax user_models/cylinder_Ascan_2D.in`, 
 
where `cylinder_Ascan.in` is a basic input file from gprMax. In certain cases, it's an advantage to use a GPU to run gprMax simulations. This can be done by using the `-gpu` argument.
