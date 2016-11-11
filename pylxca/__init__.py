# Version of the pylxca package

__version__ = '1.2.2'


# There are submodules, but clients shouldn't need to know about them.
# Importing just this module is enough.

# These are explicitly safe for 'import *'
from pylxca_api import *
from pylxca_cmd import *

# Set default logging handler to avoid "No handler found" warnings.
import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())

#Configure Logger
import logging.config
pylxca.pylxca_api.lxca_rest().set_log_config()

