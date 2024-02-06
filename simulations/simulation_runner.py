from gprMax.gprMax import api
from tools.outputfiles_merge  import merge_files
from queue import Queue

class SimulationRunner:
    def run_simulation(path_to_files, model_name, idx, gpu_queue):
        gpu_id = gpu_queue.get()  # Get an available GPU ID from the queue
        model_input_file_name = f"{model_name}{idx}"  # Assuming model names are indexed
        
        # Run the simulation on the specified GPU
        api(f"{path_to_files+model_input_file_name}.in", mpi=False, gpu=[gpu_id])
        
        print(f"Simulation {model_input_file_name} completed on GPU {gpu_id}")
        
        # Put the GPU ID back in the queue indicating it's available again
        gpu_queue.put(gpu_id)

    def create_gpu_queue(num_gpus=8):
        gpu_queue = Queue()
        for i in range(num_gpus):
            gpu_queue.put(i)  # Initialize the queue with GPU IDs (0 to 7)
        return gpu_queue


    def merge_files(remove_files, path_to_files, model_name):
        merge_files(path_to_files+model_name, removefiles = remove_files)