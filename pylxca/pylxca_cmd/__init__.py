# Package init file

'''LXCA Python Client API'''

#setting CMD_PATH environment variable to be used in submodules for loading data files
import os
import pylxca.pylxca_cmd

# All submodules of this package are imported; so clients need to import just this package.
from pylxca.pylxca_cmd import lxca_ishell
from pylxca.pylxca_cmd import lxca_icommands
from pylxca.pylxca_api import *

pylxca_cmd_path = os.path.dirname(__file__)
os.environ['PYLXCA_CMD_PATH'] = pylxca_cmd_path
