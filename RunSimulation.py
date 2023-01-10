from gprMax.gprMax import api
from tools.outputfiles_merge  import merge_files
import os
import time
from FunctionRep import *
from InitSimulation import *

start = time.time()

delta = 0.0

for trace in range(1, measurment_number+1):

    print('!!!!! Starting simulation', trace, '/', measurment_number, '!!!!!')

    delta += measurment_step

    trans[0] += measurment_step
    recei[0] += measurment_step

    model = MoveHelico(ModelName, path_to_input, path_to_materials,
    path_to_h5, xsize, ysize, discrete, freq, trans, recei, trace, 
    time_window, nx, ny, dx, dy, delta, antenna_start, antenna_height)

    api(folder_inout+ModelName+str(trace)+'.in', gpu = [0], n = 1)

    if trace%20 == 0:
        PlotInitialModel(ModelName+str(trace), model, trans, recei, 
        xsize, ysize, dx, dy)

merge_files(folder_inout+ModelName, removefiles = True)
os.system('rm inout_files/*.in')

end = time.time()
print('ELIPSED TIME =', time.strftime('%H:%M:%S', time.gmtime(end-start)), '[HH:MM:SS]')