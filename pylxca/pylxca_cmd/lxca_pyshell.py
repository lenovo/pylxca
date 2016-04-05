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

def pyshell(shell,interactive=True):
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
              "help": help}
        ns.update()
        sys.ps1 = "PYLXCA >> "
        sys.ps2 = " ... "
        code.interact('You are in Interactive Python Shell for LXCA.', local = ns)

def connect(*args, **kwargs):
    '''
    @param
    url = url to LXCA Example. https://a.b.c.d
    user = User Id to Authenticate LXCA
    pw = Password to Authenticate LXCA
    noverify = flag to indicate to not verify server certificate
    @summary:
    Use this function to connect to LXCA
    run this function as  connect(arg1, arg2, key1 = 'val1', key2 = 'val2')
    connect( url, user, pw, noverify )

    '''
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['url','user','pw','noverify']
    if len(args) == 0 and len(kwargs) == 0:
        return
    
    for i in range(len(args)):
        #print args[i]
        kwargs[keylist[i]]= args[i]
    
    con = pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
    
    return con 
def disconnect(*args, **kwargs):
    '''
    -------
    use this function to connect to LXCA
    run this function as  connect(arg1, arg2, key1 = 'val1', key2 = 'val2')
    connect( url, user, pw, noverify )

    -------
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
    -------
    use this function to connect to LXCA
    run this function as  connect(arg1, arg2, key1 = 'val1', key2 = 'val2')
    chassis( con, uuid, status )

    -------
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
    -------
    use this function to connect to LXCA
    run this function as  connect(arg1, arg2, key1 = 'val1', key2 = 'val2')
    chassis( con, uuid, status )

    -------
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
    -------
    use this function to connect to LXCA
    run this function as  connect(arg1, arg2, key1 = 'val1', key2 = 'val2')
    chassis( con, uuid, status )

    -------
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
    -------
    use this function to connect to LXCA
    run this function as  connect(arg1, arg2, key1 = 'val1', key2 = 'val2')
    chassis( con, uuid, status )

    -------
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
    -------
    use this function to connect to LXCA
    run this function as  connect(arg1, arg2, key1 = 'val1', key2 = 'val2')
    chassis( con, uuid, status )

    -------
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
    -------
    use this function to connect to LXCA
    run this function as  connect(arg1, arg2, key1 = 'val1', key2 = 'val2')
    chassis( con, uuid, status )

    -------
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
    -------
    use this function to connect to LXCA
    run this function as  connect(arg1, arg2, key1 = 'val1', key2 = 'val2')
    chassis( con, uuid, status )

    -------
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
    -------
    use this function to connect to LXCA
    run this function as  connect(arg1, arg2, key1 = 'val1', key2 = 'val2')
    chassis( con, uuid, status )

    -------
    '''
    global pyshell
    command_name = sys._getframe().f_code.co_name
    keylist = ['con','id','type','status']
    
    for i in range(len(args)):
        kwargs[keylist[i]]= args[i]
    
    ch =  pyshell.handle_input_args(command_name,args=args,kwargs=kwargs)
    return ch