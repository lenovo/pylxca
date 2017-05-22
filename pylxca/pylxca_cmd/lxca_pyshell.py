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

from pylxca.pylxca_cmd import lxca_ishell
from lxca_ishell import PYTHON_SHELL
from pylxca.pylxca_cmd.lxca_cmd import fanmuxes
from __builtin__ import ValueError

#shell is a global variable
pyshell = None
logger = logging.getLogger(__name__)

def pyshell(shell=lxca_ishell.InteractiveShell(),interactive=False):
    '''
    @summary: this method provides scriptable interactive python shell 
    '''
    global pyshell
    pyshell = shell
    pyshell.set_ostream_to_null()
    if interactive:
        ns = {"connect": connect,
              "disconnect": disconnect,
              "chassis":chassis,
              "cmms":cmms,
              "fans":fans,
              "fanmuxes":fanmuxes,
              "switches":switches, 
              "powersupplies":powersupplies,
              "nodes":nodes, 
              "scalablesystem":scalablesystem,
              "discover":discover,
              "manage":manage,
              "unmanage":unmanage,
              "jobs":jobs, 
              "users":users,
              "lxcalog":lxcalog,
              "ffdc":ffdc,
              "updatecomp":updatecomp,
              "updatepolicy":updatepolicy,
              "updaterepo":updaterepo,
              "configpatterns":configpatterns,
              "configprofiles":configprofiles,
              "configtargets":configtargets,
              "manifests":manifests,
              "help": help}
        ns.update()
        sys.ps1 = "pyshell >> "
        sys.ps2 = " ... "
        code.interact('You are in Interactive Python Shell for Lenovo XClarity Administrator.', local = ns)

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
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['url','user','pw','noverify']
    if len(args) == 0 and len(kwargs) == 0:
        return
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    con = pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
    
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

    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['con']
    if len(args) == 0 and len(kwargs) == 0:
        return
    
    for i in range(len(args)):
        #print args[i]
        kwargs[keylist[i]]= args[i]
    
    con = pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
    
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
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','uuid','chassis']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
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
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','uuid','status']
    
    for i in range(len(args)):
        #print args[i]
        kwargs[keylist[i]]= args[i]
    
    ch =  pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
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
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','uuid','chassis']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
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
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','uuid','chassis']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
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
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','uuid','chassis','status']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
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
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','uuid','chassis']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
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
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','uuid','chassis']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
    return ch

def scalablesystem(*args, **kwargs):
    '''

@summary:
    Use this function to get scalablesystem information
    run this function as  
    
    data_dictionary = scalablesystem( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
        
        keylist = ['con','id','type','status']

@param
    The parameters for this command are as follows 
    
    con      Connection Object to Lenovo XClarity Administrator
    id        scalable complex id
    type      type (flex/rackserver)
    status    scalable system manage status (managed/unmanaged)

@example 
    
    '''
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','id','type','status']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
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
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','ip','job']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
    return ch

def manage(*args, **kwargs):
    '''

@summary:
    Use this function to manage endpoint from Lenovo XClarity Administrator
    run this function as  
    
    data_dictionary = manage( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
        
        keylist = ['con','ip','user','pw','rpw','mp','type','epuuid','job']

@param
    The parameters for this command are as follows 
    
        con      Connection Object to Lenovo XClarity Administrator
        ip       One or more IP addresses for each endpoint to be managed.
        user     user ID to access the endpoint
        pw       The current password to access the endpoint.
        rpw      The recovery password to be used for the endpoint.
        mp       A list of endpoint management ports, it is a comma separated list of
                      management port information. Each management port includes protocol, port number and
                      boolean flag of whether the port enabled (True/False) respectively. These properties
                      should be separate by semicolon. See the discovey request job response
                      body for the supported protocols for the endpoint's management ports.
        type     Type of endpoint to be managed. This can be one of the following values:
                                  Chassis
                                  ThinkServer
                                  Storage
                                  Rackswitch
                                  Rack-Tower
        epuuid    UUID of endpoint to be managed
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
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','ip','user','pw','rpw','mp','type','epuuid','job','force']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
    return ch

def unmanage(*args, **kwargs):
    '''

@summary:
    Use this function to unmanage endpoint from Lenovo XClarity Administrator
    run this function as  
    
    data_dictionary = unmanage( key1 = 'val1', key2 = 'val2', ...)
    
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
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','ep','force','job']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
    return ch

def configpatterns(*args, **kwargs):
    '''

@summary:
    Use this function to Retrieve information and deploy all server and category patterns
            that have been defined in the Lenovo XClarity Administrator
            
    run this function as  
    
    data_dictionary = configpatterns( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
        
        keylist = ['con','id','endpoint','restart','type']

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


@example 

    '''    
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','id','endpoint','restart','type']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
    return ch

def configprofiles(*args, **kwargs):
    '''

@summary:
    Use this function to Retrieve information server configuration profiles
            that have been defined in the Lenovo XClarity Administrator
    
    run this function as  
    
    data_dictionary = configprofiles( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
        
        keylist = ['con','id']

@param
    The parameters for this command are as follows 
    
        id    The unique ID that was assigned when the server profile was created

@example 

    '''
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','id']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
    return ch

def configtargets(*args, **kwargs):
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
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','ep','force','job']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
    return ch

def updatepolicy(*args, **kwargs):
    '''

@summary:
    Use this function to read Firmwar update Policy from Lenovo XClarity Administrator
    run this function as  
    
    data_dictionary = updatepolicy( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
        
        keylist = ['con','policy','info']

@param
    The parameters for this command are as follows 
    
    policy  This is comma separated list of compliance policies. Each policy information
            should contain policyname, type and UUID of device separated by semicolon where -
                Policyname = Name of the compliance-policy to be assigned to device
                Type = The device type. This can be one of the following values.
                    CMM - Chassis Management Module
                    IOSwitch - Flex switch
                    RACKSWITCH - RackSwitch switch
                    STORAGE - Lenovo Storage system
                    xITE - Compute node or rack server
                UUID = UUID of the device to which you want to assign the compliance policy
                
    info    Specifies the type of information to return. This can be one of the following values:
                FIRMWARE- Returns information about firmware that is applicable to each managed endpoint
                RESULTS- Returns persisted compare result for servers to which a compliance policy is assigned
                
@example 

    '''
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','policy','info']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
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

@example 

    '''
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','key']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
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
                components - Returns a list of endpoints and components that can be updated.
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

            For action = apply/cancelApply, Each of the endpoint infomration should contain following data separated by comma
                UUID:       UUID of the device
                Fixid:      Firmware-updare ID of the target package to be applied to the component.
                Component:  Component name
    
            For action = power, Each of the endpoint infomration should contain UUID and desired powerState separated by comma
                UUID - UUID of the device
                
                Desired powerState can have one of the power state values. Possible values per device type are
                    Server: powerOn, powerOff, powerCycleSoft, powerCycleSoftGraceful, powerOffHardGraceful
                    Switch: powerOn, powerOff, powerCycleSoft
                    CMM: reset

@example 

    '''
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','query','mode','action','cmm','switch','server','storage']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
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
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','id']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
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
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','uuid']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
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
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','filter']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
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
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','id','uuid','state','cancel','delete']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
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
    global pyshell
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
            
    out_obj =  pyshell.handle_input_dict(command_name,con,param_dict)
    return out_obj
