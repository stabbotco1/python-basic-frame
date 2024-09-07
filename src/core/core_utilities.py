import os

class CoreUtilities:
    _root_directory = None

    @staticmethod
    def get_root_directory():
        if CoreUtilities._root_directory is None:
            CoreUtilities._root_directory = os.path.abspath(os.path.dirname(__file__))
        return CoreUtilities._root_directory