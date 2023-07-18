import numpy as np
import matplotlib.pyplot as plt
import h5py
from os.path import exists
import os
from FunctionRep import *

# Model size and discretization -----------------------------------
xsize = 50 # x-size of the model [m]
ysize = 10 # y-size of the model [m]
zsize = 40 # z-size of the model [m]

dx = .25 # z cell size [m]
dy = .25 # y cell size [m]
dz = .25 # z cell size [m]
 
discrete = [dx, dy, dz]

nx = int(xsize / dx) # x-number of cell
ny = int(ysize / dy) # y-number of cell
nz = int(zsize / dz) # z-number of cell

# Define x and y position for the transiever and the receiver ------
transiever1 = [round(xsize/10)     , round(ysize/2), round(zsize/3-.5)]
receiver1 = [round(xsize/10 + 4) , round(ysize/2), round(zsize/3-.5)]

# Frequency and time window ---------------------------------------
freq = 25e6 # [MHz]
time_window = 1.e-6 # [s]
measurment_number = 20 # number of gprMax simulations
measurment_step = round((ysize - 30)/measurment_number) # number of step minus a margin

# Folder, files name and path -------------------------------------
ModelName = 'test_rugged_bedrock_air_helico'

folder_inout = 'inout_files/'
filename_input = ModelName # .in file
filename_materials = ModelName+'_materials' # material file
path_to_h5 = folder_inout+ModelName # path

# Create path to file ---------------------------------------------
path_to_input = folder_inout + filename_input
path_to_materials = folder_inout+filename_materials

# Define materials [eps_r ; sigma ; mu_r ; vel] -------------------
mat_freespace = [1., 0., 1., 0] # gprMax build in 
mat_glacier = [3.2, 5.e-8, 1., 0]  # Church et al., 2020
mat_bedrock = [5., 0.01, 1, 0] # granite Annan (1999)
mat_helico = [1., 'inf', 1., 0] # metal gprMax build in

# Create material file --------------------------------------------
WriteMaterialsFile(path_to_materials, mat_freespace, mat_bedrock, mat_glacier, mat_helico)

# Generate base of the model --------------------------------------
model = np.zeros((nx, ny, nz)) # Free space = 0
model[round(nx/2):nx,:,:] = 1 # Glacier = 1
model[0:round(nx/20),:,:] = 3 # Helico = 3

# Generate a curved bedrock ---------------------------------------
center = [0, ny/2, 0]
r = 47.5 # Define center of the circle
GenerateGlacierShape(model, r, center, dx, dz) #generate circle shape

# Flip matrix ------------------------------------------------------
model = model.T # taking the transverse of the matrix is necessary for the gprMax format

# Plot model -------------------------------------------------------
PlotInitialModel(ModelName, model, transiever1, receiver1, xsize, ysize, zsize)

# Rehape the model for gprMax compulsory third dimension -----------
model = np.reshape(model, (nx, ny, nz))

print(model.shape)

# generate h5 file -------------------------------------------------
Writeh5File(path_to_h5, model, discrete)

# Generate .in file ------------------------------------------------
WriteInputFile(ModelName, path_to_input, path_to_materials, 
               path_to_h5, xsize, ysize, zsize, discrete, freq, transiever1, 
               receiver1, measurment_step, time_window)