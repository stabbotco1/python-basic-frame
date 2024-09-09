import os

class CoreUtilities:
    _root_directory = None

    @staticmethod
    def get_root_directory():
        if CoreUtilities._root_directory is None:
            # Traverse upwards to the project root
            current_dir = os.path.abspath(os.path.dirname(__file__))
            project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))  # Move two levels up
            CoreUtilities._root_directory = project_root
        return CoreUtilities._root_directory
