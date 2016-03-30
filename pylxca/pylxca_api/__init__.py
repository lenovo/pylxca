# Package init file

'''LXCA Python Client API'''

# All submodules of this package are imported; so clients need to import just this package.
import os   
pylxca_api_path = os.path.dirname(__file__)
os.environ['PYLXCA_API_PATH'] = pylxca_api_path
from lxca_api import *