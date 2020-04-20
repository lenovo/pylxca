'''
@since: 5 Feb 2016
@author: Prashant Bhosale <pbhosale@lenovo.com>, Girish Kumar <gkumar1@lenovo.com>
@license: Lenovo License
@copyright: Copyright 2016, Lenovo
@organization: Lenovo
@summary: This module provides scriptable interfaces and scriptable python shell.
'''

import code
import logging
import sys

from pylxca import __version__
from pylxca.pylxca_cmd import lxca_ishell
from pylxca.pylxca_cmd.lxca_cmd import fanmuxes

# shell is a global variable
SHELL_OBJ = None
LOGGER = logging.getLogger(__name__)


def pyshell(shell=lxca_ishell.InteractiveShell()):
    '''
    @summary: this method provides scriptable python shell
    '''
    global SHELL_OBJ
    SHELL_OBJ = shell
    SHELL_OBJ.set_ostream_to_null()


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
          "storedcredentials": storedcredentials,
          "managementserver": managementserver,
          "help": help}
    ns.update()
    global __version__
    code.interact('Interactive Python Shell for Lenovo XClarity Administrator v' + __version__ +
                  '\nType "dir()" or "help(lxca command object)" for more information.', local=ns)


def connect(*args, **kwargs):
    '''

@summary:
    Use this function to connect to Lenovo XClarity Administrator
    run this function as
    con_variable = connect( key1 = 'val1', key2 = 'val2', ...)

    Where KeyList is as follows

        keylist = ['url', 'user', 'pw', 'noverify']

@param
    The parameters for this command are as follows
        con          Connection Object to Lenovo XClarity Administrator
        url          url to Lenovo XClarity Administrator Example. https://a.b.c.d
        user         User Id to Authenticate Lenovo XClarity Administrator
        pw           Password to Authenticate Lenovo XClarity Administrator
        noverify     flag to indicate to not verify server certificate

@example 
    con1 = connect( url = "<ipaddress>",user = "<user>", pw = "<password>", noverify = "True")
    '''
    global SHELL_OBJ
    command_name = sys._getframe().f_code.co_name
    keylist = ['url', 'user', 'pw', 'noverify']
    if len(args) == 0 and len(kwargs) == 0:
        return

    for i in range(len(args)):
        kwargs[keylist[i]] = args[i]

    con = SHELL_OBJ.handle_input_args(command_name, args=args, kwargs=kwargs)

    return con


def disconnect(*args, **kwargs):
    '''

@summary:
    Use this function to disconnect from Lenovo XClarity Administrator
    run this function as
    disconnect()


     it also reset internal current connection to original connection this is used in api version
     to retain origianal connection if we are disconnecting other than current connection

     i.e
     con1 = connect(...)
     con2 = connect(...)
     con3 = connect(...)
     con4 = connect(...)  current internal connection is con4

     disconnect(con2)  will keep current connection to con4
     disconnect(con4) or disconnect() will set current connection to None


@param
    The parameters for this command are as follows

        con      Connection Object to Lenovo XClarity Administrator

@example 
    disconnect()
    '''
    global SHELL_OBJ

    command_name = sys._getframe().f_code.co_name
    param_dict = {}
    con = None

    long_short_key_map = {}
    keylist = ['con']
    optional_keylist = ['con']
    mutually_exclusive_keys = []
    mandatory_options_list = {}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict, False)
    return out_obj


def cmms(*args, **kwargs):
    '''

@summary:
    Use this function to get CMMs information
    run this function as  

    data_dictionary = cmms( key1 = 'val1', key2 = 'val2', ...)

    Where KeyList is as follows

        keylist = ['con', 'uuid', 'chassis']

@param
    The parameters for this command are as follows 

    con       Connection Object to Lenovo XClarity Administrator
    uuid      cmm uuid
    chassis   chassis uuid  

@example 
    cmm_list = cmms( con = con1, uuid = 'fc3058cadf8b11d48c9b9b1b1b1b1b57')
    '''
    global SHELL_OBJ
    command_name = sys._getframe().f_code.co_name
    param_dict = {}
    con = None

    long_short_key_map = {'uuid': 'u', 'chassis': 'c'}
    keylist = ['con', 'uuid', 'chassis']
    optional_keylist = ['con', 'uuid', 'chassis']
    mutually_exclusive_keys = ['uuid', 'chassis']
    mandatory_options_list = {}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict)
    return out_obj


def chassis(*args, **kwargs):
    '''

@summary:
    Use this function to get Chassis information
    run this function as  

    data_dictionary = chassis( key1 = 'val1', key2 = 'val2', ...)

    Where KeyList is as follows

        keylist = ['con', 'uuid', 'status']

@param
    The parameters for this command are as follows 

    con        Connection Object to Lenovo XClarity Administrator
    uuid       chassis uuid
    status     chassis manage status (managed/unmanaged)


@example 
    chassis_list = chassis( con = con1, uuid = 'fc3058cadf8b11d48c9b9b1b1b1b1b57')
    '''
    global SHELL_OBJ
    command_name = sys._getframe().f_code.co_name
    param_dict = {}
    con = None

    long_short_key_map = {'uuid': 'u', 'status': 's'}
    keylist = ['con', 'uuid', 'status']
    optional_keylist = ['con', 'uuid', 'status']
    mutually_exclusive_keys = []
    mandatory_options_list = {}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict)
    return out_obj


def fans(*args, **kwargs):
    '''

@summary:
    Use this function to get fans information
    run this function as  

    data_dictionary = fans( key1 = 'val1', key2 = 'val2', ...)

    Where KeyList is as follows

        keylist = ['con', 'uuid', 'chassis']

@param
    The parameters for this command are as follows 

    con           Connection Object to Lenovo XClarity Administrator
    uuid          uuid of fan
    chassis       chassis uuid

@example 
    fans_list = fans( con = con1, uuid = 'fc3058cadf8b11d48c9b9b1b1b1b1b57')
    '''
    global SHELL_OBJ
    command_name = sys._getframe().f_code.co_name
    param_dict = {}
    con = None

    long_short_key_map = {'uuid': 'u', 'chassis': 'c'}
    keylist = ['con', 'uuid', 'chassis']
    optional_keylist = ['con', 'uuid', 'chassis']
    mutually_exclusive_keys = ['uuid', 'chassis']
    mandatory_options_list = {}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict)
    return out_obj


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
    global SHELL_OBJ
    command_name = sys._getframe().f_code.co_name
    param_dict = {}
    con = None

    long_short_key_map = {'uuid': 'u', 'chassis': 'c'}
    keylist = ['con', 'uuid', 'chassis']
    optional_keylist = ['con', 'uuid', 'chassis']
    mutually_exclusive_keys = ['uuid', 'chassis']
    mandatory_options_list = {}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict)
    return out_obj


def nodes(*args, **kwargs):
    '''

@summary:
    Use this function to get nodes information
    run this function as  

    data_dictionary = nodes( key1 = 'val1', key2 = 'val2', ...)

    Where KeyList is as follows

        keylist = ['con','uuid','chassis','status', 'modify', 'metrics']

@param
    The parameters for this command are as follows 

    con           Connection Object to Lenovo XClarity Administrator
    uuid          uuid of node
    chassis       chassis uuid
    status        nodes manage status (managed/unmanaged)
    modify        JSON object of modifyable node properties
    metrics       flag to fetch metrics of all nodes or metrics of a node belonging to the provided uuid

@example 

    nodes(uuid="FAA6E3D494E511E6A0739B91ED670CE8",modify='{"location":{"location": "new location", "rack": "rack 5","lowestRackUnit": 3}}')
    
    '''
    global SHELL_OBJ
    command_name = sys._getframe().f_code.co_name
    param_dict = {}
    con = None

    long_short_key_map = {'uuid': 'u', 'chassis': 'c', 'status': 's', 'modify': 'm', 'metrics': 'x'}
    keylist = ['con', 'uuid', 'chassis', 'status', 'modify', 'metrics']
    optional_keylist = ['con', 'uuid', 'chassis', 'status', 'modify', 'metrics']
    mutually_exclusive_keys = ['uuid', 'chassis']
    mandatory_options_list = {}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict)
    return out_obj


def switches(*args, **kwargs):
    '''

@summary:
    Use this function to get switches information
    run this function as  

    data_dictionary = switches( key1 = 'val1', key2 = 'val2', ...)

    Where KeyList is as follows

        keylist = ['con','uuid','chassis','ports','action']

@param
    The parameters for this command are as follows 

    con      Connection Object to Lenovo XClarity Administrator
    uuid          uuid of switch
    chassis       chassis uuid
    ports         empty ports string list all ports for uuid, comma separated ports
    action        enable/disable ports

@example 

    '''
    global SHELL_OBJ
    command_name = sys._getframe().f_code.co_name

    param_dict = {}
    con = None

    # other parameter don't have short option
    long_short_key_map = {'uuid': 'u', 'chassis': 'c'}
    keylist = ['con', 'uuid', 'chassis', 'ports', 'action']
    optional_keylist = ['con', 'uuid', 'chassis', 'ports', 'action']
    mutually_exclusive_keys = ['uuid', 'chassis']
    mandatory_options_list = {}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict)
    return out_obj


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
    global SHELL_OBJ
    command_name = sys._getframe().f_code.co_name
    param_dict = {}
    con = None
    long_short_key_map = {'uuid': 'u', 'chassis': 'c'}
    keylist = ['con', 'uuid', 'chassis']
    optional_keylist = ['con', 'uuid', 'chassis']
    mutually_exclusive_keys = ['uuid', 'chassis']
    mandatory_options_list = {}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict)
    return out_obj


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
    global SHELL_OBJ
    command_name = sys._getframe().f_code.co_name

    param_dict = {}
    con = None

    long_short_key_map = {'id': 'i', 'type': 't'}
    keylist = ['con', 'id', 'type']
    optional_keylist = ['con', 'id', 'type']
    mutually_exclusive_keys = []
    mandatory_options_list = {}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict)
    return out_obj


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
    global SHELL_OBJ
    command_name = sys._getframe().f_code.co_name
    param_dict = {}
    con = None

    long_short_key_map = {'ip': 'i', 'job': 'j'}
    keylist = ['con', 'ip', 'job']
    optional_keylist = ['con', 'ip', 'job']
    mutually_exclusive_keys = ['ip', 'job']
    mandatory_options_list = {}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)
    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict)
    return out_obj


def manage(*args, **kwargs):
    '''

@summary:
    Use this function to manage endpoint from Lenovo XClarity Administrator
    run this function as  

    data_dictionary = manage( key1 = 'val1', key2 = 'val2', ...)

    Where KeyList is as follows

        keylist = ['con','subcmd','ip','user','pw','rpw','job','force', 'storedcredential_id']

@param
    The parameters for this command are as follows 

        con      Connection Object to Lenovo XClarity Administrator
        subcmd
        ip       One or more IP addresses for each endpoint to be managed.
        user     user ID to access the endpoint
        pw       The current password to access the endpoint.
        rpw      The recovery password to be used for the endpoint.
        force     force manage
        job       Job ID of existing manage request
        storedcredential_id    Store Crendential Id to be used for device manage operation
                        if this is provided user is not required
        Note : mp, type and epuuid parameters are dedpriciated and only kept for backword compatibility. 

@example 

        jobid = manage(con=con1, subcmd='device', ip="<deviceip>",user="<deviceuser>",pw="<devicepassword>",rpw="<devicerecoverypassword>")
        jobid = manage(con=con1, subcmd='device', ip="<deviceip>",storedcredintail_id="<storedcredentialid>")

    or with named variable it can be represented as

        jobid = manage(con= con1, subcmd='device', ip="<deviceip>",user="<deviceuser>","<devicepassword>","<devicerecoverypassword>",True)
        jobid = manage(con1, subcmd='device', i="<deviceip>", u='<deviceuser>', p='<devicepassword>', r='<devicerecoverypassword>', f='True')

        Using storedcredential id for Rackswitch
        jobid = manage(con=con1, subcmd='device', i='<deviceip>', s='<storedcredentialid>', f='True')

        Using storedcredential id for Rackswitch Server
        jobid = manage(con=con1, subcmd='device',i="<deviceip>", r='<devicepassword>', s='<storedcredentialid>', f='True')


    For Getting Maangement job status

        jobid = manage(con=con1, subcmd='job_status', job="JOB_ID")
    '''
    global SHELL_OBJ
    command_name = sys._getframe().f_code.co_name

    param_dict = {}
    con = None

    long_short_key_map = {'ip': 'i', 'user': 'u', 'pw': 'p',
                          'rpw': 'r', 'job': 'j', 'force': 'f', 'storedcredential_id': 's'}
    keylist = ['con', 'subcmd', 'ip', 'user', 'pw',
               'rpw', 'job', 'force', 'storedcredential_id']
    optional_keylist = ['con', 'ip', 'user', 'pw',
                        'rpw', 'job', 'force', 'storedcredential_id']
    mutually_exclusive_keys = ['ip', 'job']
    mandatory_options_list = {'job': []}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict)
    return out_obj


def unmanage(*args, **kwargs):
    '''

@summary:
    Use this function to unmanage endpoint from Lenovo XClarity Administrator
    run this function as  

    data_dictionary = unmanage( key1 = 'val1', key2 = 'val2', ...)

    Where KeyList is as follows

        keylist = ['con','subcmd','ip','force','job']

@param
    The parameters for this command are as follows 
        subcmd      device \ job_status
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
    endpoint = 'ENDPOINT_IP;<uuid>;Rack-Tower'
    unmanage(con_lxca, subcmd=device, i=endpoint)
    '''
    global SHELL_OBJ
    command_name = sys._getframe().f_code.co_name
    param_dict = {}
    con = None

    long_short_key_map = {'ip': 'i', 'job': 'j', 'force': 'f'}
    keylist = ['con', 'subcmd', 'ip', 'force', 'job']
    optional_keylist = ['con', 'ip', 'force', 'job']
    mutually_exclusive_keys = ['ip', 'job']
    mandatory_options_list = {}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict)
    return out_obj


def configpatterns(*args, **kwargs):
    '''

@summary:
    Use this function to Retrieve information and deploy all server and category patterns
            that have been defined in the Lenovo XClarity Administrator

    run this function as  

    data_dictionary = configpatterns( key1 = 'val1', key2 = 'val2', ...)

    Where KeyList is as follows

        keylist = ['con','subcmd','id', 'includeSettings', 'endpoint','restart','type', pattern_update_dict, name, status]

@param
    The parameters for this command are as follows 
        subcmd     list, apply, import , status
        id          The unique ID that was assigned when the server pattern was created
        name        name of pattern , this is used for apply
        endpoint    List of one or more UUIDs for the target servers,If a target is an empty bay,
                      specify the location ID; otherwise, specify the server UUID

        restart     When to activate the configurations. This can be one of the following values:
                      defer - Activate IMM settings but do not restart the server.
                      immediate - Activate all settings and restart the server immediately.
                      pending - Manually activate the server profile and restart the server.

        type        Type of the server, It can be one of the following
                      flex -  Flex System Placeholder chassis empty bays
                      node
                      rack
                      tower

        pattern_update_dict  dictionary of category_pattern to import.

        status      check config status for given uuid in endpoint
                    True

@example 

    list  all configpatterns
        rep = configpatterns(con, subcmd = 'list')

    list particular configpattern
        rep = configpatterns(con, subcmd = 'list', id="53")

    list particular configpattern with includeSettings
        rep = configpatterns(con, subcmd = 'list', id="53", includeSettings="True")

    import SystemInfo category pattern

        py_dict = {
            "template_type": "SystemInfo",
            "template": {
                "contact": "contact",
                "description": "Pattern created by testAPI",
                "location": "location",
                "name": "Learned-System_Info-19",
                "systemName": {
                    "autogen": "Disable",
                    "hyphenChecked": False
                },
                "type": "SystemInfo",
                "uri": "/config/template/61",
                "userDefined": True
            }
        }
        import json
        my_json = json.dumps(py_dict)
        rep = configpatterns(con_lxca, 'import', pattern_update_dict = my_json )
    '''
    global SHELL_OBJ
    command_name = sys._getframe().f_code.co_name

    param_dict = {}
    con = None

    # some of them don't have short options
    long_short_key_map = {'id': 'i', 'endpoint': 'e', 'restart': 'r',
                          'type': 't', 'name': 'n', 'pattern_update_dict': 'p'}
    keylist = ['con', 'subcmd', 'id', 'includeSettings', 'endpoint',
               'restart', 'type', 'pattern_update_dict', 'name']
    optional_keylist = ['con', 'id', 'includeSettings', 'endpoint',
                        'restart', 'type', 'pattern_update_dict', 'name']
    mutually_exclusive_keys = ['id', 'pattern_update_dict']
    mandatory_options_list = {'id': [], 'pattern_update_dict': []}
    #                          'includeSettings': ['id']}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict)
    return out_obj


def configprofiles(*args, **kwargs):
    '''

@summary:
    Use this function to Retrieve information server configuration profiles
            that have been defined in the Lenovo XClarity Administrator

    run this function as  

    data_dictionary = configprofiles( key1 = 'val1', key2 = 'val2', ...)

    Where KeyList is as follows

        keylist = ['con', 'subcmd', 'id', 'name', 'endpoint', 'restart', 'powerdown', 'resetimm', 'resetswitch', 'force']

@param
    The parameters for this command are as follows 
        subcmd      list, rename, activate, unassign, delete
        id          The unique ID that was assigned when the server profile was created
        name        profile name
        endpoint    endpoint  UUID of the server or location id for flex system
        restart     restart server to activate profile ( immediate / defer )

                    options for unassign
        powerdown   powerdown server
        resetimm    reset IMM
        resetswitch  Identifies whether to reset the switch internal port settings to default values
        force       force unassign operation

@example
    rep = configprofiles(con_lxca, 'list')
    rep = configprofiles(con_lxca, 'list','3')
    '''
    global SHELL_OBJ
    command_name = sys._getframe().f_code.co_name

    param_dict = {}
    con = None
    # some of keys don't have short option
    long_short_key_map = {'id': 'i', 'name': 'n', 'endpoint': 'e', 'restart': 'r',
                          'powerdown': 'p', 'force': 'f'}
    keylist = ['con', 'subcmd', 'id', 'name', 'endpoint',
               'restart', 'powerdown', 'resetimm', 'resetswitch', 'force']
    optional_keylist = ['con', 'id', 'name', 'endpoint',
                        'restart', 'powerdown', 'resetimm', 'resetswitch', 'force']
    mutually_exclusive_keys = []
    mandatory_options_list = {'id': [], 'endpoint': ['restart']}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict)

    #remove dummy field added for view
    if 'dummy' in out_obj:
        out_obj.pop('dummy')
    return out_obj


    return out_obj


def configtargets(*args, **kwargs):
    '''

@summary:
    Use this function to get config pattern targets from Lenovo XClarity Administrator
    run this function as  

    data_dictionary = configtargets( key1 = 'val1', key2 = 'val2', ...)

    Where KeyList is as follows

        keylist = ['con','id']

@param
    The parameters for this command are as follows 
        id    config target id

@example 

    '''
    global SHELL_OBJ
    command_name = sys._getframe().f_code.co_name
    param_dict = {}
    con = None
    long_short_key_map = {'id': 'i'}
    keylist = ['con', 'id']
    optional_keylist = ['con']
    mutually_exclusive_keys = []
    mandatory_options_list = {}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict)
    return out_obj


def updatepolicy(*args, **kwargs):
    '''

@summary:
    Use this function to read Firmwar update Policy from Lenovo XClarity Administrator
    run this function as  

    data_dictionary = updatepolicy( key1 = 'val1', key2 = 'val2', ...)

    Where KeyList is as follows

        keylist = ['con', 'subcmd', 'info','job','uuid',policy','Type']

@param
    The parameters for this command are as follows 
    subcmd  list,query, assign , status
    info    Specifies the type of information to return. This can be one of the following values:
                FIRMWARE- Returns information about firmware that is applicable to each managed endpoint
                RESULTS- Returns persisted compare result for servers to which a compliance policy is assigned
                NAMELIST -  Returns the available compliance policies
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
    global SHELL_OBJ
    command_name = sys._getframe().f_code.co_name

    param_dict = {}
    con = None
    long_short_key_map = {'info': 'i', 'job': 'j',
                          'uuid': 'u', 'policy': 'p', 'type': 't'}
    keylist = ['con', 'subcmd', 'info', 'job', 'uuid', 'policy', 'type']
    optional_keylist = ['con', 'info', 'job', 'uuid', 'policy', 'type']
    mutually_exclusive_keys = []
    mandatory_options_list = {}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict)
    return out_obj


def updaterepo(*args, **kwargs):
    '''

@summary:
    Use this function to get repository info from Lenovo XClarity Administrator
    run this function as  

    data_dictionary = updaterepo( key1 = 'val1', key2 = 'val2', ...)

    Where KeyList is as follows

        keylist = ['con', 'subcmd', 'key', 'mt', 'scope', 'fixids', 'type']

@param
    The parameters for this command are as follows 


    subcmd    The action to take. This can be one of the following values.
                query - Get  info using key parameter
                read - Reloads the repository files. The clears the update information in cache and reads the update file again from the repository.
                refresh - Retrieves information about the latest available firmware updates from the Lenovo Support website,
                         and stores the information to the firmware-updates repository.
                acquire - Downloads the specified firmware updates from Lenovo Support website, and stores the updates to the firmware-updates repository.
                delete - Deletes the specified firmware updates from the firmware-updates repository.
                export.not supported

    key    Returns the specified type of update. This can be one of the following values.
                supportedMts - Returns a list of supported machine types
                size - Returns the repository size
                lastRefreshed - Returns the timestamp of the last repository refresh
                importDir - Returns the import directory for the repository.
                publicKeys - Returns the supported signed keys
                updates - Returns information about all firmware updates
                updatesByMt - Returns information about firmware updates for the specified machine type
                updatesByMtByComp - Returns the update component names for the specified machine type


     mt        comma separated machine types
     scope     scope of operation
     fixids    comma separated fixids
     type      filetype for PUT opertaion
@example 
     rep = updaterepo(con, "query", k="size")
     rep = updaterepo(con, subcmd = "read")
     rep = updaterepo(con_lxca, subcmd = "read")
     rep = updaterepo(con_lxca, subcmd = "acquire", mt="7903")
    '''
    global SHELL_OBJ
    command_name = sys._getframe().f_code.co_name

    param_dict = {}
    con = None

    long_short_key_map = {'key': 'k', 'mt': 'm',
                          'scope': 's', 'fixids': 'f', 'type': 't'}
    keylist = ['con', 'subcmd', 'key', 'mt', 'scope', 'fixids', 'type']
    optional_keylist = ['con', 'key', 'mt', 'scope', 'fixids', 'type']
    mutually_exclusive_keys = []
    mandatory_options_list = {}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict)
    return out_obj


def updatecomp(*args, **kwargs):
    '''

@summary:
    Use this function to update firmware of endpoint from Lenovo XClarity Administrator
    run this function as

    data_dictionary = updatecomp( key1 = 'val1', key2 = 'val2', ...)

    Where KeyList is as follows

    USAGE:

        keylist = ['con','subcmd', 'query','mode','action','cmm','switch','server','storage','dev_list']

@param
    The parameters for this command are as follows
    subcmd  info|apply
    query   The data to return. This can be one of the following values.
                components - Returns a list of devices and components that can be updated.
                status - Returns the status and progress of firmware updates. This is the default value

    mode    Indicates when to activate the update. This can be one of the following values.
                immediate - Uses Immediate Activaton mode when applying firmware updates to the selected endpoints.
                delayed - Uses Delayed Activaton mode when applying firmware updates to the selected endpoints.
                prioritized. Firmware updates on the baseboard management controller are activated immediately

    action  The action to take. This can be one of the following values.
                apply - Applies the associated firmware to the submitted components.
                power - Perform power action on selected endpoint.
                cancelApply - Cancels the firmware update request to the selected components.

    cmm     cmms information
    switch  switch information
    server  servers information
    storage storages information
    dev_list  - update all updateable components
            For action = apply/cancelApply, Device information should contain following data separated by comma
                UUID - UUID of the device
                Fixid - Firmware-update ID of the target package to be applied to the component.
                         If not provided assigned policy would be used.
                Component - Component name

            For action = power, Device information should contain following data separated by comma
                UUID - UUID of the device
                powerState - One of the power state values. Possible values per device type are
                    Server: powerOn, powerOff, powerCycleSoft, powerCycleSoftGraceful, powerOffHardGraceful
                    Switch: powerOn, powerOff, powerCycleSoft
                    CMM: reset
                    Storage:powerOff,powerCycleSoft

@example
Applying firmware update to server
endpoint = "38B1DC62084411E88C7A0A94EF4EC2EF,lnvgy_fw_lxpm_pdl116o-1.40_anyos_noarch,LXPM Diagnostic Software"
rep = updatecomp(con, 'apply', action='apply', mode='immediate', server=endpoint)

Applying firmware update using dev_list json format

dev_list = {
   "DeviceList": [{
      "ServerList": [{
         "UUID": "38B1DC62084411E88C7A0A94EF4EC2EF",
         "Components": [{
            "Fixid": "lnvgy_fw_lxpm_pdl116o-1.40_anyos_noarch",
            "Component": "LXPM Diagnostic Software"
         }]
      }]
   },
   {
      "CMMList": []
   },
   {
      "SwitchList": []
   },
   {
      "StorageList": []
   }]
}

dev_json = json.dumps(dev_list)
rep = updatecomp(con, 'apply', action='apply', mode='immediate', dev_list=dev_json)

    '''
    global SHELL_OBJ
    command_name = sys._getframe().f_code.co_name

    param_dict = {}
    con = None
    long_short_key_map = {'query': 'q', 'mode': 'm', 'action': 'a', 'cmm': 'c', 'switch': 'w', 'server': 's',
                          'storage': 't', 'dev_list': 'l'}
    keylist = ['con', 'subcmd', 'query', 'mode', 'action', 'cmm',
               'switch', 'server', 'storage', 'dev_list']
    optional_keylist = ['con', 'query', 'mode', 'action',
                        'cmm', 'switch', 'server', 'storage', 'dev_list']
    mutually_exclusive_keys = []
    mandatory_options_list = {}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict)
    return out_obj


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
    global SHELL_OBJ
    command_name = sys._getframe().f_code.co_name

    param_dict = {}
    con = None
    long_short_key_map = {'id': 'i'}
    keylist = ['con', 'id']
    optional_keylist = ['con', 'id']
    mutually_exclusive_keys = []
    mandatory_options_list = {}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict)
    return out_obj


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

        uuid    UUID of the target endpoint this is manadatory parameter

@example
    ffdc(con = lxca_con, uuid='UUID of endpoint")

    '''
    global SHELL_OBJ
    command_name = sys._getframe().f_code.co_name

    param_dict = {}
    con = None
    long_short_key_map = {'uuid': 'u'}
    keylist = ['con', 'uuid']
    optional_keylist = ['con', 'uuid']
    mutually_exclusive_keys = []
    mandatory_options_list = {}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict)
    return out_obj


def log(*args, **kwargs):
    '''

@summary:
    Use this function to get Lenovo XClarity Administrator LOG information
    run this function as

    data_dictionary = log( key1 = 'val1', key2 = 'val2', ...)

    Where KeyList is as follows

        keylist = ['con','lvl']

@param
    The parameters for this command are as follows

        lvl  log level to be set
        Possible Log Levels, Please use following values to set desired log level.

        DEBUG:        Detailed information, typically of interest only when diagnosing problems.
        INFO:        Confirmation that things are working as expected.
        WARNING:    An indication that something unexpected happened, or indicative of some problem in the near future.
        ERROR:        Due to a more serious problem, the software has not been able to perform some function.
        CRITICAL:    A serious error, indicating that the program itself may be unable to continue running.

@example

    '''
    global SHELL_OBJ
    command_name = sys._getframe().f_code.co_name

    param_dict = {}
    con = None

    long_short_key_map = {'lvl': 'l'}
    keylist = ['con', 'lvl']
    optional_keylist = ['con', 'lvl']
    mutually_exclusive_keys = []
    mandatory_options_list = {}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict)
    return out_obj


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
    global SHELL_OBJ
    command_name = sys._getframe().f_code.co_name

    param_dict = {}
    con = None

    long_short_key_map = {'filter': 'f'}
    keylist = ['con', 'filter']
    optional_keylist = ['con', 'filter']
    mutually_exclusive_keys = []
    mandatory_options_list = {}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict)
    return out_obj


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
    global SHELL_OBJ
    command_name = sys._getframe().f_code.co_name

    param_dict = {}
    con = None

    long_short_key_map = {'id': 'i', 'uuid': 'u',
                          'state': 's', 'cancel': 'c', 'delete': 'd'}
    keylist = ['con', 'id', 'uuid', 'state', 'cancel', 'delete']
    optional_keylist = ['con', 'id', 'uuid', 'state', 'cancel', 'delete']
    mutually_exclusive_keys = ['id', 'cancel', 'delete']
    mandatory_options_list = {}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict)
    return out_obj


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
    global SHELL_OBJ

    command_name = sys._getframe().f_code.co_name

    param_dict = {}
    con = None

    long_short_key_map = {'id': 'i', 'file': 'f'}
    keylist = ['con', 'id', 'file']
    optional_keylist = ['con', 'file']
    mutually_exclusive_keys = []
    mandatory_options_list = {}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict)
    # return out_obj
    return True


def tasks(*args, **kwargs):
    '''

@summary:
    Use this function to get tasks information
    run this function as

     = tasks( con, data_dictionary)

    Where data_dictionary contain input arguments as follows

        keylist = ['jobUID','children','action', 'updateList']

@param
    The parameters for this command are as follows

    con      Connection Object to Lenovo XClarity Administrator
    jobUID          uuid of job
    children        result will include children if True
    action          cancel/update/create
    updateList      required for update action , string containing list of update

@example
    update_list = [{"jobUID":"9","percentage":50}]
    str_u = str(update_list)
    rep = tasks(con_lxca, a = 'update', u = str_u)
    '''
    global SHELL_OBJ
    con = None
    param_dict = {}

    command_name = sys._getframe().f_code.co_name

    param_dict = {}
    con = None

    long_short_key_map = {'jobUID': 'j', 'children': 'c',
                          'action': 'a', 'updateList': 'u', 'template': 't'}
    keylist = ['con', 'jobUID', 'children', 'action', 'updateList','template']
    optional_keylist = ['con', 'jobUID', 'children', 'action', 'updateList','template']
    mutually_exclusive_keys = []
    mandatory_options_list = {}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict)
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
    list all resourcegroups
    rep = resourcegroups(con_lxca, 'list')

    list criteria properties for dynamic groups
    rep = resourcegroups(con_lxca, 'criteriaproperties')

    For creating dynamic group
    criteria = {
				u'parent': u'root',
				u'value': None,
				u'criteria': [{
						u'operator': u'contains',
						u'value': u'test',
						u'property': u'hostname',
						u'id': u'1001',
						u'parent': u'lxca_customUI_resourceViews_allGroupsPage_editGroupDynamicPage_2'
					}
				],
				u'operator': u'AND',
				u'property': None,
				u'id': u'root'
			}

    criteria_json = json.dumps(criteria)
    print criteria_json
    rep = resourcegroups(con_lxca, 'create', n="TEST_DYNAMIC", d="TRIAL_GROUP", t='dynamic', c=criteria_json)

    Updating dynamic group
    rep = resourcegroups(con_lxca, 'update', u="5C5AB42D94C6A719BEF2A375", n="R1_GROUP", d="TRIAL_GROUP modified", t='dynamic', c=criteria_json)

    Delete resouregroup
    rep = resourcegroups(con_lxca, 'delete', u="5C5BC6EA90F54D074FC7BC0D")

    Create solution group supported for api only for uhm
    solutionVPD = {
               'id': '59A54997C18DCF0594A8CCD1',
               'machineType': 'TESTMTM',
               'model': 'TESTMODEL',
               'serialNumber': 'TESTSERIAL',
               'manufacturer': 'LENOVO'}
    members = []
    criteria = []

    rep = resourcegroups(con_lxca, 'create', n="TEST_solution", d="Test_GROUP", t='solution', s=solutionVPD, m=members, c=criteria)


    '''
    global SHELL_OBJ
    con = None
    param_dict = {}

    command_name = sys._getframe().f_code.co_name

    long_short_key_map = {'uuid': 'u', 'name': 'n', 'description': 'd', 'type': 't', 'solutionVPD': 's',
                          'members': 'm', 'criteria': 'c'}

    keylist = ['con', 'subcmd', 'uuid', 'name', 'description',
               'type', 'solutionVPD', 'members', 'criteria']
    optional_keylist = ['con', 'uuid', 'name', 'description',
                        'type', 'solutionVPD', 'members', 'criteria']
    mutually_exclusive_keys = []
    mandatory_options_list = {'uuid': [], 'name': ['type']}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist, mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    LOGGER.debug("resourcegroups %s" %str(param_dict))
    if 'type' in param_dict:
        if 'solution' in param_dict['type']:
            out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict, False)
        else:
            out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict)
    else:
        out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict)
    return out_obj


def _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                    mutually_exclusive_keys, param_dict, *args, **kwargs):
    '''
     this function will create param_dict and con from args and kwargs, param_dict will have only long options for keys,
     it will convert short option to long option key and finally validate parameters
    :param arglist: list of arguments derived from args

    :param keylist: keylist of name of fields
    :param mandatory_options_list:
    :param optional_keylist:
    :param mutually_exclusive_keys:
    :param param_dict: append to param_dict
    :return: connection object
    '''
    arglist = list(args)
    arglist = arglist[::-1]
    con = None
    for key in keylist:
        short_key = long_short_key_map.get(key)
        if (key in list(kwargs.keys())):
            param_dict[key] = kwargs[key]
        elif key in param_dict:
            continue
        elif short_key and (short_key in list(kwargs.keys())):
            param_dict[key] = kwargs[short_key]

        elif len(arglist) >= 1:
            value = arglist.pop()
            if value != None:
                param_dict[key] = value
        elif key not in optional_keylist:
            LOGGER.error(" Invalid Input args %s is not in optional list %s" % (
                key, str(mandatory_options_list)))
            raise ValueError("Invalid Input Arguments")

        if key == 'con':
            if key in param_dict:
                con = param_dict.pop(key)

    # if not con:
    #    raise AttributeError("Invalid command invocation: Connection Object missing.")

    me_key_found = False
    for me_key in list(param_dict.keys()):
        # Checking mandatory option_list presence
        if me_key in list(mandatory_options_list.keys()):
            if not set(mandatory_options_list[me_key]).issubset(set(param_dict.keys())):
                LOGGER.error(" Invalid command invocation %s of mandatory list %s is not in arguments parovided" % (
                    me_key, str(mandatory_options_list)))
                raise AttributeError("Invalid command invocation")

        # Checking mutually exclusive key presense
        if me_key in mutually_exclusive_keys:
            if me_key_found:
                LOGGER.error(" Invalid command invocation %s of mutual exclusive list %s " % (
                    me_key, str(mutually_exclusive_keys)))
                raise AttributeError("Invalid command invocation")
            me_key_found = True

    if not set(keylist + list(long_short_key_map.values())).issuperset(set(kwargs.keys())):
        LOGGER.error(" Invalid Input args: %s unsupported argument passed"
                     % list(set(kwargs.keys()).difference(set(keylist + long_short_key_map.values()))))
        raise ValueError("Invalid Input Arguments")

    return con


def osimages(*args, **kwargs):
    '''
    @summary:
        Use this function to retrieve information about, delete, and import OS images,
         OS-image profiles, device driver, and boot-options files.
        data_dictionary = osimages(input_args, key=values )

        Where KeyList is as follows

            keylist = [con, subcmd, o]

    @param
        subcmd
            list                Retrieve information about all osimages
            globalsettings      Retrieve or modify global operating-system deployment
                                settings. Global settings serve as defaults settings
                                when operating systems are deployed.
            hostsettings        Retrieve information about the network and storage
                                settings for all servers, and create or modify the
                                network and storage settings for one or more servers
            hostplatforms       Retrieve information about the host platforms and
                                deploy operating-system images to the host platforms
                                as a job
            import              Import OS images and scripts from remote server to
                                LXCA
            remotefileservers   Retrieve information about all remote file-server
                                profiles or to create or modify a remote file-server
                                profile
            delete              Delete osimages from LXCA

    @example
        list all osimages info
        osimages(con, subcmd='list')

        delete osimages with ids
        osimages(con, subcmd='delete', id='i1,i2')
        rep = osimages(con_lxca, 'delete', i='20190131054310_trail.py')
        List all globalsettings
        osimages(con, subcmd = 'globalsettings')

        Set Linux default password using globalsettings
        change_linux_password = {
	"activeDirectory": {
		"allDomains": [],
		"defaultDomain": "DEFAULT_DOMAIN"
	},
	"credentials": [{
			"name": "USERNAME",
			"password": "<password>",
			"passwordChanged": True,
			"type": "LINUX"
		}, {
			"type": "WINDOWS",
			"name": "USERNAME",
			"password": None,
			"passwordChanged": False
		}
	],
	"ipAssignment": "dhcpv4",
	"isVLANMode": False,
	"licenseKeys": {
		"win2012r1": {
			"dataCenterLicenseKey": "",
			"standardLicenseKey": "",
		},
		"win2012r2": {
			"dataCenterLicenseKey": "",
			"standardLicenseKey": ""
		},
		"win2016r1": {
			"dataCenterLicenseKey": "",
			"standardLicenseKey": ""
		},
		"win2019r1": {
			"dataCenterLicenseKey": "",
			"standardLicenseKey": ""
		}
	}
}

json_string = json.dumps(change_linux_password)
print json_string

rep = osimages(con_lxca, subcmd = 'globalsettings', osimages_dict = json_string)


    Remote file server list
    rep = osimages(con_lxca, subcmd = 'remotefileservers')

    Create remote file server entry for ftp server

    rep = osimages(con_lxca, subcmd = 'remotefileservers',
			   osimages_dict ='{"username":"guest", "password":"<password>",
			    "protocol":"FTP", "port": 21, "address":"<ipaddress>", "displayName": "new_ftp_207" }')

    Update remote file server
    rep = osimages(con_lxca, subcmd = 'remotefileservers',
                   osimages_dict ='{"putid": "1", "protocol":"FTP", "port": 21,
                    "address":"<ipaddress>", "displayName": "new_ftp_207" }')

    Delete remote file server
    rep = osimages(con_lxca, subcmd = 'remotefileservers', osimages_dict ='{"deleteid": "1"}')


    Import local files of imagetype (UNATTEND, CUSTOM_CONFIG, SCRIPT, OS)
    rep = osimages(con_lxca, subcmd='import', imagetype='UNATTEND')
    print rep
    file_dict = { "jobId":rep["jobId"], "imageName":"SLES", "os":"sles", "description":"SLES_config_file", "file": "/path/to/sles_unattended.xml" }
    rep = osimages(con_lxca, subcmd='import', imagetype='UNATTEND', osimages_dict = json.dumps(file_dict))

    import BUNDLE and BUNDLESIG done with single jobid and imagename should be same as basename of files
    rep = osimages(con_lxca, subcmd='import', imagetype='BUNDLE')
    file_dict = {"jobId":rep["jobId"], "imageName":"bundle_win2016_20180926153236.zip", "file": "/path/to/osimage_test/bundle_win2016_20180926153236.zip"}
    rep1 = osimages(con_lxca, subcmd='import', imagetype='BUNDLE', osimages_dict = json.dumps(file_dict))
    file_dict = { "jobId":rep["jobId"], "imageName":"bundle_win2016_20180926153236.zip.asc", "file": "/path/to/osimage_test/bundle_win2016_20180926153236.zip.asc"}
    rep2 = osimages(con_lxca, subcmd='import', imagetype='BUNDLESIG', osimages_dict = json.dumps(file_dict))

    get all hostSettings
    rep = osimages(con_lxca, 'hostsettings')

    create hostsettings entry
    host_settings_dict = {u'hosts': [{u'storageSettings': {u'targetDevice': u'localdisk'}, u'uuid': u'UUID', u'networkSettings': {u'dns2': u'', u'dns1': u'<dns1ip>', u'hostname': u'nodeundefined', u'vlanId': 0, u'selectedMAC': u'AUTO', u'gateway': u'<gatewayip>', u'subnetMask': u'<subnetmask>', u'mtu': 1500, u'prefixLength': 64, u'ipAddress': u'<ipaddress>'}}, {u'storageSettings': {u'targetDevice': u'localdisk'}, u'uuid': u'UUID2', u'networkSettings': {u'dns2': u'', u'dns1': u'<dns1ip>', u'hostname': u'proton1', u'vlanId': 0, u'selectedMAC': u'AUTO', u'gateway': u'<gatewayip>', u'subnetMask': u'<subnetmask>', u'mtu': 1500, u'prefixLength': 64, u'ipAddress': u'<ipaddress>'}}]}
    host_settings_json = json.dumps(host_settings_dict)
    rep = osimages(con_lxca, 'hostsettings', action='create', osimages_dict = host_settings_json)

    update hostSettings entry
    host_settings_dict = {u'hosts': [{u'storageSettings': {u'targetDevice': u'localdisk'}, u'uuid': u'UUID', u'networkSettings': {u'dns2': u'', u'dns1': u'<dns1ip>', u'hostname': u'nodeundefined', u'vlanId': 0, u'selectedMAC': u'AUTO', u'gateway': u'<gatewayip>', u'subnetMask': u'<subnetmask>', u'mtu': 1500, u'prefixLength': 64, u'ipAddress': u'<ipaddress>'}}, {u'storageSettings': {u'targetDevice': u'localdisk'}, u'uuid': u'UUID2', u'networkSettings': {u'dns2': u'', u'dns1': u'<dns1ip>', u'hostname': u'proton1', u'vlanId': 0, u'selectedMAC': u'AUTO', u'gateway': u'<gatewayip>', u'subnetMask': u'<subnetmask>', u'mtu': 1500, u'prefixLength': 64, u'ipAddress': u'<ipaddress>'}}]}
    host_settings_json = json.dumps(host_settings_dict)
    rep = osimages(con_lxca, 'hostsettings', action='update', osimages_dict = host_settings_json)

    '''

    global SHELL_OBJ
    # #con = None
    # param_dict = {}
    # command_name = sys._getframe().f_code.co_name
    #
    # # con = kwargs.get('con')
    # # if not con:
    # #     raise ValueError("Invalid Input Arguments")
    #
    # logger.info(" osimages got kwargs %s " % str(kwargs))
    # if args:
    #     kwargs['osimages_info'] = args[0]
    # #param_dict = (args, kwargs)
    # logger.info(" osimages got param_dict %s " % str(kwargs))
    # # handle_input_dict only takes param_dict as input argument
    # ch = shell_obj.handle_input_dict(command_name, con, kwargs)
    #  return ch

    con = None
    param_dict = {}
    param_dict = kwargs
    kwargs = {}     # this is required  to avoid invalid argument error in _validate_param
    command_name = sys._getframe().f_code.co_name

    long_short_key_map = {}
    keylist = ['con', 'subcmd']
    optional_keylist = ['con']
    mutually_exclusive_keys = []
    mandatory_options_list = {}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict)
    return out_obj


def managementserver(*args, **kwargs):
    '''

@summary:
    Use this function to get repository info from Lenovo XClarity Administrator
    run this function as

    data_dictionary = managementserver( key1 = 'val1', key2 = 'val2', ...)

    Where KeyList is as follows

        keylist = ['con', 'subcmd', 'key', 'fixids', 'type', 'action', 'files','jobid']

@param
    The parameters for this command are as follows
    subcmd
        query               Retrieve information about all updates in the
                            management-server updates repository
        query_fixids        Retrieve information or the readme or change history
                            file for a specific update in the management-server
                            updates repository
        apply               install a management-server update.
        acquire             Downloads the specified firmware updates from Lenovo
                            XClarity Support website, and stores the updates to
                            the updates repository
        refresh             Retrieves information about the latest available
                            firmware updates from the Lenovo XClarity Support
                            website, and stores the information to the updates
                            repository
        delete              Deletes the specified fixids - removeMetadata not supported
        import              Import files to management server

    key    Returns the specified type of update. This can be one of the following values.
                all. Returns all information. This is the default value.
                currentVersion. Returns the current version of Lenovo XClarity Administrator.
                history. Returns the history of management-server updates.
                importDir. Returns the directory for the management-server updates repository.
                size. Returns the repository size (in bytes).
                updates. Returns information about all updates packages.
                updatedDate. Returns the date when the last update was performed.

     fixids    comma separated fixids
     type      Type for Get with fixids
                changeHistory. Returns the change-history file for the specified management-server update.
                readme. Returns the readme file for the specified management-server update
     jobid     jobid for import
     files     files to be imported with fullpath and comma separated
@example
    TO import files
    rep = managementserver(con_lxca, subcmd='import', files='/path/to/updates/updates/lnvgy_sw_lxca_thinksystemrepo1-1.3.2_anyos_noarch.txt')
    rep = managementserver(con_lxca, subcmd='import', j=rep['jobid'], files='/path/to/updates/updates/lnvgy_sw_lxca_thinksystemrepo1-1.3.2_anyos_noarch.txt')


    '''
    global SHELL_OBJ
    command_name = sys._getframe().f_code.co_name
    param_dict = {}
    con = None

    # some paramters don't have short options
    long_short_key_map = {'key': 'k', 'fixids': 'f',
                          'type': 't', 'jobid': 'j'}

    keylist = ['con', 'subcmd', 'key', 'fixids', 'type', 'files', 'jobid']
    optional_keylist = ['con', 'key', 'fixids',
                        'type', 'files', 'jobid']
    mutually_exclusive_keys = []
    mandatory_options_list = {}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict)

    #remove dummy field added for view
    if 'dummy' in out_obj:
        out_obj.pop('dummy')
    return out_obj


def rules(*args, **kwargs):
    '''

@summary:
    Use this function to get and set complaince rules on Lenovo XClarity Administrator
    run this function as

    data_dictionary = managementserver( key1 = 'val1', key2 = 'val2', ...)

    Where KeyList is as follows

        keylist = ['con', 'id', 'rule']

@param
    The parameters for this command are as follows


@example

    '''
    global SHELL_OBJ
    command_name = sys._getframe().f_code.co_name
    param_dict = {}
    con = None

    # some paramters don't have short options
    long_short_key_map = {'id': 'i', 'rule': 'r'}

    keylist = ['con', 'id', 'rule']
    optional_keylist = ['con', 'id', 'rule']
    mutually_exclusive_keys = ['id', 'rule']
    mandatory_options_list = {}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict, False)
    return out_obj


def compositeResults(*args, **kwargs):
    '''

@summary:
    Use this function to get and set complaince rules on Lenovo XClarity Administrator
    run this function as

    data_dictionary = managementserver( key1 = 'val1', key2 = 'val2', ...)

    Where KeyList is as follows

        keylist = ['con', 'id', ,'query_solutionGroups', 'solutionGroups','targetResources','all_rules']

@param
    The parameters for this command are as follows


@example

    '''
    global SHELL_OBJ
    command_name = sys._getframe().f_code.co_name
    param_dict = {}
    con = None

    # some paramters don't have short options
    long_short_key_map = {'id': 'i', 'query_solutionGroups': 'q',
                          'solutionGroups': 's', 'targetResources': 't', 'all_rules': 'a'}

    keylist = ['con', 'id', 'query_solutionGroups',
               'solutionGroups', 'targetResources', 'all_rules']
    optional_keylist = ['con', 'id', 'query_solutionGroups',
                        'solutionGroups', 'targetResources', 'all_rules']
    mutually_exclusive_keys = ['id', 'query_solutionGroups',
                               'solutionGroups', 'targetResources', 'all_rules']
    mandatory_options_list = {}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict, False)
    return out_obj


def storedcredentials(*args, **kwargs):
    '''

@summary:
    Use this function to get and set complaince rules on Lenovo XClarity Administrator
    run this function as

    data_dictionary = storedcredentials( key1 = 'val1', key2 = 'val2', ...)

    Where KeyList is as follows

        keylist = ['con', 'id', 'user_name', 'description', 'password', 'delete_id']

@param
    The parameters for this command are as follows
    id          Stored credential id of stored credential
    user_name    user name
    password    password
    description description of user credential
    delete_id    id to be deleted

@example
    rep = storedcredentials(con1)
    rep = storedcredentials(con1, id='955')
    rep = storedcredentials(con1,u='admin1', p='admin1', d='description of stored credentials')
    rep = storedcredentials(con1, delete_id='954')
    rep = storedcredentials(con1,i='955', u='admin1', p='admin1', d='description of stored credentials for admin')

    '''
    global SHELL_OBJ
    command_name = sys._getframe().f_code.co_name
    param_dict = {}
    con = None

    # some paramters don't have short options
    long_short_key_map = {'id': 'i', 'user_name': 'u',
                          'description': 'd', 'password': 'p'}

    keylist = ['con', 'id', 'user_name',
               'description', 'password', 'delete_id']
    optional_keylist = ['con', 'id', 'user_name',
                        'description', 'password', 'delete_id']
    mutually_exclusive_keys = ['id', 'delete_id']
    mandatory_options_list = {}

    con = _validate_param(keylist, long_short_key_map, mandatory_options_list, optional_keylist,
                          mutually_exclusive_keys,
                          param_dict, *args, **kwargs)

    out_obj = SHELL_OBJ.handle_input_dict(command_name, con, param_dict)
    return out_obj