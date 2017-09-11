'''
@since: 5 Feb 2016
@author: Prashant Bhosale <pbhosale@lenovo.com>, Girish Kumar <gkumar1@lenovo.com>
@license: Lenovo License
@copyright: Copyright 2016, Lenovo
@organization: Lenovo 
@summary: This module provides scriptable interfaces and scriptable python shell.
'''

import os, time,code
import signal, logging, sys
import traceback

from pylxca import __version__
from pylxca.pylxca_cmd import lxca_ishell
from pylxca.pylxca_cmd.lxca_cmd import fanmuxes
from __builtin__ import ValueError

#shell is a global variable
shell_obj = None
logger = logging.getLogger(__name__)


def pyshell(shell=lxca_ishell.InteractiveShell()):
    '''
    @summary: this method provides scriptable python shell
    '''
    global shell_obj
    shell_obj = shell
    shell_obj.set_ostream_to_null()

def set_interactive():
    '''
    @summary: This method set the shell in interactive mode
    '''
    ns = {"connect": connect,
          "disconnect": disconnect,
          "chassis": chassis,
          "cmms": cmms,
          "fans": fans,
          "fanmuxes": fanmuxes,
          "switches": switches,
          "powersupplies": powersupplies,
          "nodes": nodes,
          "scalablesystem": scalablesystem,
          "discover": discover,
          "manage": manage,
          "unmanage": unmanage,
          "jobs": jobs,
          "users": users,
          "lxcalog": lxcalog,
          "ffdc": ffdc,
          "updatecomp": updatecomp,
          "updatepolicy": updatepolicy,
          "updaterepo": updaterepo,
          "configpatterns": configpatterns,
          "configprofiles": configprofiles,
          "configtargets": configtargets,
          "tasks": tasks,
          "manifests": manifests,
          "osimages": osimages,
          "resourcegroups": resourcegroups, 
          "help": help}
    ns.update()
    global __version__
    code.interact('Interactive Python Shell for Lenovo XClarity Administrator v' + __version__ + '\nType "dir()" or "help(lxca command object)" for more information.', local=ns)


def connect(*args, **kwargs):

    '''

@summary:
    Use this function to connect to Lenovo XClarity Administrator
    run this function as  
    
    con_variable = connect( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
        
        keylist = ['url','user','pw','noverify']

@param
    The parameters for this command are as follows 
    
        con          Connection Object to Lenovo XClarity Administrator
        url          url to Lenovo XClarity Administrator Example. https://a.b.c.d
        user         User Id to Authenticate Lenovo XClarity Administrator
        pw           Password to Authenticate Lenovo XClarity Administrator
        noverify     flag to indicate to not verify server certificate

@example 
    con1 = connect( con = "https://10.243.12.142",user = "USERID", pw = "Password", noverify = "True")
    '''
    global shell_obj
    command_name = sys._getframe().f_code.co_name
    keylist = ['url','user','pw','noverify']
    if len(args) == 0 and len(kwargs) == 0:
        return
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    con = shell_obj.handle_input_args(command_name, args=args, kwargs=kwargs)
    
    return con 
def disconnect(*args, **kwargs):

    '''

@summary:
    Use this function to disconnect from Lenovo XClarity Administrator
    run this function as  
        disconnect()  

@param
    The parameters for this command are as follows
        
        con      Connection Object to Lenovo XClarity Administrator
    
@example 
    disconnect()
    '''

    global shell_obj
    command_name = sys._getframe().f_code.co_name
    keylist = ['con']
    if len(args) == 0 and len(kwargs) == 0:
        return
    
    for i in range(len(args)):
        #print args[i]
        kwargs[keylist[i]]= args[i]
    
    con = shell_obj.handle_input_args(command_name, args=args, kwargs=kwargs)
    
    return con 

def cmms(*args, **kwargs):
    '''

@summary:
    Use this function to get CMMs information
    run this function as  
    
    data_dictionary = cmms( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
        
        keylist = ['con','uuid','chassis']

@param
    The parameters for this command are as follows 
    
    con       Connection Object to Lenovo XClarity Administrator
    uuid      cmm uuid
    chassis   chassis uuid  

@example 
    cmm_list = cmms( con = con1 ,uuid = 'fc3058cadf8b11d48c9b9b1b1b1b1b57', pw = 'Password', noverify = "True")
    '''
    global shell_obj
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','uuid','chassis']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  shell_obj.handle_input_args(command_name, args=args, kwargs=kwargs)
    return ch

def chassis(*args, **kwargs):
    '''

@summary:
    Use this function to get Chassis information
    run this function as  
    
    data_dictionary = chassis( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
        
        keylist = ['con','uuid','status']

@param
    The parameters for this command are as follows 
    
    con        Connection Object to Lenovo XClarity Administrator
    uuid       chassis uuid
    status     chassis manage status (managed/unmanaged)
    

@example 
    
    '''
    global shell_obj
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','uuid','status']
    
    for i in range(len(args)):
        #print args[i]
        kwargs[keylist[i]]= args[i]
    
    ch =  shell_obj.handle_input_args(command_name, args=args, kwargs=kwargs)
    return ch

def fans(*args, **kwargs):
    '''

@summary:
    Use this function to get fans information
    run this function as  
    
    data_dictionary = fans( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
        
        keylist = ['con','uuid','chassis']

@param
    The parameters for this command are as follows 
    
    con           Connection Object to Lenovo XClarity Administrator
    uuid          uuid of fan
    chassis       chassis uuid
    
@example 
    
    '''
    global shell_obj
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','uuid','chassis']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  shell_obj.handle_input_args(command_name, args=args, kwargs=kwargs)
    return ch

def fanmuxes(*args, **kwargs):
    '''

@summary:
    Use this function to get fanmuxes information
    run this function as  
    
    data_dictionary = fanmuxes( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
        
        keylist = ['con','uuid','chassis']

@param
    The parameters for this command are as follows 
    
    con           Connection Object to Lenovo XClarity Administrator
    uuid          uuid of fanmux
    chassis       chassis uuid
    
@example 
    
    '''
    global shell_obj
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','uuid','chassis']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  shell_obj.handle_input_args(command_name, args=args, kwargs=kwargs)
    return ch

def nodes(*args, **kwargs):
    '''

@summary:
    Use this function to get nodes information
    run this function as  
    
    data_dictionary = nodes( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
        
        keylist = ['con','uuid','chassis','status']

@param
    The parameters for this command are as follows 
    
    con           Connection Object to Lenovo XClarity Administrator
    uuid          uuid of node
    chassis       chassis uuid
    status        nodes manage status (managed/unmanaged)
    
@example 
    
    '''
    global shell_obj
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','uuid','chassis','status']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  shell_obj.handle_input_args(command_name, args=args, kwargs=kwargs)
    return ch

def switches(*args, **kwargs):
    '''

@summary:
    Use this function to get switches information
    run this function as  
    
    data_dictionary = switches( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
        
        keylist = ['con','uuid','chassis']

@param
    The parameters for this command are as follows 
    
    con      Connection Object to Lenovo XClarity Administrator
    uuid          uuid of switch
    chassis       chassis uuid
    
@example 
    
    '''
    global shell_obj
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','uuid','chassis','ports','action']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  shell_obj.handle_input_args(command_name, args=args, kwargs=kwargs)
    return ch

def powersupplies(*args, **kwargs):
    '''

@summary:
    Use this function to get powersupplies information
    run this function as  
    
    data_dictionary = powersupplies( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
        
        keylist = ['con','uuid','chassis']

@param
    The parameters for this command are as follows 
    
    con      Connection Object to Lenovo XClarity Administrator
    uuid          uuid of power supply
    chassis       chassis uuid
    
@example 
    
    '''
    global shell_obj
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','uuid','chassis']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  shell_obj.handle_input_args(command_name, args=args, kwargs=kwargs)
    return ch

def scalablesystem(*args, **kwargs):
    '''

@summary:
    Use this function to get scalablesystem information
    run this function as  
    
    data_dictionary = scalablesystem( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
        
        keylist = ['con','id','type']

@param
    The parameters for this command are as follows 
    
    con      Connection Object to Lenovo XClarity Administrator
    id        scalable complex id
    type      type (flex/rackserver)

@example 
    
    '''
    global shell_obj
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','id','type']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  shell_obj.handle_input_args(command_name, args=args, kwargs=kwargs)
    return ch

def discover(*args, **kwargs):
    '''

@summary:
    Use this function to discover endpoint from Lenovo XClarity Administrator
    run this function as  
    
    data_dictionary = discover( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
        
        keylist = ['con','ip','job']

@param
    The parameters for this command are as follows 
    
    con    Connection Object to Lenovo XClarity Administrator
    ip     One or more IP addresses for each endpoint to be discovered.
    job    Job ID of discover request


@example
 
    For Getting Maangement job status
        
        job_data = discover(con=con1,job=jobid)
            
    '''
    global shell_obj
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','ip','job']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  shell_obj.handle_input_args(command_name, args=args, kwargs=kwargs)
    return ch

def manage(*args, **kwargs):
    '''

@summary:
    Use this function to manage endpoint from Lenovo XClarity Administrator
    run this function as  
    
    data_dictionary = manage( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
        
        keylist = ['con','ip','user','pw','rpw','job','force']

@param
    The parameters for this command are as follows 
    
        con      Connection Object to Lenovo XClarity Administrator
        ip       One or more IP addresses for each endpoint to be managed.
        user     user ID to access the endpoint
        pw       The current password to access the endpoint.
        rpw      The recovery password to be used for the endpoint.
        force     force manage
        job       Job ID of existing manage request
        
        Note : mp, type and epuuid parameters are dedpriciated and only kept for backword compatibility. 

@example 

        jobid = manage(con=con1,ip="10.243.6.68",user="USERID",pw="PASSW0RD",rpw="PASSW0RD")
    
    or with named variable it can be represented as
    
        jobid = manage(con= con1,ip="10.243.6.68",user="USERID","PASSW0RD","PASSW0RD",True)
            
    For Getting Maangement job status
        
        manage_data = manage(con=con1,job=jobid)
    '''
    global shell_obj
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','ip','user','pw','rpw','job','force']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  shell_obj.handle_input_args(command_name, args=args, kwargs=kwargs)
    return ch

def unmanage(*args, **kwargs):
    '''

@summary:
    Use this function to unmanage endpoint from Lenovo XClarity Administrator
    run this function as  
    
    data_dictionary = unmanage( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
        
        keylist = ['con','ip','force','job']

@param
    The parameters for this command are as follows 
    
        ip          one or more endpoints to be unmanaged.
                    This is comma separated list of multiple endpoints, each endpoint should
                    contain endpoint information separated by semicolon.
                    endpoint's IP Address(multiple addresses should be separated by #), UUID of the endpoint and
                    Type of endpoint to be unmanaged ,This can be one of the following values:
                          Chassis
                          ThinkServer
                          Storage
                          Rackswitch
                          Rack-Tower
        force       Indicates whether to force the unmanagement of an endpoint (True/False)
        job         Job ID of unmanage request

@example 

    '''
    global shell_obj
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','ip','force','job']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  shell_obj.handle_input_args(command_name, args=args, kwargs=kwargs)
    return ch

def configpatterns(*args, **kwargs):
    '''

@summary:
    Use this function to Retrieve information and deploy all server and category patterns
            that have been defined in the Lenovo XClarity Administrator
            
    run this function as  
    
    data_dictionary = configpatterns( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
        
        keylist = ['con','id', 'includeSettings', 'endpoint','restart','type', pattern_update_dict]

@param
    The parameters for this command are as follows 
    
        id          The unique ID that was assigned when the server pattern was created
        
        endpoint    List of one or more UUIDs for the target servers,If a target is an empty bay,
                      specify the location ID; otherwise, specify the server UUID
        
        restart     When to activate the configurations. This can be one of the following values:
                      defer - Activate IMM settings but do not restart the server.
                      immediate - Activate all settings and restart the server immediately.
                      pending - Manually activate the server profile and restart the server.
        
        type        Type of the server, It can be one of the following
                      Node
                      Rack
                      Tower

        pattern_update_dict  dictionary of category_pattern to import.

@example 

    '''    
    global shell_obj
    command_name = sys._getframe().f_code.co_name
    if len(args) < 1 or len(args) > 2:
        raise ValueError("Invalid Input Arguments")

    param_dict = {}
    con = None

    keylist = ['con', 'id', 'includeSettings', 'endpoint', 'restart', 'type', 'pattern_update_dict']
    optional_keylist = ['id', 'includeSettings', 'endpoint', 'restart', 'type', 'pattern_update_dict']
    mutually_exclusive_keys = ['id', 'pattern_update_dict']
    mandatory_options_list = {'id': [], 'endpoint': ['type', 'restart'], 'pattern_update_dict': [],
                              'includeSettings': ['id']}

    _validate_param(keylist, mandatory_options_list, optional_keylist, mutually_exclusive_keys,
                        con, param_dict, *args, **kwargs)

    out_obj = shell_obj.handle_input_dict(command_name, con, param_dict)
    return out_obj


def configprofiles(*args, **kwargs):
    '''

@summary:
    Use this function to Retrieve information server configuration profiles
            that have been defined in the Lenovo XClarity Administrator
    
    run this function as  
    
    data_dictionary = configprofiles( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
        
        keylist = ['con', 'id', 'name', 'endpoint', 'restart', 'delete', 'unassign', 'powerdown', 'resetimm', 'force']

@param
    The parameters for this command are as follows 
    
        id          The unique ID that was assigned when the server profile was created
        name        profile name
        endpoint    endpoint  UUID of the server or location id for flex system
        restart     restart server to activate profile ( immediate / defer )
        delete      True for delete id
        unassign    unassign specified id
                    options for unassign
        powerdown   powerdown server
        resetIMM    reset IMM
        force       force unassign operation

@example 

    '''
    global shell_obj
    command_name = sys._getframe().f_code.co_name
    keylist = ['con', 'id', 'name', 'endpoint', 'restart', 'delete', 'unassign', 'powerdown', 'resetimm', 'force']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]

    logger.info(" configprofiles got kwargs %s " % str(kwargs))
    ch =  shell_obj.handle_input_args(command_name, args=args, kwargs=kwargs)
    return ch

def configttargets(*args, **kwargs):
    '''

@summary:
    Use this function to get config pattern targets from Lenovo XClarity Administrator
    run this function as  
    
    data_dictionary = configtargets( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
        
        keylist = ['con','ep','force','job']

@param
    The parameters for this command are as follows 
    
        ep          one or more endpoints to be unmanaged.
                    This is comma separated list of multiple endpoints, each endpoint should
                    contain endpoint information separated by semicolon.
                    endpoint's IP Address(multiple addresses should be separated by #), UUID of the endpoint and
                    Type of endpoint to be unmanaged ,This can be one of the following values:
                          Chassis
                          ThinkServer
                          Storage
                          Rackswitch
                          Rack-Tower
        force       Indicates whether to force the unmanagement of an endpoint (True/False)
        job         Job ID of unmanage request

@example 

    '''
    global shell_obj
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','id','force','job']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  shell_obj.handle_input_args(command_name, args=args, kwargs=kwargs)
    return ch

def updatepolicy(*args, **kwargs):
    '''

@summary:
    Use this function to read Firmwar update Policy from Lenovo XClarity Administrator
    run this function as  
    
    data_dictionary = updatepolicy( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
        
        keylist = ['con','info','job','uuid',policy','Type']

@param
    The parameters for this command are as follows 

    info    Specifies the type of information to return. This can be one of the following values:
                FIRMWARE- Returns information about firmware that is applicable to each managed endpoint
                RESULTS- Returns persisted compare result for servers to which a compliance policy is assigned

    jobid    Job ID of assign compliance policy operation

    uuid     UUID of the device to which you want to assign the compliance policy

    policy   Policyname, Name of the compliance-policy to be assigned to device

    Type     Device type. This can be one of the following values.
                    CMM - Chassis Management Module
                    IOSwitch - Flex switch
                    RACKSWITCH - RackSwitch switch
                    STORAGE - Lenovo Storage system
                    SERVER - Compute node or rack server

@example

    '''
    global shell_obj
    command_name = sys._getframe().f_code.co_name
    keylist = ['con', 'info', 'job', 'uuid', 'policy','type']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]

    logger.info(" updatepolicy got kwargs %s " %str(kwargs))
    ch =  shell_obj.handle_input_args(command_name, args=args, kwargs=kwargs)
    return ch

def updaterepo(*args, **kwargs):
    '''

@summary:
    Use this function to get repository info from Lenovo XClarity Administrator
    run this function as  
    
    data_dictionary = updaterepo( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
        
        keylist = ['con','key']

@param
    The parameters for this command are as follows 
    
    key    Returns the specified type of update. This can be one of the following values.
                supportedMts - Returns a list of supported machine types
                size - Returns the repository size
                lastRefreshed - Returns the timestamp of the last repository refresh
                importDir - Returns the import directory for the repository.
                publicKeys - Returns the supported signed keys
                updates - Returns information about all firmware updates
                updatesByMt - Returns information about firmware updates for the specified machine type
                updatesByMtByComp - Returns the update component names for the specified machine type

    action    The action to take. This can be one of the following values.
                read - Reloads the repository files. The clears the update information in cache and reads the update file again from the repository.
                refresh - Retrieves information about the latest available firmware updates from the Lenovo Support website,
                         and stores the information to the firmware-updates repository.
                acquire - Downloads the specified firmware updates from Lenovo Support website, and stores the updates to the firmware-updates repository.
                delete - Deletes the specified firmware updates from the firmware-updates repository.
                export.not supported

     mt        comma separated machine types
     scope     scope of operation
     fixids    comma separated fixids
     type      filetype for PUT opertaion
@example 

    '''
    global shell_obj
    command_name = sys._getframe().f_code.co_name
    keylist = ['con', 'key', 'action', 'mt', 'scope', 'fixids', 'type']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  shell_obj.handle_input_args(command_name, args=args, kwargs=kwargs)
    return ch

def updatecomp(*args, **kwargs):
    '''

@summary:
    Use this function to update firmware of endpoint from Lenovo XClarity Administrator
    run this function as  
    
    data_dictionary = updatecomp( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
    
    USAGE:

        keylist = ['con','query','mode','action','cmm','switch','server','storage']

@param
    The parameters for this command are as follows 
    
    query   The data to return. This can be one of the following values.
                components - Returns a list of devices and components that can be updated.
                status - Returns the status and progress of firmware updates. This is the default value
    
    mode    Indicates when to activate the update. This can be one of the following values.
                immediate - Uses Immediate Activaton mode when applying firmware updates to the selected endpoints.
                delayed - Uses Delayed Activaton mode when applying firmware updates to the selected endpoints.
    
    action  The action to take. This can be one of the following values.
                apply - Applies the associated firmware to the submitted components.
                power - Perform power action on selected endpoint.
                cancelApply - Cancels the firmware update request to the selected components.

    cmm     cmms information
    switch  switch information
    server  servers information
    storage storages information

            For action = apply/cancelApply, Device information should contain following data separated by comma
                UUID - UUID of the device
                Fixid - Firmware-update ID of the target package to be applied to the component. If not provided assigned policy would be used.
                Component - Component name

            For action = power, Device information should contain following data separated by comma
                UUID - UUID of the device
                powerState - One of the power state values. Possible values per device type are
                    Server: powerOn, powerOff, powerCycleSoft, powerCycleSoftGraceful, powerOffHardGraceful
                    Switch: powerOn, powerOff, powerCycleSoft
                    CMM: reset
                    Storage:powerOff,powerCycleSoft



@example 

    '''
    global shell_obj
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','query','mode','action','cmm','switch','server','storage']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  shell_obj.handle_input_args(command_name, args=args, kwargs=kwargs)
    return ch



def users(*args, **kwargs):
    '''

@summary:
    Use this function to get users data from Lenovo XClarity Administrator
    run this function as  
    
    data_dictionary = users( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
        
        keylist = ['con','id']

@param
    The parameters for this command are as follows 
    
        id    unique ID of the user to be retrieved

@example 

    '''
    global shell_obj
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','id']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  shell_obj.handle_input_args(command_name, args=args, kwargs=kwargs)
    return ch

def ffdc(*args, **kwargs):
    '''

@summary:
    Use this function to Collect and export specific endpoint data 
        from Lenovo XClarity Administrator
    
    run this function as  
    
    data_dictionary = ffdc( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
        
        keylist = ['con','uuid']

@param
    The parameters for this command are as follows 
    
        uuid    UUID of the target endpoint

@example 

    '''
    global shell_obj
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','uuid']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  shell_obj.handle_input_args(command_name, args=args, kwargs=kwargs)
    return ch


def log(*args, **kwargs):
    '''

@summary:
    Use this function to get Lenovo XClarity Administrator LOG information
    run this function as

    data_dictionary = log( key1 = 'val1', key2 = 'val2', ...)

    Where KeyList is as follows

        keylist = ['con','filter']

@param
    The parameters for this command are as follows

        filter  filter for the event

@example

    '''
    global shell_obj
    command_name = sys._getframe().f_code.co_name
    keylist = ['lvl']

    for i in range(len(args)):
        kwargs[keylist[i]] = args[i]

    ch = shell_obj.handle_input_args(command_name, args=args, kwargs=kwargs)
    return ch

def lxcalog(*args, **kwargs):
    '''

@summary:
    Use this function to get Lenovo XClarity Administrator LOG information
    run this function as  
    
    data_dictionary = lxcalog( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
        
        keylist = ['con','filter']

@param
    The parameters for this command are as follows 
    
        filter  filter for the event

@example 

    '''
    global shell_obj
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','filter']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  shell_obj.handle_input_args(command_name, args=args, kwargs=kwargs)
    return ch

def jobs(*args, **kwargs):
    '''

@summary:
    Use this function to get jobs information from Lenovo XClarity Administrator
    run this function as  
    
    data_dictionary = jobs( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
        
        keylist = ['con','id','uuid','state','cancel','delete']

@param
    The parameters for this command are as follows 
    
        id=         job id
        uuid=       uuid of endpoint for which jobs should be retrieved
        state=      job state to retrieve jobs in specified state.
                      The state can be one of the following
                      Pending
                      Running
                      Complete
                      Cancelled
                      Running_With_Errors
                      Cancelled_With_Errors
                      Stopped_With_Error
                      Interrupted
        cancel=     cancel job of specified id
        delete=     delete job of specified id

@example 

    '''
    global shell_obj
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','id','uuid','state','cancel','delete']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  shell_obj.handle_input_args(command_name, args=args, kwargs=kwargs)
    return ch

def manifests(*args, **kwargs):
    '''

@summary:
    Use this function to send solution manifest to and retreive manifests from Lenovo XClarity Administrator
    run this function as  
    
    data_dictionary = manifests( conn_handle, input_args_dictionary{key,value} )
    
    Where KeyList is as follows
        
        keylist = [id','file']

@param
    The parameters for this command are as follows 
    
        id=         solution id
        file=       path to manifest file

@example 

    '''
    global shell_obj
    con = None
    param_dict = {}
    
    command_name = sys._getframe().f_code.co_name
    
    if len(args) < 1 or len(args) > 2:
        raise ValueError("Invalid Input Arguments")
    
    for i in range(len(args)):
        if isinstance(args[i], dict):
            param_dict = args[i]
        else:
            con = args[i]
            
    out_obj =  shell_obj.handle_input_dict(command_name, con, param_dict)
    # return out_obj
    return True


def tasks(*args, **kwargs):
    '''

@summary:
    Use this function to get tasks information
    run this function as

     = tasks( con, data_dictionary)

    Where data_dictionary contain input arguments as follows

        keylist = ['jobuuid']

@param
    The parameters for this command are as follows

    con      Connection Object to Lenovo XClarity Administrator
    uuid          uuid of job


@example

    '''
    global shell_obj
    con = None
    param_dict = {}

    command_name = sys._getframe().f_code.co_name

    if len(args) < 1 or len(args) > 2:
        raise ValueError("Invalid Input Arguments")

    for i in range(len(args)):
        if isinstance(args[i], dict):
            param_dict = args[i]
        else:
            con = args[i]

    out_obj = shell_obj.handle_input_dict(command_name, con, param_dict)
    return out_obj


def resourcegroups(*args, **kwargs):
    '''

@summary:
    Use this function to Create, modify, delete or read resource group from Lenovo XClarity Administrator
    run this function as

    data_dictionary = resourcegroups( con_handle,uuid, name, desc, type, solutionVPD, members, criteria )

    Where KeyList is as follows

        keylist = ['uuid', 'name','description','type','solutionVPD','members','criteria']

@param
    The parameters for this command are as follows

        uuid=         UUID of already created Group 
        name=         Name of Resource Group
        desc=         Description of Resource Group
        type=         Type of Resource Group. <{"static", "dynamic", "solution"}>,
        solutionVPD": { "id": <UUID string>,
                        "machineType": <machine type string>,
                        "model": <model string>,
                        "serialNumber": <serial number string>,
                        "manufacturer": <string>
                      },

        "members": [ "uri","uri",....],
        "criteria":[]

@example

    '''
    global shell_obj
    con = None
    arglist = list(args)
    param_dict = {}

    command_name = sys._getframe().f_code.co_name

    keylist = ['con','uuid','name','description','type','solutionVPD','members','criteria']
    optional_keylist = ['uuid','name','description','type','solutionVPD','members','criteria']
    mutually_exclusive_keys = ['uuid', 'name']
    mandatory_options_list = {'uuid':[],'name':['type']}

    if len(args) == 0 and len(kwargs) == 0:
        raise AttributeError("Invalid Input Arguments")

    arglist = arglist[::-1]

    for key in keylist:
        if (key in kwargs.keys()):
            param_dict[key] = kwargs[key]
        elif len(arglist)>=1:
            param_dict[key] = arglist.pop()
        elif key not in optional_keylist:
            raise ValueError("Invalid Input Arguments")
        
        if key == 'con':
            con = param_dict.pop(key)
      
    if not con:
        raise AttributeError("Invalid command invocation: Connection Object missing.")
    
    me_key_found = False
    for me_key in param_dict.keys():
        #Checking mandatory option_list presence
        if me_key in mandatory_options_list.keys():
            if not set(mandatory_options_list[me_key]).issubset(set(param_dict.keys())):
                raise AttributeError("Invalid command invocation")
            
        #Checking mutually exclusive key presense 
        if me_key in mutually_exclusive_keys:
            if me_key_found:
                raise AttributeError("Invalid command invocation")
            me_key_found = True
            
    out_obj = shell_obj.handle_input_dict(command_name, con, param_dict)
    return out_obj


def _validate_param(keylist, mandatory_options_list, optional_keylist, mutually_exclusive_keys, con, param_dict, *args, **kwargs):
    '''
     validate parameters
    :param arglist: list of arguments derived from args

    :param keylist: keylist of name of fields
    :param mandatory_options_list:
    :param optional_keylist:
    :param mutually_exclusive_keys:
    :param con:  return parameter
    :param param_dict: append to param_dict
    :return:
    '''
    arglist = list(args)
    arglist = arglist[::-1]

    for key in keylist:
        if (key in kwargs.keys()):
            param_dict[key] = kwargs[key]
        elif len(arglist) >= 1:
            param_dict[key] = arglist.pop()
        elif key not in optional_keylist:
            logger.error(" Invalid Input args %s is not in optional list %s" %(key, str(mandatory_options_list)))
            raise ValueError("Invalid Input Arguments")

        if key == 'con':
            con = param_dict.pop(key)

    if not con:
        raise AttributeError("Invalid command invocation: Connection Object missing.")

    logger.debug(" Parameter dict %s " %str(param_dict))

    me_key_found = False
    for me_key in param_dict.keys():
        # Checking mandatory option_list presence
        if me_key in mandatory_options_list.keys():
            if not set(mandatory_options_list[me_key]).issubset(set(param_dict.keys())):
                logger.error(" Invalid command invocation %s of mandatory list %s is not in arguments parovided" % (me_key, str(mandatory_options_list)))
                raise AttributeError("Invalid command invocation")

        # Checking mutually exclusive key presense
        if me_key in mutually_exclusive_keys:
            if me_key_found:
                logger.error(" Invalid command invocation %s of mutual exclusive list %s " % (
                me_key, str(mutually_exclusive_keys)))
                raise AttributeError("Invalid command invocation")
            me_key_found = True


def osimages(con, *args, **kwargs):
    '''
    @summary:
        Use this function to retrieve information about, delete, and import OS images, OS-image profiles, device driver, and boot-options files.
        data_dictionary = osimages(input_args, key=values )

        Where KeyList is as follows

            keylist = [fileName, Id, profile,remoteFileServer,imageType,jobId, ...]

    @param

        - osimages(hostplatforms)
        - osimages(hostplatforms, **kwargs)

        - osimages(osdeployment, items=[])
        - osimages(osdeployment, action=<>,mac=<>,nodeName=<>)

        - osimages(connection)

        - osimages(globalSettings)
        - osimages(globalSettings, **kwargs)

        - osimages()
        - osimages(imageType=<DUD,BOOT,OS,OSPROFILE>)

        - osimages(fileName=<>)

        - osimages(id=<>)
        - osimages(id=<>, **kwargs)

        - osimages(jobid = <>)

        - osimages(remoteFileServers)
        - osimages(remoteFileServers, **kwargs)

        - osimages(remoteFileServers, id=<>)
        - osimages(remoteFileServers, putId/deleteId=<>, **kwargs)
    @example
        osimage()                   : shows osimages
        osimage(imageType='BOOT')   : POST osimage with imageType='BOOT'
        osimages(fileName='foo')    : shows osimages for fileName='foo'
    '''

    global shell_obj
    #con = None
    param_dict = {}
    command_name = sys._getframe().f_code.co_name

    # con = kwargs.get('con')
    # if not con:
    #     raise ValueError("Invalid Input Arguments")

    logger.info(" osimages got kwargs %s " % str(kwargs))
    param_dict = (args, kwargs)
    logger.info(" osimages got param_dict %s " % str(param_dict))
    # handle_input_dict only takes param_dict as input argument
    ch = shell_obj.handle_input_dict(command_name, con, param_dict)
    return ch
