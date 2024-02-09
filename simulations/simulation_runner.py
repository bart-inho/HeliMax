from gprMax.gprMax import api
from tools.outputfiles_merge  import merge_files
from queue import Queue
import os
from multiprocessing import current_process


class SimulationRunner:
    def run_simulation(args):
        path_to_files, model_name, idx, gpu_id = args
        model_input_file_name = model_name if idx == 0 else f"{model_name}{idx}"
        
        print(f"Process {current_process().name} running on GPU {gpu_id}: {os.path.join(path_to_files, model_input_file_name + '.in')}")
        api(os.path.join(path_to_files, model_input_file_name + ".in"), mpi=False, gpu=[gpu_id], n = 1)

    def create_gpu_queue(gpu_ids):
        """
        Create a queue populated with the specified GPU IDs.
        """
        gpu_queue = Queue() # Create a queue
        for gpu_id in gpu_ids: # Iterate over the specified GPU IDs
            gpu_queue.put(gpu_id)  # Populate the queue with specified GPU IDs
        return gpu_queue


    def merge_files(remove_files, path_to_files, model_name):
        merge_files(path_to_files+model_name, removefiles = remove_files)