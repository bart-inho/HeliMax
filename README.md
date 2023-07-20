# HeliMax
This repository aims to show how to generate gprMax input files using NumPy arrays, and how to perform simulation using these input files. The models generated and performed are inspired by an airborne ice Radar setup from ETH Zurich. This work takes place is a master thesis project. The ultimate goal of these simulations is to determine if a shielding between the GPR and the helicopter would be effective and if so, what geometry and properties it should have. 
 
Public description of the project : https://vaw.ethz.ch/en/research/glaciology/research-projects.html
 
# The setup
The setup is composed of multiple python files, which the most important one is `main.py`. The folder `inout_files` stores  input and output files, as well as the figures. This repository should be downloaded and placed into the gprMax folder. For example :
 
`home/user/gprMax/HeliMax`
 
 You must have a gprMax environment correctly installed : https://github.com/gprMax/gprMax
 You must install additionnal requirments (´conda requirment.txt´)
 
# How it works
The script is executed using the terminal. `python main.py` generates the model, you can check your geometry and the files generated. `python main.py --run` regenerate all the files and launch the gprMax simulation.

## Generate models
The models can be generated using simple NumPy arrays. Any kind of geometry can be generated, on few conditions:
1. The array is composed of integer (not physical properties)
2. Every integer correspond to a specific material
3. All materials are described in a `.txt` file (see the file for the structure)
4. The order of the materials matters
5. The matrix of integer is stored in a `.h5` file
6. The `.in` file contains all the information, plus the `.txt` and `.h5` file paths

## gprMax simulations
The documentation of gprMax give some simple commands to run simulations. For example:
 
`python -m gprMax user_models/cylinder_Ascan_2D.in`, 
 
where `cylinder_Ascan.in` is a basic input file from gprMax. In certain cases, it's an advantage to use a GPU to run gprMax simulations. This can be done by using the `-gpu` argument.

# Multi-GPU clusters
For multi-GPU users, the installation requires some attention. In the same conda environment used for gprMax, some packages must be installed. The three main packages to install are `pycuda`, `openmpy` and `mpi4py`. This must be done using:

`conda install -c conda-forge pycuda mpi4py openmpi`

Then, in certain cases, it will be necessary to remove tha package `mpich` which is installed by conda when installing the package `mpi4py`. `pip` is not used as it will struggle to build wheels to install the packages. 
