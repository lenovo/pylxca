'''
@since: 15 Sep 2015
@author: Prashant Bhosale <pbhosale@lenovo.com>
@license: Lenovo License
@copyright: Copyright 2016, Lenovo
@organization: Lenovo 
@summary: This module provides command class implementation for PyLXCA 
'''

import sys, getopt
import logging, traceback
from getpass import getpass

import pylxca.pylxca_api
from pylxca.pylxca_api.lxca_rest import HTTPError
from pylxca.pylxca_api.lxca_connection import ConnectionError
from pylxca.pylxca_cmd.lxca_icommands import InteractiveCommand
from pylxca.pylxca_cmd.lxca_icommands import PyAPI

logger = logging.getLogger(__name__)

class connect(InteractiveCommand):
    """
    Connects to the LXCA Interface

    USAGE:
        connect -h | --help
        connect -l <URL> -u <USER> [--noverify]
    
    OPTIONS:
        -h        This option displays command usage information
        -l, --url    URL of LXCA
        -u, --user    Username to authenticate
        --noverify    Do not verify the server certificate for https URLs

    """
    def handle_command(self, opts, args):
        try:
            opts, argv = getopt.getopt(args, self.get_char_options(), self.get_long_options())
        except getopt.GetoptError, e:
            self.invalid_input_err()
            return
        
        for opt, arg in opts:
            if '-h' in opt:
                self.sprint (self.__doc__)
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
            self.sprint("Exception %s occurred while executing command."%(re))
        except ConnectionError as re:
            self.sprint("Exception %s occurred while executing command."%(re))
        except RuntimeError:
            self.sprint("Session Error to LXCA, Try connect")
        except Exception as err:
            self.sprint("Exception occurred: %s" %(err)) 
    
        return out_obj
    
    def handle_no_input(self,con_obj = None):
        #no_opt action can differ command to command so override this function if required
        self.invalid_input_err()
        return
    
    def handle_output(self, out_obj):
        if out_obj == None:
            self.sprint("Failed to connect given LXCA " )
        else:
            self.sprint("Connection to LXCA successful")
        return
    
###############################################################################
    
class disconnect(InteractiveCommand):
    """
    Diconnects from LXCA Interface 

    USAGE:
        disconnect -h | --help
        disconnect
    """
    def handle_no_input(self):
        api = pylxca.pylxca_api.lxca_api()
        if api.disconnect() == True:
            self.sprint("Connection with LXCA closed successfully " )
        else:
            self.sprint("Failed to close connection with LXCA " )
        return 

###############################################################################

class log(InteractiveCommand):
    """
    Retrieve and configure logging of LXCA Python tool
    
    USAGE:
        log -h | --help
        log [-l <level>]

    OPTIONS:
        -l, --lvl    Logging level
      
    """
    def handle_no_input(self,con_obj = None):
        api = pylxca.pylxca_api.lxca_api()
        self.sprint("Current Log Level is set to " + str(logging.getLevelName(api.get_log_level())))
        message = """
Possible Log Levels, Please use following values to set desired log level. 

\tDEBUG:        Detailed information, typically of interest only when diagnosing problems.
\tINFO:        Confirmation that things are working as expected.
\tWARNING:    An indication that something unexpected happened, or indicative of some problem in the near future. 
\tERROR:        Due to a more serious problem, the software has not been able to perform some function.
\tCRITICAL:    A serious error, indicating that the program itself may be unable to continue running.
"""
        self.sprint(message)
        return    
    
    ## custom def for inline activites
    def handle_output(self, out_obj):
        api = pylxca.pylxca_api.lxca_api()
        if out_obj == True:
            self.sprint("Current Log Level is set to " + logging.getLevelName(api.get_log_level()))
        else:
            self.sprint("Fail to set Log Level")
        message = """
Possible Log Levels, Please use following values to set desired log level. 

\tDEBUG:        Detailed information, typically of interest only when diagnosing problems.
\tINFO:        Confirmation that things are working as expected.
\tWARNING:    An indication that something unexpected happened, or indicative of some problem in the near future. 
\tERROR:        Due to a more serious problem, the software has not been able to perform some function.
\tCRITICAL:    A serious error, indicating that the program itself may be unable to continue running.
"""
        self.sprint(message)
        return
    
###############################################################################

class ostream(InteractiveCommand):
    """
    Configure output stream or verbose level of command shell 
    
    USAGE:
        ostream -h | --help
        ostream [-l <level>]
    
    OPTIONS:
        -l, --lvl    verbose level

    """
    
    def handle_no_input(self,con_obj = None):
        self.sprint("Current ostream level is set to %s" %(self.shell.ostream.get_lvl()))
        message = """
Possible ostream levels, Please use following values to set desired stdout level. 

\t0:Quite.
\t1:Console.
\t2:File. 
\t3:Console and File.
"""
        self.sprint(message)
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
            self.sprint("Current ostream level is set to %s" %(self.shell.ostream.get_lvl()))
        else:
            self.sprint("Fail to set ostream Level")
            message = """
Possible ostream levels, Please use following values to set desired ostream level. 

\t0:Quite.
\t1:Console.
\t2:File. 
\t3:Console and File.
"""
            self.sprint(message)
        return

###############################################################################

class chassis(InteractiveCommand):
    """
    Get Chassis List and Chassis Information
    
    USAGE:
        chassis -h
        chassis [-u <chassis UUID>] [-v <view filter name>]
    
    OPTIONS:
        -h        This option displays command usage information
        -u, --uuid    chassis uuid
        -s, --status    chassis manage status (managed/unmanaged)
        -v, --view    view filter name

    """    
    
###############################################################################

class nodes(InteractiveCommand):
    """
    Retrieve nodes List and nodes Information
    
    USAGE:
        nodes -h
        nodes [-u <node UUID>] [-s <managed/unmanaged>] [-c <chassis UUID>] [-v <view filter name>]
    
    OPTIONS:
        -h        This option displays command usage information
        -u, --uuid    node uuid
        -s, --status    nodes manage status (managed/unmanaged)
        -c, --chassis    chassis uuid
        -v, --view    view filter name

    """
    
###############################################################################

class switches(InteractiveCommand):
    """
    Retrieve switches List and switches Information
    
    USAGE:
        switches -h
        switches [-u <switch UUID>] [-c <chassis UUID>] [-v <view filter name>]
        switches  [-u <switch_UUID>] [--ports <port_name>] [--action <action>]
    
    OPTIONS:
        -h            This option displays command usage information
        -u, --uuid    switch uuid
        -c, --chassis    chassis uuid
        --ports        portnames if port is empty lists ports
        --action       enable/disable ports
        -v, --view    view filter name

    """

    def handle_command(self, opts, args):

        # code to handle --ports command without value
        no_args = len(args)
        change = False
        try:
            i = args.index('--ports')
            if i < (no_args - 1):
                next_args = args[i + 1];
                if next_args.startswith("-"):
                    change = True
                else:
                    change = False
            else:
                change = True
        except ValueError:
            change = False
        if change:
            args = [w.replace('--ports', '--ports=') if w == "--ports" else  w for w in args]

        return InteractiveCommand.handle_command(self, opts, args)


###############################################################################

class fans(InteractiveCommand):
    """
    Retrieve fan List and fans Information
    
    USAGE:
        fans -h
        fans [-u <fan UUID>] [-c <chassis UUID>] [-v <view filter name>]
    
    OPTIONS:
        -h        This option displays command usage information
        -u, --uuid    fan uuid
        -c, --chassis    chassis uuid
        -v, --view    view filter name

    """
    
###############################################################################

class powersupplies(InteractiveCommand):
    """
    Retrieve Power Supply Information
    
    USAGE:
        powersupplies -h
        powersupplies [-u <power supply UUID>] [-c <chassis UUID>] [-v <view filter name>]
    
    OPTIONS:
        -h            This option displays command usage information
        -u, --uuid    power supply uuid
        -c, --chassis    chassis uuid
        -v, --view    view filter name

    """
                
###############################################################################

class fanmuxes(InteractiveCommand):
    """
    Retrieve fan Mux Information

    USAGE:
        fanmuxes -h
        fanmuxes [-u <fan mux UUID>] [-c <chassis UUID>] [-v <view filter name>]
    
    OPTIONS:
        -h        This option displays command usage information
        -u, --uuid    fan mux uuid
        -c, --chassis    chassis uuid
        -v, --view    view filter name

    """

###############################################################################

class cmms(InteractiveCommand):
    """
    Get CMM  Information
    
    USAGE:
        cmms -h
        cmms [-u <cmm UUID>] [-c <chassis UUID>] [-v <view filter name>]
    
    OPTIONS:
        -h        This option displays command usage information
        -u, --uuid    cmm uuid
        -c, --chassis    chassis uuid
        -v, --view    view filter name

    """


###############################################################################

class scalablesystem(InteractiveCommand):
    """
    Retrieve Scalable Complex System  Information
    
    USAGE:
        scalablesystem -h
        scalablesystem [-i <scalablesystem id>] [-t <scalablesystem type>] [-s <status>] [-v <view filter name>]
    
    OPTIONS:
        -h        This option displays command usage information
        -i, --id    scalable complex id
        -t, --type    type (flex/rackserver)
        -s, --status    scalable system manage status (managed/unmanaged)
        -v, --view    view filter name

"""

    
###############################################################################

class jobs(InteractiveCommand):
    """
    Retrieve and Manage information about jobs.

    USAGE:
        jobs -h | --help
        jobs [-i <job id>][-u <uuid of endpoint>][-s <jobs state>]
        jobs [-c <cancels the job with specified id>]
        jobs [-d <delete the job with specified id>]
    
    OPTIONS:
        -i, --id=    job id
        -u, --uuid=    uuid of endpoint for which jobs should be retrieved
        -s, --state=    job state to retrieve jobs in specified state.
                The state can be one of the following
                Pending
                Running
                Complete
                Cancelled
                Running_With_Errors
                Cancelled_With_Errors
                Stopped_With_Error
                Interrupted
        -c, --cancel=    cancel job of specified id
        -d, --delete=    delete job of specified id

    """
    def handle_output(self, out_obj):
        if out_obj == None:
            self.sprint("Jobs command Failed." )
        elif out_obj == False:
            self.sprint("Jobs command Failed." )
        elif out_obj == True:
            self.sprint("Jobs command succeeded" )
        return
    
###############################################################################

class discover(InteractiveCommand):
    """
    Retrieve a list of devices discovered by SLP discovery.
    
    USAGE:
        discover [-i <IP Address of endpoint>][-j <job ID>]
    
    OPTIONS:
        -i, --ip       One or more IP addresses for each endpoint to be discovered.
        -j, --job      Job ID of discover request
    

    """
    def handle_output(self, out_obj):
        if out_obj == None:
            self.sprint("Failed to start Discovery job for selected endpoint " )
        else:
            self.sprint("Discovery job started, jobId = " + out_obj)
        return
    
class manage(InteractiveCommand):
    """
    Manage the endpoint.
    
    USAGE:
        manage  -h | --help
        manage  -i <IP Address of endpoint> -u <user ID to access the endpoint>
                -p <current password to access the endpoint> [-r <recovery password for the endpoint>]
                [-f <Force Manage (True/False)>]
        manage  -j <job ID> [-v <view filter name>]

    OPTIONS:
        -i, --ip        One or more IP addresses for each endpoint to be managed.
        -u, --user      user ID to access the endpoint
        -p, --pw        The current password to access the endpoint.
        -r, --rpw       The recovery password to be used for the endpoint.
        -j, --job       Job ID of existing manage request
        -f, --force     Force Manage Boolean flag
        -v, --view      view filter name
    """
    def handle_output(self, out_obj):
        if out_obj == None:
            self.sprint("Failed to start manage job for selected endpoint " )
        else:
            self.sprint("Manage job started, jobId = " + out_obj)
        return
    
class unmanage(InteractiveCommand):
    """
    Unmanage the endpoint

    USAGE:
        unmanage -h | --help
        unmanage -i <IP Address of endpoint> [--force]
        unmanage -j <job ID> [-v <view filter name>]
    
    OPTIONS:
        -i, --ip        One or more IP addresses for each endpoint to be unmanaged.
        -f, --force     Indicates whether to force the unmanagement of an endpoint (True/False)
        -j, --job       Job ID of unmanage request
        -v, --view      View filter name

    """
    def handle_output(self, out_obj):
        if out_obj == None:
            self.sprint("Failed to start unmanage job for selected endpoint " )
        else:
            self.sprint("Unmanage job started, jobId = " + out_obj)
        return

###############################################################################

class lxcalog(InteractiveCommand):
    """
    Retrieve and Manage information about LXCA Event log.

    USAGE:
        lxcalog [-f < events that apply to the specified filters >]

    """
###############################################################################

class ffdc(InteractiveCommand):
    """
    Retrieve and Manage information about ffdc

    USAGE:
        ffdc [-u <UUID of the target endpoint>]
    
    OPTIONS:
        -u, --uuid    <UUID of the target endpoint>
    """
    def handle_output(self, out_obj):
        if out_obj == None:
            self.sprint("Failed to start ffdc job for selected endpoint " )
        else:
            self.sprint("FFDC job started, jobId = " + out_obj)
        return
###############################################################################

class users(InteractiveCommand):
    """
    Retrieve and Manage information about users.
    
    USAGE:
        users [-i <unique ID of the user to be retrieved>][-v <view filter name>]

    OPTIONS:
        -i, --id    unique ID of the user to be retrieved
        -v, --view    View filter name

    """
###############################################################################

class updatepolicy(InteractiveCommand):
    """
    Retrieve and Manage information about jobs.
    
    USAGE:
        updatepolicy [-v <view filter name>]
        updatepolicy -p <Compliance policy to be assigned to device>
        updatepolicy -i <Information type of compliance policy to be retreived>
    
    OPTIONS:
        -p, --policy    This is comma separated list of compliance policies. Each policy information
                should contain policyname, type and UUID of device separated by semicolon where -
                    Policyname = Name of the compliance-policy to be assigned to device
                    Type = The device type. This can be one of the following values.
                        CMM - Chassis Management Module
                        IOSwitch - Flex switch
                        RACKSWITCH - RackSwitch switch
                        STORAGE - Lenovo Storage system
                        xITE - Compute node or rack server
                    UUID = UUID of the device to which you want to assign the compliance policy
        -i, --info    Specifies the type of information to return. This can be one of the following values:
                    FIRMWARE- Returns information about firmware that is applicable to each managed endpoint
                    RESULTS- Returns persisted compare result for servers to which a compliance policy is assigned
        -v, --view    View filter name

    """
###############################################################################
class updaterepo(InteractiveCommand):
    """
    Retrieve and Manage information about jobs.

    USAGE:
        updaterepo -k <Key to return the specified type of update> [-v <view filter name>]
    
    OPTIONS:
        -k, --key    Returns the specified type of update. This can be one of the following values.
                    supportedMts - Returns a list of supported machine types
                    size - Returns the repository size
                    lastRefreshed - Returns the timestamp of the last repository refresh
                    importDir - Returns the import directory for the repository.
                    publicKeys - Returns the supported signed keys
                    updates - Returns information about all firmware updates
                    updatesByMt - Returns information about firmware updates for the specified machine type
                    updatesByMtByComp - Returns the update component names for the specified machine type
        -v, --view    View filter name

    """
###############################################################################
class updatecomp(InteractiveCommand):
    """
    Update the firmware of specified component.
        
    USAGE:
        updatecomp [-q <The data to return>] [-v <view filter name>]
        updatecomp  [-m <activate mode>] [-a <action to take>] [-c <information of cmms>] [-w <information of switches>] [-s <information of servers>] [-t <information of storages>]
        updatecomp  -a power [-c <cmms UUID and desired state>] [-w <switches UUID and desired state>]  [-s <servers UUID and desired state>]
    
    OPTIONS:
        -q, --query    The data to return. This can be one of the following values.
                components - Returns a list of endpoints and components that can be updated.
                status - Returns the status and progress of firmware updates. This is the default value
        -m, --mode    Indicates when to activate the update. This can be one of the following values.
                immediate - Uses Immediate Activation mode when applying firmware updates to the selected endpoints.
                delayed - Uses Delayed Activation mode when applying firmware updates to the selected endpoints.
        -a, --action    The action to take. This can be one of the following values.
                apply - Applies the associated firmware to the submitted components.
                power - Perform power action on selected endpoint.
                cancelApply - Cancels the firmware update request to the selected components.
        -c, --cmm    cmms information
        -w, --switch    switch information
        -s, --server    servers information
        -t, --storage    storages information
    
                For action = apply/cancelApply, Each of the endpoint information should contain following data separated by comma
                    UUID - UUID of the device
                    Fixid - Firmware-update ID of the target package to be applied to the component.
                    Component - Component name
    
                For action = power, Each of the endpoint information should contain following data separated by comma
                    UUID - UUID of the device
                    powerState - One of the power state values. Possible values per device type are
                        Server: powerOn, powerOff, powerCycleSoft, powerCycleSoftGraceful, powerOffHardGraceful
                        Switch: powerOn, powerOff, powerCycleSoft
                        CMM: reset
                        Storage:powerOff,powerCycleSoft
    
        -v, --view    View filter name

    """

    
###############################################################################
class configtargets(InteractiveCommand):
    """
    Retrieve and Manage information of configuration targes.
    
    USAGE:
        configtargets [-i <ID of specific profile or pattern>] [-v <view filter name>]
    
    OPTIONS:
        -i, --id    The unique ID that was assigned when the server pattern was created
        -v, --view    View filter name
    
    
    """
###############################################################################

class configpatterns(InteractiveCommand):
    """
    Retrieve and Manage information about config patterns.
    
    USAGE:
        configpatterns [-i <ID of specific pattern>] [-r <when to activate the configurations>] [-e <Comma separated list of one or more UUIDs for the target servers>] [-t <type of the target server>] [-v <view filter name>]
    
    OPTIONS:
        -i, --id    The unique ID that was assigned when the server pattern was created
        -e, --endpoint    Comma separated list of one or more UUIDs for the target servers,If a target is an empty bay,
                specify the location ID; otherwise, specify the server UUID
        -r, --restart    When to activate the configurations. This can be one of the following values:
                defer - Activate IMM settings but do not restart the server.
                immediate - Activate all settings and restart the server immediately.
                pending - Manually activate the server profile and restart the server.
        -t, --type    Type of the server, It can be one of the following
                Node
                Rack
                Tower
        -v, --view    View filter name

    """
###############################################################################

class configprofiles(InteractiveCommand):
    """
    Retrieve and Manage information of config profiles.

    USAGE:
        configprofiles [-i <ID of specific profile>] [-v <view filter name>]
    
    OPTIONS:
        -i, --id    The unique ID that was assigned when the server pattern was created
        -v, --view    View filter name

    """
###############################################################################

class manifests(PyAPI):
    """
    Send solution manifest to and retreive manifests from Lenovo XClarity Administrator.
    """

###############################################################################

class tasks(PyAPI):
    """
    Retrieve tasks List and tasks Information

    USAGE:
        tasks -h
        tasks [-u <JOB UUID>]  [-v <view filter name>]

    OPTIONS:
    -h            This option displays command usage information
        -u, --uuid    Job uuids
        -v, --view    view filter name

    """

###############################################################################


class resourcegroups(PyAPI):
    """
    create Group of Resources
    """

###############################################################################
