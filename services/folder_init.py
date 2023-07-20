from pathlib import Path

class InitializeFolders:

    @staticmethod
    def check_and_create_directories():
        # Check if inout_files exists and create if not
        Path('inout_files/figures').mkdir(parents=True, exist_ok=True)