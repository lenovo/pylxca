# Package init file

'''LXCA Python Client API'''

#setting CMD_PATH environment variable to be used in submodules for loading data files
import os   
pylxca_api_path = os.path.dirname(__file__)
os.environ['PYLXCA_API_PATH'] = pylxca_api_path

# All submodules of this package are imported; so clients need to import just this package.
from lxca_api import *