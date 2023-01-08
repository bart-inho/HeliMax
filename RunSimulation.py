from gprMax.gprMax import api
from tools.outputfiles_merge  import merge_files
from InitSimulation import *

api(folder_inout+ModelName+'.in', gpu = [0], n = 1)
merge_files(folder_inout+ModelName, removefiles = True)