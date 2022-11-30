import numpy as np
import matplotlib.pyplot as plt
import h5py as h5py
from os.path import exists
import os
from FuncTest import *

# Model size and discretization -----------------------------------
xsize = 100 # x-size of the model [m]
ysize = 100 # y-size of the model [m]

dx = .1 # z cell size [m]
dy = .1 # y cell size [m]
dz = .1 # z cell size [m]

nx = int(xsize / dx) # x-number of cell
ny = int(ysize / dy) # y-number of cell

# Frequency and time window ---------------------------------------
freq = 25e6 # [MHz]
time_window = 1.5e-6 # [s]

# Folder and path -------------------------------------------------
ModelName = 'off-centered-bedrock'
infileFolder = 'inout_files/'
pathinput = 'bedrock_model.in' # .in file
pathmaterials = 'bedrock_model_materials.txt' # material file

# Create a new files ----------------------------------------------
infilename = open(infileFolder+pathinput, 'w') # create .in file
infilname_materials = open(infileFolder+pathmaterials, 'w') # create materials file

# Define materials [eps_r ; sigma ; mu_r ; vel] -------------------
mat_freespace = [1., 0., 1., 0] # gprMax build in 
mat_glacier = [3.2, 5.e-8, 1., 0]  # Church et al., 2020
mat_bedrock = [5., 0.01, 1, 0] # granite Annan (1999)
mat_helico = [1., 'inf', 1., 0] # metal gprMax build in

# Generate file with material properties --------------------------
infilname_materials.write('#material: '+str(mat_freespace[0])+' '+str(mat_freespace[1])+' '+str(mat_freespace[2])+' '+str(mat_freespace[3])+' freespace\n')
infilname_materials.write('#material: '+str(mat_glacier[0])+' '+str(mat_glacier[1])+' '+str(mat_glacier[2])+' '+str(mat_glacier[3])+' glacier\n')
infilname_materials.write('#material: '+str(mat_bedrock[0])+' '+str(mat_bedrock[1])+' '+str(mat_bedrock[2])+' '+str(mat_bedrock[3])+' bedrock\n')
infilname_materials.write('#material: '+str(mat_helico[0])+' '+str(mat_helico[1])+' '+str(mat_helico[2])+' '+str(mat_helico[3])+' helicopter\n')

# Generate base of the model --------------------------------------
model = np.zeros((ny, nx)) # Free space = 1
model[round(ny/2):ny,:] = 2 # Granite = 2
# model[round(ny*2/3):ny, :] = 2 # alternative geometry
model[0:round(ny/20), :] = 3 # Helico = 3

# Generate a curved bedrock ---------------------------------------
center = [0, nx]
r = 100 # Define center of the circle
for i in range(0, ny): # start loop on x
    for j in range(0, nx): # start loop on y
        rij = np.sqrt(((j - center[1])*dx)**2 + ((i - center[0])*dy)**2) # Calculate distance
        if rij < r and i > round(ny/2):# condition
            model[i, j] = 1 # Glacier = 1

# Flip matrix ------------------------------------------------------
model = model.T # taking the transverse of the matrix is necessary for the gprMax format

# Define x and y position for the transiever and the receiver ------
transx = round(xsize/10)
receix = round(xsize/10 + 3)
transy = round(ysize/3-.5) # transeiver in the air
receiy = round(ysize/3-.5) # receiver in the air
# transy = round(ysize/2-.5) # transeiver on the ground
# receiy = round(ysize/2-.5) # receiver on the ground

# Plot the model ---------------------------------------------------
plt.imshow(model.T) # plotting the transverse
plt.scatter(transx/xsize*nx, transy/ysize*ny)
plt.scatter(receix/xsize*nx, receiy/ysize*ny)
plt.title(ModelName)
plt.savefig('figures/'+ModelName+'.png')
plt.show()

# Rehape the model for gprMax compulsory third dimension -----------
model = np.reshape(model, (nx, ny, 1))

# generate h5 file -------------------------------------------------
pathh5 = infileFolder+'bedrock.h5' # path
if exists(pathh5) == True: # condition to delete old h5 file
    os.remove(pathh5) # delete old h5 file

hdf = h5py.File(pathh5, 'w') # create a new h5 file
modelh5 = hdf.create_dataset(name = 'data', data = model) # create a new dataset
hdf.attrs['dx_dy_dz'] = [dx, dy, dz] # create an attribute that containes dx, dy and dz
# -> more info : https://docs.h5py.org/en/stable/high/dataset.html?highlight=attrs#h5py.Dataset.attrs

# Generate .in file ------------------------------------------------
infilename.write('#title: bedrock_model \n')

# Set domain size, don't forget z = dz for 2D
infilename.write('#domain: '+str(xsize)+' '+str(ysize)+' '+str(dz)+' \n')
infilename.write('#dx_dy_dz: '+str(dx)+' '+str(dy)+' '+str(dz)+' \n')

# Time window
infilename.write('#time_window: '+ str(time_window)+'\n')

# Frequency and antenna geometry
infilename.write('#waveform: ricker 1 '+ str(freq)+ ' my_ricker\n')
infilename.write('#hertzian_dipole: z '+str(transx)+' '+str(transy)+' 0 my_ricker\n')
infilename.write('#rx: '+str(receix)+' '+str(receiy)+' 0\n')

# Movement of the right
infilename.write('#src_steps: 2 0 0\n')
infilename.write('#rx_steps: 2 0 0\n')

# Include external files
infilename.write('#geometry_objects_read: 0 0 0 '+pathh5+' '+infileFolder+pathmaterials)