import os
import time
from gprMax.gprMax import api
from tools.outputfiles_merge  import merge_files
from InitSimulation import *

start = time.time()
delta = 0.0

# Start loop
for trace in range(1, measurment_number+1):

    # Print which simulation is started
    print('!!!!! Starting simulation', trace, '/', measurment_number, '!!!!!')

    # Generate a distance delta from initial position
    if trace > 1 :
        delta += measurment_step

    # Add the distance increment (measurment step size)
    trans[0] += measurment_step
    recei[0] += measurment_step

    # Generate the new model and write new text files
    model = MoveHelico(ModelName, path_to_input, path_to_materials,
    path_to_h5, xsize, ysize, discrete, freq, trans, recei, trace, 
    time_window, nx, ny, dx, dy, delta, antenna_start, antenna_height)

    # Run the simulation for the generated input file
    api(folder_inout+ModelName+str(trace)+'.in', gpu = [0], n = 1)

    # Remove input files
    os.system('rm '+folder_inout+ModelName+str(trace)+'.in')

    # Generate a figure of the input model for each n timesteps
    n = 20
    if trace%n == 0:
        PlotInitialModel(ModelName+str(trace), model, trans, recei, 
        xsize, ysize, dx, dy)

# Merge the output files into one 2D file
merge_files(folder_inout+ModelName, removefiles = True)

# Running time calculation
end = time.time()
print('ELIPSED TIME =', time.strftime('%H:%M:%S', time.gmtime(end-start)), '[HH:MM:SS]')