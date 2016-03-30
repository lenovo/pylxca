from pylxca.pylxca_cmd.lxca_icommands import InteractiveCommand
import sys, getopt
import pylxca.pylxca_api
import lxca_view
import logging
import traceback
from getpass import getpass
from pylxca.pylxca_api.lxca_rest import HTTPError
from pylxca.pylxca_api.lxca_connection import ConnectionError

logger = logging.getLogger(__name__)

class connect(InteractiveCommand):
    """
    Connects to the LXCA Interface
    connect -i <ip> -u <user> -p <passwd>
    """
    def handle_command(self, opts, args):
        try:
            opts, argv = getopt.getopt(args, self.get_char_options(), self.get_long_options())
        except getopt.GetoptError, e:
            self.invalid_input_err()
            return
        
        for opt, arg in opts:
            if '-h' in opt:
                print (self.get_help_message())
                return                
        
        if not self.is_mand_opt_passed(opts):
            self.invalid_input_err()
            return
        
        if not opts:
            self.handle_no_input()
            return
        
        opt_dict = self.parse_args(opts, argv)
        if not opt_dict.has_key("pw"):
            opt_dict ['pw'] = getpass("Enter Password: ")
        
        out_obj = None
        
        try:
            out_obj = self.handle_input(opt_dict)
            self.handle_output(out_obj)
        except HTTPError as re:
            print("Exception %s occurred while executing command."%(re))
        except ConnectionError as re:
            print("Exception %s occurred while executing command."%(re))
        except RuntimeError:
            print "Session Error to LXCA, Try connect"
        except Exception as err:
            print "Exception occurred: %s" %(err) 
            traceback.print_exc( )

        return out_obj
    
    def handle_no_input(self,con_obj):
        #no_opt action can differ command to command so override this function if required
        self.invalid_input_err()
        return
    
    def handle_output(self, out_obj):
        if out_obj == None:
            print("Failed to connect given LXCA " )
        else:
            print("Connection to LXCA successful")
        return
    
###############################################################################
    
class disconnect(InteractiveCommand):
    """
    Diconnects to the LXCA Interface 
    """
    def handle_no_input(self):
        api = pylxca.pylxca_api.lxca_api()
        if api.disconnect() == True:
            print("Connection with LXCA closed successfully " )
        else:
            print("Failed to close connection with LXCA " )
        return 

###############################################################################

class log(InteractiveCommand):
    """
    Connects to the LXCA Interface
    log -l <level>  
    """
    def handle_no_input(self):
        api = pylxca.pylxca_api.lxca_api()
        print("Current Log Level is set to " + str(logging.getLevelName(api.get_log_level())))
        message = """
Possible Log Levels, Please use following values to set desired log level. 

\tDEBUG:        Detailed information, typically of interest only when diagnosing problems.
\tINFO:        Confirmation that things are working as expected.
\tWARNING:    An indication that something unexpected happened, or indicative of some problem in the near future. 
\tERROR:        Due to a more serious problem, the software has not been able to perform some function.
\tCRITICAL:    A serious error, indicating that the program itself may be unable to continue running.
"""
        print message
        return    
    
    ## custom def for inline activites
    def handle_output(self, out_obj):
        api = pylxca.pylxca_api.lxca_api()
        if out_obj == True:
            print("Current Log Level is set to " + logging.getLevelName(api.get_log_level()))
        else:
            print("Fail to set Log Level")
        message = """
Possible Log Levels, Please use following values to set desired log level. 

\tDEBUG:        Detailed information, typically of interest only when diagnosing problems.
\tINFO:        Confirmation that things are working as expected.
\tWARNING:    An indication that something unexpected happened, or indicative of some problem in the near future. 
\tERROR:        Due to a more serious problem, the software has not been able to perform some function.
\tCRITICAL:    A serious error, indicating that the program itself may be unable to continue running.
"""
        print message
        return
    
###############################################################################

class ostream(InteractiveCommand):

    def handle_no_input(self):
        print("Current ostream level is set to %s" %(self.shell.ostream.get_lvl()))
        message = """
Possible ostream levels, Please use following values to set desired stdout level. 

\t0:Quite.
\t1:Console.
\t2:File. 
\t3:Console and File.
"""
        print message
        return 
       
    def handle_input(self, dict_handler):
        lvl = None
        if dict_handler:
            lvl =  dict_handler['l'] or dict_handler['lvl']
            return self.shell.ostream.set_lvl(int(lvl))
        return False
        
    ## custom def for inline activites
    def handle_output(self, out_obj):
        if out_obj == True:
            print("Current ostream level is set to %s" %(self.shell.ostream.get_lvl()))
        else:
            print("Fail to set ostream Level")
            message = """
Possible ostream levels, Please use following values to set desired ostream level. 

\t0:Quite.
\t1:Console.
\t2:File. 
\t3:Console and File.
"""
            print message
        return

###############################################################################

class chassis(InteractiveCommand):
    """
    Get Chassis List and Chassis Information
    """
    
    
###############################################################################

class nodes(InteractiveCommand):
    """
    Get nodes List and nodes Information
    """
    
###############################################################################

class switches(InteractiveCommand):
    """
    Get switches List and switches Information
    """
    
###############################################################################

class fans(InteractiveCommand):
    """
    Get fan List and fans Information
    """
    
###############################################################################

class powersupplies(InteractiveCommand):
    """
    Get Power Supply Information
    """
                
###############################################################################

class fanmuxes(InteractiveCommand):
    """
    Get fan Mux Information
    """

###############################################################################

class cmms(InteractiveCommand):
    """
    Get CMM  Information
    """


###############################################################################

class scalablesystem(InteractiveCommand):
    """
    Get Scalable Complex System  Information
    """

    
###############################################################################

class jobs(InteractiveCommand):
    """
    Retrieve and Manage information about jobs.
    """