from gprMax.gprMax import api
from tools.outputfiles_merge  import merge_files
from InitSimulation import *

api(folder_inout+ModelName+'.in', gpu = [0], n = measurment_step)
merge_files(folder_inout+ModelName, removefiles = True)
print('Process ended')