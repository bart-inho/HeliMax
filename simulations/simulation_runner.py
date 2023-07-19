from gprMax.gprMax import api
from tools.outputfiles_merge  import merge_files

class SimulationRunner:
    def __init__(self, simulation_model):
        self.simulation_model = simulation_model

    def run_simulation(self, measurement_number):
        api(self.simulation_model.path + self.simulation_model.name + '.in', gpu = [0], n = measurement_number)
    
    def merge_files(self, remove_files):
        merge_files(self.simulation_model.path + self.simulation_model.name, removefiles = True)