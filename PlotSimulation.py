import os
ModelName = 'test_shielding'
folder_inout = 'inout_files/'
os.system('python -m tools.plot_Bscan '+folder_inout+ModelName+'_merged.out Ez')    