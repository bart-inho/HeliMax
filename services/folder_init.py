from pathlib import Path

class InitializeFolders:

    @staticmethod
    def check_and_create_directories(folder_name):
        # Check if inout_files exists and create if not
        Path(folder_name+'figures').mkdir(parents=True, exist_ok=True)
