'''
Created on 15 Sep 2015

@author: root
'''

import os
import time
import signal, time, sys
import code

from pylxca.pylxca_cmd import lxca_ishell
from lxca_ishell import PYTHON_SHELL

#shell is a global variable
pyshell = None

def pyshell(shell,interactive=True):
    """ Begin user interaction """
    global pyshell
    pyshell = shell
    if interactive:
        ns = {'connect': connect,"chassis":chassis, 'help': help}
        ns.update()
        sys.ps1 = "PYLXCA >> "
        sys.ps2 = " ... "
        code.interact('You are in Interactive Python Shell for LXCA.', local = ns)

def connect(*args, **kwargs):
    '''
    -------
    use this function to connect to LXCA
    run this function as  connect(arg1, arg2, key1 = 'val1', key2 = 'val2')
    connect( url, user, pw, noverify )

    -------
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
