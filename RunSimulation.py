from gprMax.gprMax import api
from tools.outputfiles_merge  import merge_files

ModelName = 'test_moving'
folder_inout = 'inout_files/'
api(folder_inout+ModelName+'.in', gpu = [0], n = 30)
merge_files(folder_inout+ModelName, removefiles = True)