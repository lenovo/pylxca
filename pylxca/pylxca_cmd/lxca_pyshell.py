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
              "help": help}
        ns.update()
        sys.ps1 = "PYLXCA >> "
        sys.ps2 = " ... "
        code.interact('You are in Interactive Python Shell for LXCA.', local = ns)

def connect(*args, **kwargs):

    '''

@summary:
    Use this function to connect to LXCA
    run this function as  
    
    con_variable = connect( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
        
        keylist = ['url','user','pw','noverify']

@param
    The parameters for this command are as follows 
    
        con          Connection Object to LXCA
        url          url to LXCA Example. https://a.b.c.d
        user         User Id to Authenticate LXCA
        pw           Password to Authenticate LXCA
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
    Use this function to disconnect from LXCA
    run this function as  
        disconnect()  

@param
    The parameters for this command are as follows
        
        con      Connection Object to LXCA
    
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
    
    con       Connection Object to LXCA
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
    
    con        Connection Object to LXCA
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
    
    con           Connection Object to LXCA
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
    
    con           Connection Object to LXCA
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
    
    con           Connection Object to LXCA
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
    
    con      Connection Object to LXCA
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
    
    con      Connection Object to LXCA
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
    
    con      Connection Object to LXCA
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
    Use this function to discover endpoint from LXCA
    run this function as  
    
    data_dictionary = discover( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
        
        keylist = ['con','ip','job']

@param
    The parameters for this command are as follows 
    
    con      Connection Object to LXCA
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
    Use this function to manage endpoint from LXCA
    run this function as  
    
    data_dictionary = manage( key1 = 'val1', key2 = 'val2', ...)
    
    Where KeyList is as follows
        
        keylist = ['con','ip','user','pw','rpw','mp','type','epuuid','job']

@param
    The parameters for this command are as follows 
    
        con      Connection Object to LXCA
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
        job       Job ID of existing manage request

@example 

        jobid = manage(con=con1,ip="10.243.6.68",user="USERID",pw="PASSW0RD",rpw="PASSW0RD",mp=
            "cimxml-http;5988;true,cimxml-https;5989;true,http;80;true,snmpv3;163;true,https;443;true,
            snmpv1;161;true,ssh;22;true,telnet;23;true,rem-pres;3900;true,rmcp;623;true",
            type="Rack-Tower",epuuid="fc3058cadf8b11d48c9b9b1b1b1b1b57")
    
    or with named variable it can be represented as
    
        jobid = manage(con= con1,ip="10.243.6.68",user="USERID","PASSW0RD","PASSW0RD",
            "cimxml-http;5988;true,cimxml-https;5989;true,http;80;true,snmpv3;163;true,https;443;true,
            snmpv1;161;true,ssh;22;true,telnet;23;true,rem-pres;3900;true,rmcp;623;true",
            "Rack-Tower","fc3058cadf8b11d48c9b9b1b1b1b1b57")
            
    For Getting Maangement job status
        
        manage_data = manage(con=con1,job=jobid)
    '''
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','ip','user','pw','rpw','mp','type','epuuid','job']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
    return ch

def unmanage(*args, **kwargs):
    '''

@summary:
    Use this function to manage endpoint from LXCA
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
    -------
    use this function to unmanage chassis from LXCA
    run this function as  unmanage(arg1, arg2, key1 = 'val1', key2 = 'val2')
    unmanage( con, ep,force )

    -------
    '''
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','ep','force','job']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
    return ch

def configprofiles(*args, **kwargs):
    '''
    -------
    use this function to unmanage chassis from LXCA
    run this function as  unmanage(arg1, arg2, key1 = 'val1', key2 = 'val2')
    unmanage( con, ep,force )

    -------
    '''
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','ep','force','job']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
    return ch

def configtargets(*args, **kwargs):
    '''
    -------
    use this function to unmanage chassis from LXCA
    run this function as  unmanage(arg1, arg2, key1 = 'val1', key2 = 'val2')
    unmanage( con, ep,force )

    -------
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
    -------
    use this function to unmanage chassis from LXCA
    run this function as  unmanage(arg1, arg2, key1 = 'val1', key2 = 'val2')
    unmanage( con, ep,force )

    -------
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
    -------
    use this function to unmanage chassis from LXCA
    run this function as  unmanage(arg1, arg2, key1 = 'val1', key2 = 'val2')
    unmanage( con, ep,force )

    -------
    '''
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','ep','force','job']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
    return ch

def updatecomp(*args, **kwargs):
    '''
    -------
    use this function to unmanage chassis from LXCA
    run this function as  unmanage(arg1, arg2, key1 = 'val1', key2 = 'val2')
    unmanage( con, ep,force )

    -------
    '''
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','ep','force','job']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
    return ch



def users(*args, **kwargs):
    '''
    -------
    use this function to unmanage chassis from LXCA
    run this function as  unmanage(arg1, arg2, key1 = 'val1', key2 = 'val2')
    unmanage( con, ep,force )

    -------
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
    -------
    use this function to unmanage chassis from LXCA
    run this function as  unmanage(arg1, arg2, key1 = 'val1', key2 = 'val2')
    unmanage( con, ep,force )

    -------
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
    -------
    use this function to unmanage chassis from LXCA
    run this function as  unmanage(arg1, arg2, key1 = 'val1', key2 = 'val2')
    unmanage( con, ep,force )

    -------
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
    -------
    use this function to unmanage chassis from LXCA
    run this function as  unmanage(arg1, arg2, key1 = 'val1', key2 = 'val2')
    unmanage( con, ep,force )

    -------
    '''
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','id','uuid','state','cancel','delete']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
    return ch