import numpy as np
import matplotlib.pyplot as plt
import h5py
from os.path import exists
import os

# Model size and discretization
xsize = 40 # size of the model [m]
ysize = 100

dx = .1 # discretization
dy = .1
dz = .1

nx = int(xsize / dx) # number of cell
ny = int(ysize / dy)

# Frequency
freq = 25e6 # MHz
time_window = 1.5e-6

folder = 'GenerateModels/'
pathinput = 'bedrock_model.in'
pathmaterials = 'bedrock_model_materials.txt'

filename = open(folder+pathinput, 'w')
filname_materials = open(folder+pathmaterials, 'w')

# Define materials
#mat_helicopter = []
mat_freespace = [1., 0., 1., 0] # gprMax build in [eps_r ; sigma ; mu_r ; vel]
mat_glacier = [3.2, 5.e-8, 1., 0]  # Church et al., 2020
mat_bedrock = [5., 0.01, 1, 0] # granite Annan (1999)
mat_helico = [1., 1000., 1., 0]

# generate file with material properties
filname_materials.write('#material: '+str(mat_freespace[0])+' '+str(mat_freespace[1])+' '+str(mat_freespace[2])+' '+str(mat_freespace[3])+' freespace\n')
filname_materials.write('#material: '+str(mat_glacier[0])+' '+str(mat_glacier[1])+' '+str(mat_glacier[2])+' '+str(mat_glacier[3])+' glacier\n')
filname_materials.write('#material: '+str(mat_bedrock[0])+' '+str(mat_bedrock[1])+' '+str(mat_bedrock[2])+' '+str(mat_bedrock[3])+' bedrock\n')
filname_materials.write('#material: '+str(mat_helico[0])+' '+str(mat_helico[1])+' '+str(mat_helico[2])+' '+str(mat_helico[3])+' helicopter\n')


model = np.zeros((ny, nx))
model[round(ny/2):ny,:] = 2
#model[round(ny*2/3):ny, :] = 2
#model[0:round(ny/20), :] = 3

r = 90

# center = [round(nx/2), round(nx/2)]
center = [0, nx]

for i in range(0, ny):
    for j in range(0, nx):
        rij = np.sqrt(((j - center[1])*dx)**2 + ((i - center[0])*dy)**2)
        if rij < r and i > round(ny/2):# and j < round(nx/2):
            model[i, j] = 1

#model[round(ny/2):ny, round(nx/2):nx] = 1

# Flip matrix
model = model.T

transx = round(xsize/10)
receix = round(xsize/10 + 3)
transy = round(ysize/3-.5)
receiy = round(ysize/3-.5)
# transy = round(ysize/2-.5)
# receiy = round(ysize/2-.5)

# Plot the model
plt.imshow(model.T)
plt.scatter(transx/xsize*nx, transy/ysize*ny)
plt.scatter(receix/xsize*nx, receiy/ysize*ny)
plt.title('off centered bedrock')
plt.savefig('off_centered_bedrock.png')
plt.show()

# Rehape the model for gprMax compulsory third dimension
model = np.reshape(model, (nx, ny, 1))

# generate h5 file
pathh5 = folder+'bedrock.h5'
pathchris = folder+'chrismodelh5.h5'
if exists(pathh5) == True:
    os.remove(pathh5)

hdf = h5py.File(pathh5, 'w')
modelh5 = hdf.create_dataset(name = 'data', data = model)
hdf.attrs['dx_dy_dz'] = [dx, dy, dz]


# Generate .in file
filename.write('#title: bedrock_model \n')
filename.write('#domain: '+str(xsize)+' '+str(ysize)+' '+str(dz)+' \n')
filename.write('#dx_dy_dz: '+str(dx)+' '+str(dy)+' '+str(dz)+' \n')
filename.write('#time_window: '+ str(time_window)+'\n')
filename.write('#waveform: ricker 1 '+ str(freq)+ ' my_ricker\n')
filename.write('#hertzian_dipole: z '+str(transx)+' '+str(transy)+' 0 my_ricker\n')
filename.write('#rx: '+str(receix)+' '+str(receiy)+' 0\n')
filename.write('#src_steps: 0.5 0 0\n')
filename.write('#rx_steps: 0.5 0 0\n')
filename.write('#geometry_objects_read: 0 0 0 '+pathh5+' '+folder+pathmaterials)