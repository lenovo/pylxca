'''
@since: 21 Oct 2015
@author: Prashant Bhosale <pbhosale@lenovo.com>
@license: Lenovo License
@copyright: Copyright 2016, Lenovo
@organization: Lenovo
@summary: This module implement facade interface for pylxca API interface.
It provides a single entry point for APIs.
'''

import logging.config
import json
from pylxca.pylxca_api.lxca_connection import lxca_connection
from pylxca.pylxca_api.lxca_connection import ConnectionError
from  pylxca.pylxca_api.lxca_rest import lxca_rest
from  pylxca.pylxca_api.lxca_rest import HTTPError

logger = logging.getLogger(__name__)

class Singleton(type):
    """Singleton class"""
    def __call__(cls, *args, **kwargs):#@NoSelf
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super(Singleton, cls).__call__(*args, **kwargs)
            return cls.__instance

def with_metaclass(meta, *bases):
    """with metaclass"""
    class MetaClass(meta):
        """metaclass"""
        __call__ = type.__call__
        __init__ = type.__init__
        def __new__(cls, name, this_bases, argd):
            if this_bases is None:
                return type.__new__(cls, name, (), argd)
            return meta(name, bases, argd)
    return MetaClass('temporary_class', None, {})
# pylint: disable=R0904
# pylint: disable=C0116
# pylint: disable=C0301
# pylint: disable=C0103
class lxca_api(with_metaclass(Singleton, object)):

    '''
    Facade class which exposes interface for accessing various LXCA APIs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.con = None
        self.func_dict = {'connect':self.connect,
                          'disconnect':self.disconnect,
                          'chassis':self.get_chassis,
                          'nodes':self.get_nodes,
                          'switches':self.get_switches,
                          'fans':self.get_fans,
                          'powersupplies':self.get_powersupply,
                          'fanmuxes':self.get_fanmux,
                          'cmms':self.get_cmm,
                          'scalablesystem':self.get_scalablesystem,
                          'log':self.get_log_level,
                          'discover':self.do_discovery,
                          'manage':self.do_manage,
                          'unmanage':self.do_unmanage,
                          'configpatterns':self.do_configpatterns,
                          'configprofiles':self.get_configprofiles,
                          'configtargets':self.get_configtargets,
                          'updatepolicy':self.do_updatepolicy,
                          'updaterepo':self.get_updaterepo,
                          'updatecomp':self.do_updatecomp,
                          'managementserver':self.do_managementserver,
                          'users':self.get_users,
                          'ffdc':self.get_ffdc,
                          'jobs':self.get_jobs,
                          'lxcalog':self.get_lxcalog,
                          'tasks':self.get_set_tasks,
                          'manifests':self.get_set_manifests,
                          'osimages':self.get_set_osimage,
                          'resourcegroups':self.get_set_resourcegroups,
                          'rules': self.get_set_rules,
                          'compositeResults': self.get_set_compositeResults,
                          'storedcredentials': self.get_set_storedcredentials,
                          'license': self.get_license
                        }
    def api( self, object_name, dict_handler = None, con = None ):
        try:
            # If Any connection is establibshed
            if con is None and self.con and isinstance(self.con,lxca_connection):
                con = self.con

            if object_name  == "disconnect":
                dict_handler['orig_con'] = self.con

            if object_name  != "connect":
                if con and isinstance(con,lxca_connection): 
                    self.con = con
                else:
                    raise ConnectionError("Invalid Connection Object")
            return self.func_dict[object_name](dict_handler)
        except ConnectionError as raised_connection_error:
            logger.error("Connection Exception: Exception = %s", raised_connection_error)
            if self.con:
                self.con.disconnect()
                self.con = None
            raise raised_connection_error
        except HTTPError as raised_connection_error:
            logger.error("Exception {%s} Occurred while calling REST API for object {%s}",raised_connection_error , object_name)
            raise raised_connection_error
        except ValueError as raised_connection_error:
            logger.error("Exception ValueError {%s} Occurred while calling REST API for object {%s}", raised_connection_error, object_name)
            raise raised_connection_error
        except AttributeError as raised_connection_error:
            logger.error("Exception AttributeError {%s} Occurred while calling REST API for object {%s}", raised_connection_error, object_name)
            raise raised_connection_error
        except Exception as raised_connection_error:
            logger.error("Exception: {%s}  {%s} Occurred while calling REST API for object {%s}",type(raised_connection_error), str(raised_connection_error), object_name)
            raise raised_connection_error
        return None

    def connect( self, dict_handler = None ):
        url = user = passwd = None
        verify = True
        if dict_handler:
            url = next(item for item in [dict_handler.get('l') , dict_handler.get('url')] if item is not None)
            user = next(item for item in [dict_handler.get('u') , dict_handler.get('user')] if item is not None)
            passwd = next(item for item in [dict_handler.get('p') , dict_handler.get('pw')] if item is not None)
            if "noverify" in dict_handler:
                verify = False
           
        self.con = lxca_connection(url,user,passwd,verify)
  
        #clear the temp stored passwd
        passwd = None
  
        if self.con.connect() is True:
            self.con.test_connection()
            logger.debug("Connection to LXCA Success")
            return self.con
        else:
            logger.error("Connection to LXCA Failed")
            self.con = None
            return self.con

    def disconnect( self, dict_handler=None):
        """
            this method perform disconnect operation
             it also reset current connection to original connection this is used in api version
             to retain origianal connection if we are disconnecting other than current connection

             i.e
             con1 = connect(...)
             con2 = connect(...)
             con3 = connect(...)
             con4 = connect(...)

             disconnect(con2)  will keep current connection to con4
             disconnect(con4) or disconnect() will set current connection to None

        :param dict_handler:  orig_con have original connection before call of disconnect()
        :return:
        """
        resp = False
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")

        reset_conn_to_orig = False
        if dict_handler and ("orig_con" in dict_handler):
            if self.con !=  dict_handler['orig_con']:
                reset_conn_to_orig = True
        try:
            resp = self.con.disconnect()
        except Exception as connectexception:
            logger.error("Exception {%s} Occurred while disconnecting",connectexception)
            if reset_conn_to_orig:
                self.con = dict_handler['orig_con']
            raise
        if reset_conn_to_orig:
            self.con = dict_handler['orig_con']
        else:
            self.con = None
        return resp

    def get_log_level(self, dict_handler=None):
        lvl = None
        if dict_handler:
            lvl = next((item for item in [dict_handler.get('l') , dict_handler.get('lvl')] if item is not None),None)
        if lvl is None:
            lvl = lxca_rest().get_log_level()
        else:
            return self.set_log_level(lvl)
        return lvl

    def set_log_level(self, log_value):
        try:
            lxca_rest().set_log_level(log_value)
            logger.debug("Current Log Level is now set to {%s} ",str(logger.getEffectiveLevel()))
        except Exception as loglevelexception:
            logger.error("Fail to set Log Level{%s}",loglevelexception)
            return False
        return True

    def get_chassis( self, dict_handler = None ):
        uuid = None
        status = None
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")

        if dict_handler:
            uuid = next((item for item in [dict_handler.get('u') , dict_handler.get('uuid')] if item is not None),None)
            status = next((item for item in [dict_handler.get('s') , dict_handler.get('status')] if item is not None),None)
  
        resp = lxca_rest().get_chassis(self.con.get_url(),self.con.get_session(),uuid,status)
        py_obj = json.loads(resp.text)
        return py_obj

    def get_nodes( self, dict_handler = None ):
        uuid = None
        status = None
        chassis_uuid = None
    
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")
  
        if dict_handler:
            uuid = next((item for item in [dict_handler.get('u') , dict_handler.get('uuid')] if item is not None),None)
            modify = next((item for item in [dict_handler.get('m'), dict_handler.get('modify')] if item is not None), None)
            status = next((item for item in [dict_handler.get('s') , dict_handler.get('status')] if item is not None),None)
            chassis_uuid = next((item for item in [dict_handler.get('c') , dict_handler.get('chassis')] if item is not None),None)
            metrics = next((True for item in [dict_handler.get('x', False), dict_handler.get('metrics', False)] if item is None or item is True), False)
      
        if chassis_uuid:
            resp = lxca_rest().get_chassis(self.con.get_url(),self.con.get_session(),chassis_uuid,status)
            py_obj = json.loads(resp.text)
            py_obj = {'nodesList':py_obj["nodes"]}

        if uuid and modify:
            resp = lxca_rest().set_nodes(self.con.get_url(), self.con.get_session(), uuid, modify)
            return resp

        if metrics:
            resp = lxca_rest().get_metrics(self.con.get_url(), self.con.get_session(), uuid)
            py_obj = json.loads(resp.text)
        else:
            resp = lxca_rest().get_nodes(self.con.get_url(),self.con.get_session(),uuid,status)
            py_obj = json.loads(resp.text)
        return py_obj
  
    def get_switches( self, dict_handler = None ):
        uuid = None
        chassis_uuid = None
        port_name = None
        list_port = None
        action = None

        if not self.con:
            raise ConnectionError("Connection is not Initialized.")
  
        if dict_handler:
            uuid = next((item for item in [dict_handler.get('u') , dict_handler.get('uuid')] if item is not None),None)
            chassis_uuid = next((item for item in [dict_handler.get('c') , dict_handler.get('chassis')] if item is not None),None)
            port_name = next((item for item in [dict_handler.get('ports')] if item is not None),None)
            action = next((item for item in [dict_handler.get('action')] if item is not None),
                             None)
            #if "ports" in dict_handler: list_port = True
            if port_name:
                list_port = True

        if chassis_uuid:
            resp = lxca_rest().get_chassis(self.con.get_url(),self.con.get_session(),chassis_uuid,None)
            py_obj = json.loads(resp.text)
            py_obj = {'switchesList':py_obj["switches"]}
        elif list_port and (action is None):
            resp = lxca_rest().get_switches_port(self.con.get_url(), self.con.get_session(), uuid, list_port)
            py_obj = json.loads(resp.text)
        elif port_name and action:
            resp = lxca_rest().put_switches_port(self.con.get_url(), self.con.get_session(), uuid, port_name, action)
            py_obj = json.loads(resp.text)
        else:
            resp = lxca_rest().get_switches(self.con.get_url(),self.con.get_session(),uuid)
            py_obj = json.loads(resp.text)
        return py_obj

    def get_fans( self, dict_handler = None ):
        uuid = None
        chassis_uuid = None
   
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")
  
        if dict_handler:
            uuid = next((item for item in [dict_handler.get('u') , dict_handler.get('uuid')] if item is not None),None)
            chassis_uuid = next((item for item in [dict_handler.get('c') , dict_handler.get('chassis')] if item is not None),None)
      
        if chassis_uuid:
            resp = lxca_rest().get_chassis(self.con.get_url(),self.con.get_session(),chassis_uuid,None)
            py_obj = json.loads(resp.text)
            py_obj = {'fansList':py_obj["fans"]}
        else:
            resp = lxca_rest().get_fan(self.con.get_url(),self.con.get_session(),uuid)
            py_obj = json.loads(resp.text)
        return py_obj

    def get_powersupply( self, dict_handler = None ):
        uuid = None
        chassis_uuid = None
  
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")
  
        if dict_handler:
            uuid = next((item for item in [dict_handler.get('u') , dict_handler.get('uuid')] if item is not None),None)
            chassis_uuid = next((item for item in [dict_handler.get('c') , dict_handler.get('chassis')] if item is not None),None)
     
        if chassis_uuid:
            resp = lxca_rest().get_chassis(self.con.get_url(),self.con.get_session(),chassis_uuid,None)
            py_obj = json.loads(resp.text)
            py_obj = {'powersuppliesList':py_obj["powerSupplies"]}
        else:
            resp = lxca_rest().get_powersupply(self.con.get_url(),self.con.get_session(),uuid)
            py_obj = json.loads(resp.text)
        return py_obj

    def get_fanmux( self, dict_handler = None ):
        uuid = None
        chassis_uuid = None
  
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")
  
        if dict_handler:
            uuid = next((item for item in [dict_handler.get('u') , dict_handler.get('uuid')] if item is not None),None)
            chassis_uuid = next((item for item in [dict_handler.get('c') , dict_handler.get('chassis')] if item is not None),None)
       
        if chassis_uuid:
            resp = lxca_rest().get_chassis(self.con.get_url(),self.con.get_session(),chassis_uuid,None)
            py_obj = json.loads(resp.text)
            py_obj = {'fanmuxesList':py_obj["fanMuxes"]}
        else:
            resp = lxca_rest().get_fanmux(self.con.get_url(),self.con.get_session(),uuid)
            py_obj = json.loads(resp.text)
        return py_obj

    def get_cmm( self, dict_handler = None ):
        uuid = None
        chassis_uuid = None
    
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")
   
        if dict_handler:
            uuid = next((item for item in [dict_handler.get('u') , dict_handler.get('uuid')] if item is not None),None)
            chassis_uuid = next((item for item in [dict_handler.get('c') , dict_handler.get('chassis')] if item is not None),None)
       
        if chassis_uuid:
            resp = lxca_rest().get_chassis(self.con.get_url(),self.con.get_session(),chassis_uuid,None)
            py_obj = json.loads(resp.text)
            py_obj = {'cmmsList':py_obj["cmms"]}
        else:
            resp = lxca_rest().get_cmm(self.con.get_url(),self.con.get_session(),uuid)
            py_obj = json.loads(resp.text)
        return py_obj

    def get_scalablesystem( self, dict_handler = None ):
        complexid = None
        complextype = None

        if not self.con:
            raise ConnectionError("Connection is not Initialized.")
   
        if dict_handler:
            complexid = next((item for item in [dict_handler.get('i') , dict_handler.get('id')] if item is not None),None)
            complextype = next((item for item in [dict_handler.get('t') , dict_handler.get('type')] if item is not None),None)

        resp = lxca_rest().get_scalablesystem(self.con.get_url(),self.con.get_session(),complexid,complextype)
        py_obj = json.loads(resp.text)
        return py_obj

    def do_discovery( self, dict_handler = None ):
        ip_addr = None
        jobid = None
   
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")
   
        if dict_handler:
            ip_addr = next((item for item in [dict_handler.get  ('i') , dict_handler.get('ip')] if item is not None),None)
            jobid = next((item for item in [dict_handler.get  ('j') , dict_handler.get('job')] if item is not None),None)
  
        resp = lxca_rest().do_discovery(self.con.get_url(),self.con.get_session(),ip_addr,jobid)
   
        try:
            py_obj = resp
            return py_obj
        except AttributeError as valueerror:
            raise valueerror

    def do_manage( self, dict_handler = None ):
        ip_addr = None
        user = None
        pw = None
        rpw = None
        jobid = None
        force = None
        storedcredential_id = None
  
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")
  
        if dict_handler:
            ip_addr = next((item for item in [dict_handler.get  ('i') , dict_handler.get('ip')] if item is not None),None)
            user = next((item for item in [dict_handler.get  ('u') , dict_handler.get('user')] if item is not None),None)
            pw = next((item for item in [dict_handler.get  ('p') , dict_handler.get('pw')] if item is not None),None)
            rpw = next((item for item in [dict_handler.get  ('r') , dict_handler.get('rpw')] if item is not None),None)
            jobid = next((item for item in [dict_handler.get  ('j') , dict_handler.get('job')] if item is not None),None)
            storedcredential_id = next((item for item in [dict_handler.get  ('s') ,
                                dict_handler.get('storedcredential_id')] if item is not None),None)
            force = next((item for item in [dict_handler.get  ('f') , dict_handler.get('force')] if item is not None),None)

        resp = lxca_rest().do_manage(self.con.get_url(),self.con.get_session(),ip_addr,user,
                                     pw,rpw,force,jobid, storedcredential_id)
  
        try:
            py_obj = resp
            return py_obj
        except AttributeError as valueerror:
            raise valueerror


    def do_unmanage( self, dict_handler = None ):
        endpoints = None
        force = None
        jobid = None
   
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")
  
        if dict_handler:
            endpoints = next((item for item in [dict_handler.get  ('e') , dict_handler.get('ep')] if item is not None),None)
            force = next((item for item in [dict_handler.get  ('f') , dict_handler.get('force')] if item is not None),False)
            jobid = next((item for item in [dict_handler.get  ('j') , dict_handler.get('job')] if item is not None),None)
      
        resp = lxca_rest().do_unmanage(self.con.get_url(),self.con.get_session(),endpoints,force,jobid)
   
        try:
            py_obj = resp
        except AttributeError as valueerror:
            raise valueerror
        return py_obj
  
    def get_configtargets( self, dict_handler = None ):
        targetid = None

        if not self.con:
            raise ConnectionError("Connection is not Initialized.")

        if dict_handler:
            targetid = next((item for item in [dict_handler.get  ('i') , dict_handler.get('id')] if item is not None),None)

        resp = lxca_rest().get_configtargets(self.con.get_url(),self.con.get_session(),targetid)

        try:
            py_obj = json.loads(resp.text)
            return py_obj

        except AttributeError as valueerror:
            raise valueerror

    def do_configpatterns( self, dict_handler = None ):
        patternid = None
        patternname = None
        includesettings = None
        endpoint = None
        restart = None
        etype = None
        pattern_update_dict = None
        subcmd = None

        if not self.con:
            raise ConnectionError("Connection is not Initialized.")

        try:

            if dict_handler:
                patternid = next((item for item in [dict_handler.get  ('i') , dict_handler.get('id')] if item is not None),None)
                patternname = next((item for item in [dict_handler.get('n'), dict_handler.get('name')] if item is not None),
                                None)
                includesettings = next((item for item in [dict_handler.get('includeSettings')] if item is not None),None)
                endpoint = next((item for item in [dict_handler.get  ('e') , dict_handler.get('endpoint')] if item is not None),None)
                restart = next((item for item in [dict_handler.get  ('r') , dict_handler.get('restart')] if item is not None),None)
                etype = next((item for item in [dict_handler.get  ('t') , dict_handler.get('type')] if item is not None),None)
                pattern_update_dict = next((item for item in [dict_handler.get('pattern_update_dict')] if item is not None), None)
                subcmd = next((item for item in [dict_handler.get('subcmd')] if item is not None), None)
            if patternname and not patternid:
                # get all patterns and get id from name
                resp = lxca_rest().do_configpatterns(self.con.get_url(), self.con.get_session(), None, None,
                                                    None, None, None, None)
                py_obj = json.loads(resp.text)
                for item in py_obj['items']:
                    if item['name'] == patternname:
                        patternid = item['id']
                        break
                if not patternid:
                    raise Exception(f"Pattern Name {patternname} not found")
            if subcmd == 'status':
                resp = lxca_rest().get_configstatus(self.con.get_url(), self.con.get_session(), endpoint)
            else:
                resp = lxca_rest().do_configpatterns(self.con.get_url(),self.con.get_session(),patternid, includesettings, endpoint, restart, etype, pattern_update_dict)

            # if endpoint:
            #     return resp
            # else:
            py_obj = json.loads(resp.text)
            return py_obj

        except HTTPError as errorhttp:
            logger.error(errorhttp)
            if errorhttp.response.status_code == 403:
                return errorhttp.response.json()
            else:
                logger.error("Exception {%s} Occurred while calling REST API",errorhttp)
                raise errorhttp
        except AttributeError as valueerror:
            raise valueerror

    def get_configprofiles( self, dict_handler = None ):
        profileid = None
        profilename = None
        endpoint = None
        restart = None
        subcmd = None
        powerdown = None
        resetimm = None
        resetswitch = None
        force = None

        if not self.con:
            raise ConnectionError("Connection is not Initialized.")

        try:

            if dict_handler:
                profileid = next((item for item in [dict_handler.get  ('i') , dict_handler.get('id')] if item is not None),None)
                profilename = next((item for item in [dict_handler.get('n'), dict_handler.get('name')] if item is not None),
                                None)
                endpoint = next(
                    (item for item in [dict_handler.get('e'), dict_handler.get('endpoint')] if item is not None), None)
                restart = next((item for item in [dict_handler.get('r'), dict_handler.get('restart')] if item is not None),
                            None)
                subcmd = next((item for item in [dict_handler.get('subcmd')] if item is not None),
                            None)
                powerdown = next((item for item in [dict_handler.get('p'), dict_handler.get('powerdown')] if item is not None),
                    None)
                resetimm = next(
                    (item for item in [dict_handler.get('resetimm')] if item is not None),
                    None)
                resetswitch = next(
                    (item for item in [dict_handler.get('resetswitch')] if item is not None),
                    None)

                force = next((item for item in [dict_handler.get('f'), dict_handler.get('force')] if item is not None),
                            None)

            if subcmd == 'rename' and profilename:
                resp = lxca_rest().put_configprofiles(self.con.get_url(), self.con.get_session(), profileid, profilename)
            elif subcmd == 'activate' and endpoint and restart:
                resp = lxca_rest().post_configprofiles(self.con.get_url(), self.con.get_session(), profileid, endpoint, restart)
            elif subcmd == 'delete' and profileid:
                resp = lxca_rest().delete_configprofiles(self.con.get_url(), self.con.get_session(), profileid)
            elif subcmd == 'unassign' and profileid:
                resp = lxca_rest().unassign_configprofiles(self.con.get_url(), self.con.get_session(), profileid, powerdown, resetimm, resetswitch, force)
                if len(resp.text):
                    py_obj = json.loads(resp.text)
                    py_obj['dummy'] = {'status': []}
                    return py_obj

            elif subcmd == 'list':
                resp = lxca_rest().get_configprofiles(self.con.get_url(),self.con.get_session(),profileid)

            if len(resp.text):
                py_obj = json.loads(resp.text)
                return py_obj
            elif resp.status_code == 204:   # Its success for rename of profile with empty text
                return { 'ID':profileid, 'name':profilename}

        except HTTPError as errorhttp:
            logger.error(errorhttp)
            if errorhttp.response.status_code == 403:
                return errorhttp.response.json()
            else:
                logger.error("Exception %s Occurred while calling REST API",errorhttp)
                raise errorhttp

        except AttributeError as valueerror:
            raise valueerror
    
    def get_jobs( self, dict_handler = None ):
        jobid = None
        uuid = None
        state = None
        canceljobid = None
        deletejobid = None
        
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")
        
        if dict_handler:
            jobid = next((item for item in [dict_handler.get  ('i') , dict_handler.get('id')] if item is not None),None)
            uuid = next((item for item in [dict_handler.get  ('u') , dict_handler.get('uuid')] if item is not None),False)
            state = next((item for item in [dict_handler.get  ('s') , dict_handler.get('state')] if item is not None),None)
            canceljobid = next((item for item in [dict_handler.get  ('c') , dict_handler.get('cancel')] if item is not None),None)
            deletejobid = next((item for item in [dict_handler.get  ('d') , dict_handler.get('delete')] if item is not None),None)
            
        resp = lxca_rest().get_jobs(self.con.get_url(),self.con.get_session(),jobid,uuid,state,canceljobid,deletejobid)
        
        try:
            if jobid:
                py_obj = json.loads(resp.text)
                py_obj = {'jobsList': [py_obj]}
                return py_obj
            if canceljobid or deletejobid:
                return resp
            else:
                py_obj = json.loads(resp.text)
                py_obj = {'jobsList':py_obj}
            return py_obj
        except AttributeError as valueerror:
            raise valueerror



    def get_users( self, dict_handler = None ):
        userid = None
        
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")
        
        if dict_handler:
            userid = next((item for item in [dict_handler.get  ('i') , dict_handler.get('id')] if item is not None),None)
            
        resp = lxca_rest().get_users(self.con.get_url(),self.con.get_session(),userid)
        
        try:
                   
            if userid:
                py_obj = json.loads(resp.text)['response']
            else:
                py_obj = json.loads(resp.text)
                py_obj = {'usersList':py_obj['response']}
        except AttributeError as valueerror:
            raise valueerror
        return py_obj
    
    def get_lxcalog( self, dict_handler = None ):
        filter = None
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")
        
        if dict_handler:
            filter = next((item for item in [dict_handler.get  ('f') , dict_handler.get('filter')] if item is not None),None)
            
        resp = lxca_rest().get_lxcalog(self.con.get_url(),self.con.get_session(),filter)
        
        try:
            py_obj = json.loads(resp.text)
            py_obj = {'eventList':py_obj}
            return py_obj
        except AttributeError as valueerror:
            raise valueerror
        
    def get_ffdc( self, dict_handler = None ): 
        uuid = None
        
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")
        
        if dict_handler:
            uuid = next((item for item in [dict_handler.get  ('u') , dict_handler.get('uuid')] if item is not None),None)
            
        resp = lxca_rest().get_ffdc(self.con.get_url(),self.con.get_session(),uuid)
        
        try:
            py_obj = resp
        except AttributeError as valueerror:
            raise valueerror
        return py_obj
    
    
    def do_updatepolicy( self, dict_handler = None ):
        info = None
        policy = None
        jobid= None

        if not self.con:
            raise ConnectionError("Connection is not Initialized.")

        if dict_handler:
            policy = next((item for item in [dict_handler.get('p'), dict_handler.get('policy')] if item is not None),
                          None)
            info = next((item for item in [dict_handler.get('i'), dict_handler.get('info')] if item is not None), None)
            uuid = next((item for item in [dict_handler.get('u'), dict_handler.get('uuid')] if item is not None), None)
            jobid = next((item for item in [dict_handler.get('j'), dict_handler.get('jobid')] if item is not None),
                         None)
            type = next((item for item in [dict_handler.get('t'), dict_handler.get('type')] if item is not None),
                         None)

        if policy:
            resp = lxca_rest().post_updatepolicy(self.con.get_url(), self.con.get_session(), policy, type, uuid)
        else:
            resp = lxca_rest().get_updatepolicy(self.con.get_url(), self.con.get_session(), info, jobid, uuid)

        try:
            py_obj = json.loads(resp.text)
            if info == "RESULTS":
                py_obj = py_obj["all"]
        except AttributeError as valueerror:
            raise valueerror
        return py_obj

    def get_updaterepo( self, dict_handler = None ):
        key = None
        action = None
        mt = None
        scope = None
        fixids = None
        type = None
        
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")
        
        if dict_handler:
            key = next((item for item in [dict_handler.get('k'), dict_handler.get('key')] if item is not None), None)
            action = next((item for item in [dict_handler.get('subcmd')] if item is not None), None)
            mt = next((item for item in [dict_handler.get('m'), dict_handler.get('mt')] if item is not None), None)
            scope = next((item for item in [dict_handler.get('s'), dict_handler.get('scope')] if item is not None), None)
            fixids = next((item for item in [dict_handler.get('f'), dict_handler.get('fixids')] if item is not None), None)
            type = next((item for item in [dict_handler.get('t'), dict_handler.get('type')] if item is not None), None)

        if key:
            resp = lxca_rest().get_updaterepo(self.con.get_url(),self.con.get_session(), key, mt, scope)
        elif action:
            resp = lxca_rest().put_updaterepo(self.con.get_url(), self.con.get_session(), action, fixids, mt, type, scope)
        else:
            raise Exception("Invalid argument")

        try:
            py_obj = json.loads(resp.text)
        except AttributeError as valueerror:
            raise valueerror
        return py_obj



    def do_managementserver(self, dict_handler=None):
        key = None
        action = None
        fixids = None
        type = None
        jobid = None
        files = None

        if not self.con:
            raise ConnectionError("Connection is not Initialized.")

        if dict_handler:
            key = next((item for item in [dict_handler.get('k'), dict_handler.get('key')] if item is not None), None)
            action = next((item for item in [dict_handler.get('subcmd')] if item is not None),
                          None)
            fixids = next((item for item in [dict_handler.get('f'), dict_handler.get('fixids')] if item is not None),
                          None)
            type = next((item for item in [dict_handler.get('t'), dict_handler.get('type')] if item is not None), None)
            jobid = next((item for item in [dict_handler.get('j'), dict_handler.get('jobid')] if item is not None), None)
            files = next((item for item in [dict_handler.get('files')] if item is not None),       None)
        if key or type:
            resp = lxca_rest().get_managementserver(self.con.get_url(), self.con.get_session(), key, fixids, type)
        elif action:
            resp = lxca_rest().set_managementserver(self.con.get_url(), self.con.get_session(), action, files, jobid, fixids)

        try:
            py_obj = json.loads(resp.text)
        except AttributeError as valueerror:
            raise valueerror
        py_obj['dummy']={'status':[]}
        return py_obj

    def do_updatecomp( self, dict_handler = None ):
        mode = None
        action = None
        server = None
        switch = None
        cmm = None
        storage = None
        query = None
        dev_list = None
                
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")
        
        if dict_handler:
            mode = next((item for item in [dict_handler.get  ('m') , dict_handler.get('mode')] if item is not None),None)
            action = next((item for item in [dict_handler.get  ('a') , dict_handler.get('action')] if item is not None),None)
            server = next((item for item in [dict_handler.get  ('s') , dict_handler.get('server')] if item is not None),None)
            storage = next((item for item in [dict_handler.get  ('t') , dict_handler.get('storage')] if item is not None),None)
            switch = next((item for item in [dict_handler.get  ('w') , dict_handler.get('switch')] if item is not None),None)
            cmm = next((item for item in [dict_handler.get  ('c') , dict_handler.get('cmm')] if item is not None),None)
            query = next((item for item in [dict_handler.get('q'), dict_handler.get('query')] if item is not None), None)
            dev_list = next((item for item in [dict_handler.get('l'), dict_handler.get('dev_list')] if item is not None), None)

        resp = lxca_rest().do_updatecomp(self.con.get_url(),self.con.get_session(), query, mode,action,server,switch,storage,cmm, dev_list)
        
        try:
            if mode is None and action is None and server is None and  switch is None and storage is None and cmm is None and dev_list is None :
                py_obj = json.loads(resp.text)
            else:
                py_obj = resp.json()
            return py_obj
        except AttributeError as valueerror:
            raise valueerror
        return py_obj

    def get_set_tasks(self, dict_handler=None):
        job_uuid = None
        includechildren = False
        action = None
        #status = None
        #cmdupdatelist = None
        template = None

        if not self.con:
            raise ConnectionError("Connection is not Initialized.")

        if dict_handler:
            job_uuid = next((item for item in [ dict_handler.get('jobUID')] if item is not None), None)
            includechildren = next((item for item in [ dict_handler.get('children')] if item is not None), "true")
            action = next((item for item in [dict_handler.get('action')] if item is not None), None)
            updatelist = next((item for item in [dict_handler.get('updateList')] if item is not None), None)
            template = next((item for item in [dict_handler.get('template')] if item is not None), None)
            #if updatelist:
            #    updatelist = updatelist['taskList']


        if job_uuid and action in ['cancel']:
            resp = lxca_rest().put_tasks(self.con.get_url(), self.con.get_session(), job_uuid, action)
            py_obj = resp.status_code
        elif action in ['delete']:
            resp = lxca_rest().delete_tasks(self.con.get_url(), self.con.get_session(), job_uuid)
            py_obj = resp.status_code
        elif action in ['update']:
            resp = lxca_rest().put_tasks_update(self.con.get_url(), self.con.get_session(), updatelist)
            py_obj = resp.status_code
        elif action in ['create']:
            resp = lxca_rest().post_tasks(self.con.get_url(), self.con.get_session(), template)
            py_obj = resp
        else:
            resp = lxca_rest().get_tasks(self.con.get_url(), self.con.get_session(), job_uuid, includechildren)
            py_obj = json.loads(resp.text)
            py_obj = {'TaskList': py_obj[:]}
        return py_obj

    def get_set_manifests( self, dict_handler = None ):
        sol_id = None
        filepath = None
                
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")
        
        if dict_handler:
            sol_id = next((item for item in [dict_handler.get('i') , dict_handler.get('id')] if item is not None),None)
            filepath = next((item for item in [dict_handler.get('f') , dict_handler.get('file')] if item is not None),None)
        resp = lxca_rest().get_set_manifests(self.con.get_url(),self.con.get_session(),sol_id,filepath)
        try:
            py_obj = resp.json()
            return py_obj
        except AttributeError as valueerror:
            raise valueerror
        return py_obj



    def get_set_osimage(self, dict_handler = None):
        '''
        Reference URL: http://10.240.61.40:8131/help/topic/com.lenovo.lxca_restapis_all.doc/rest_apis_os_deployment_resources.html?cp=0_4_5
        commands construction:
        - osimages() 									<< GET  command   ::DONE
        - osimages(imageType=<DUD,BOOT,OS,OSPROFILE>)  	<< POST command   ::DONE
        - osimages(fileName=<>) 						<< GET  command   ::DONE
        - osimages(id=<>)								<< GET  command   ::DONE
        - osimages(id=<>, **kwargs)     				<< PUT/POST/DELETE command  :: DONE [TODO: its a complex post args]
        - osimages(jobid = <>)							<< POST command    ::DONE

        - osimages(remoteFileServers)					<< GET  command    ::DONE
        - osimages(remoteFileServers, **kwargs)			<< POST command    ::DONE
        - osimages(remoteFileServers, getId=<>)			<< GET  command    ::DONE
        - osimages(remoteFileServers, putId/deleteId=<>, **kwargs)	<< PUT/DELETE command  DONE

        - osimages(hostplatforms)						<< GET  command    ::DONE
        - osimages(hostplatforms, **kwargs)				<< PUT  command    ::DONE [TODO: jsonify complex args]

        - osimages(osdeployment)						<< PUT  command   :: DONE
        - osimages(osdeployment, **kwargs)				<< POST command   :: DONE [TODO: jsonify complex args]
        - osimages(connection)                          << GET  command   :: DONE
        - osimages(globalSettings)                      << GET  command   :: DONE
        - osimages(globalSettings, **kwargs)            << PUT  command   :: DONE

        '''
        get_method  = True
        id = None
        action = None
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")

        try:
            if dict_handler:
                osimages_info = next((item for item in [dict_handler.get('subcmd')] if item is not None), None)
                imagetype = next((item for item in [dict_handler.get('t'), dict_handler.get('imagetype')] if item is not None), None)
                id = next((item for item in [dict_handler.get('i'), dict_handler.get('id')] if item is not None), None)
                action = next((item for item in [dict_handler.get('a'), dict_handler.get('action')] if item is not None), None)

                kwargs = next((item for item in [dict_handler.get('o'),
                                                dict_handler.get('osimages_dict')] if item is not None), None)

            if 'list' in osimages_info:
                resp = lxca_rest().list_osimage(self.con.get_url(), self.con.get_session())
            elif 'globalsettings' in osimages_info :
                resp = lxca_rest().osimage_globalsettings(self.con.get_url(), self.con.get_session(), kwargs)
            elif 'hostsettings' in osimages_info :
                if action:
                    if action in ['update']:
                        if not 'hosts' in kwargs:
                            raise Exception("Invalid argument: hosts detail is missing")
                        resp = lxca_rest().update_osimage_hostsettings(self.con.get_url(), self.con.get_session(), kwargs['hosts'])
                    elif action in ['create']:
                        if not 'hosts' in kwargs:
                            raise Exception("Invalid argument: hosts detail is missing")
                        resp = lxca_rest().create_osimage_hostsettings(self.con.get_url(), self.con.get_session(), kwargs['hosts'])
                    elif action in ['delete']:
                        resp = lxca_rest().delete_osimage_hostsettings(self.con.get_url(), self.con.get_session(), kwargs)
                else:
                    resp = lxca_rest().list_osimage_hostsettings(self.con.get_url(), self.con.get_session(), kwargs)
            elif 'hostplatforms' in osimages_info :
                resp = lxca_rest().osimage_hostplatforms(self.con.get_url(), self.con.get_session(), kwargs)
            elif 'import' in osimages_info:
                if not kwargs:
                    kwargs = {}
                kwargs['imageType'] = imagetype
                resp = lxca_rest().osimage_import(self.con.get_url(), self.con.get_session(), kwargs)
            elif 'remotefileservers' in osimages_info:
                if not kwargs:
                    kwargs = {}
                resp = lxca_rest().osimage_remotefileservers(self.con.get_url(), self.con.get_session(), kwargs)

            elif 'delete' in osimages_info:
                if not kwargs:
                    kwargs = {}
                kwargs['id'] = id
                resp = lxca_rest().osimage_delete(self.con.get_url(), self.con.get_session(), kwargs)

            py_obj = resp.json()
            return py_obj

        except HTTPError as errorhttp:
            logger.error(errorhttp)
            if errorhttp.response.status_code == 403:
                return errorhttp.response.json()
            else:
                logger.error("Exception {%s} Occurred while calling REST API",errorhttp)
                raise errorhttp

        except ValueError as err:
            logger.error("Exception: Non json response: {%s}",err)
            raise err
        except AttributeError as err:
            raise err
        return py_obj

    def get_set_resourcegroups(self, dict_handler = None):
        '''get_set_resourcegroups
    
        '''
        
        subcmd=uuid = name = desc = type = solutionvpd = members = criteria = None
        
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")

        # parsing dict_handler to fetch parameter    
        if dict_handler:
            uuid = next((item for item in [dict_handler.get('u') , dict_handler.get('uuid')] if item is not None),None)
            name = next((item for item in [dict_handler.get('n') , dict_handler.get('name')] if item is not None),None)
            desc = next((item for item in [dict_handler.get('d') , dict_handler.get('description')] if item is not None),None)
            type = next((item for item in [dict_handler.get('t') , dict_handler.get('type')] if item is not None),None)
            solutionvpd = next((item for item in [dict_handler.get('s') , dict_handler.get('solutionVPD')] if item is not None),None)
            members = next((item for item in [dict_handler.get('m') , dict_handler.get('members')] if item is not None),None)
            criteria = next((item for item in [dict_handler.get('c') , dict_handler.get('criteria')] if item is not None),None)
            subcmd = next(
                (item for item in [dict_handler.get('subcmd')] if item is not None), None)

        if 'list' in subcmd:
            resp = lxca_rest().list_resourcegroups(self.con.get_url(), self.con.get_session(), uuid)
        elif 'criteriaproperties' in subcmd:
            resp = lxca_rest().criteriaproperties_resourcegroups(self.con.get_url(), self.con.get_session())
            py_obj = json.loads(resp.text)
            py_obj = {'propertiesList': py_obj}
            return py_obj
        elif 'delete' in subcmd:
            resp = lxca_rest().delete_resourcegroups(self.con.get_url(), self.con.get_session(), uuid)
            if resp.status_code == 200:
                return "Deleted Successfully"
        elif 'create' in subcmd:
            if 'dynamic' in type:
                resp = lxca_rest().dynamic_resourcegroups(self.con.get_url(), self.con.get_session(), uuid, name, desc,
                                                  type, criteria)
            elif 'solution' in type:
                resp = lxca_rest().solution_resourcegroups(self.con.get_url(), self.con.get_session(), uuid, name,
                                                           desc, type, solutionvpd, members, criteria)
            else:
                raise Exception("Invalid argument: Type supported are dynamic and solution")
        elif 'update' in subcmd:
            if 'dynamic' in type:
                resp = lxca_rest().dynamic_resourcegroups(self.con.get_url(), self.con.get_session(), uuid, name,
                                                          desc,
                                                          type, criteria)
            elif 'solution' in type:
                resp = lxca_rest().solution_resourcegroups(self.con.get_url(), self.con.get_session(), uuid, name,
                                                           desc, type, solutionvpd, members, criteria)
            else:
                raise Exception("Invalid argument: Type supported are dynamic and solution")

        try:
            py_obj = json.loads(resp.text)
        except AttributeError as valueerror:
            raise valueerror
        return py_obj

    def get_set_rules(self, dict_handler=None):
        id = None
        rule = None

        if not self.con:
            raise ConnectionError("Connection is not Initialized.")

        if dict_handler:
            id = next((item for item in [dict_handler.get('i'), dict_handler.get('id')] if item is not None),
                        None)
            rule = next((item for item in [dict_handler.get('r'), dict_handler.get('rule')] if item is not None),
                             None)

        if rule:
            resp = lxca_rest().set_rules(self.con.get_url(), self.con.get_session(), rule)
        else:
            resp = lxca_rest().get_rules(self.con.get_url(), self.con.get_session(), id)
        py_obj = json.loads(resp.text)
        return py_obj

    def get_set_compositeResults(self, dict_handler=None):
        id = None
        query_solutiongroups = None
        solutiongroups = None
        targetresources = None
        all_rules = None

        if not self.con:
            raise ConnectionError("Connection is not Initialized.")

        if dict_handler:
            id = next((item for item in [dict_handler.get('i'), dict_handler.get('id')] if item is not None),
                        None)
            query_solutiongroups = next((item for item in
                [dict_handler.get('q'), dict_handler.get('query_solutionGroups')] if item is not None),
                      None)
            solutiongroups = next((item for item in [dict_handler.get('s'),
                dict_handler.get('solutionGroups')] if item is not None),
                             None)
            targetresources = next(
                (item for item in [dict_handler.get('t'), dict_handler.get('targetResources')] if item is not None),
                None)
            all_rules = next(
                (item for item in [dict_handler.get('a'), dict_handler.get('all_rules')] if item is not None),
                None)

        if all_rules or solutiongroups or targetresources:
            resp = lxca_rest().set_compositeResults(self.con.get_url(),
                    self.con.get_session(), solutiongroups, targetresources, all_rules)
        else:
            resp = lxca_rest().get_compositeResults(self.con.get_url(),
                    self.con.get_session(), id, query_solutiongroups)
        py_obj = json.loads(resp.text)
        return py_obj


    def get_set_storedcredentials(self, dict_handler=None):
        """
        Stored credential api handler
        :param dict_handler:
        :return:
        """
        id = None
        user_name = None
        description = None
        password = None
        delete_id = None

        if not self.con:
            raise ConnectionError("Connection is not Initialized.")

        if dict_handler:
            id = next((item for item in [dict_handler.get('i'), dict_handler.get('id')] if item is not None),
                        None)
            user_name = next((item for item in [dict_handler.get('u'), dict_handler.get('user_name')] if item is not None),
                             None)
            description = next((item for item in [dict_handler.get('d'), dict_handler.get('description')] if item is not None),
                             None)
            password = next(
                (item for item in [dict_handler.get('p'), dict_handler.get('password')] if item is not None),
                None)
            delete_id = next(
                (item for item in [dict_handler.get('delete_id')] if item is not None),
                None)

        if delete_id:
            resp = lxca_rest().delete_storedcredentials(self.con.get_url(), self.con.get_session(), delete_id)
            resp = json.loads(resp.text)
        elif id and (user_name or password or description):
            resp = lxca_rest().put_storedcredentials(self.con.get_url(), self.con.get_session(), id, user_name, password, description)
            resp = json.loads(resp.text)
        elif user_name and password:
            resp = lxca_rest().post_storedcredentials(self.con.get_url(), self.con.get_session(), user_name, password, description)
            py_obj = json.loads(resp.text)
            resp = {'storedcredentialsList': [py_obj['response']]}
        else:
            resp = lxca_rest().get_storedcredentials(self.con.get_url(), self.con.get_session(), id)
            py_obj = json.loads(resp.text)
            resp = {'storedcredentialsList': py_obj['response']}
        return resp

    def get_license(self, dict_handler=None):
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")
        
        resp = lxca_rest().get_license(self.con.get_url(),self.con.get_session())
        py_obj = resp.json()
        return py_obj
