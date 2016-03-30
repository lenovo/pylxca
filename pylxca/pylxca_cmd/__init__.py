import os

pylxca_cmd_path = os.path.dirname(__file__)
os.environ['PYLXCA_CMD_PATH'] = pylxca_cmd_path

from pylxca.pylxca_cmd import lxca_ishell
from pylxca.pylxca_cmd import lxca_icommands
from pylxca.pylxca_api import *
import pylxca.pylxca_cmd