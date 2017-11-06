'''
@since: 21 Oct 2015
@author: Prashant Bhosale <pbhosale@lenovo.com>
@license: Lenovo License
@copyright: Copyright 2016, Lenovo
@organization: Lenovo
@summary: This module implement facade interface for pylxca API interface. It provides a 
single entry point for APIs.   
'''


import logging.config
import json

from pylxca.pylxca_api.lxca_connection import lxca_connection
from pylxca.pylxca_api.lxca_connection import ConnectionError
from  pylxca.pylxca_api.lxca_rest import lxca_rest
from  pylxca.pylxca_api.lxca_rest import HTTPError

logger = logging.getLogger(__name__)

class Singleton(type):
    
    def __call__(cls, *args, **kwargs):#@NoSelf
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super(Singleton, cls).__call__(*args, **kwargs)
            return cls.__instance

def with_metaclass(meta, *bases):
    class metaclass(meta):
        __call__ = type.__call__
        __init__ = type.__init__
        def __new__(cls, name, this_bases, d):
            if this_bases is None:
                return type.__new__(cls, name, (), d)
            return meta(name, bases, d)
    return metaclass('temporary_class', None, {})

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
                          'resourcegroups':self.get_set_resourcegroups
                        }
    
    def api( self, object_name, dict_handler = None, con = None ):
        
 
        try:
            # If Any connection is establibshed
            if con == None and self.con and isinstance(self.con,lxca_connection):
                con = self.con
                
            if object_name  != "connect":
                if con and isinstance(con,lxca_connection): 
                    self.con = con
                else:
                    raise ConnectionError("Invalid Connection Object")

            return self.func_dict[object_name](dict_handler)
        except ConnectionError as re:
            logger.error("Connection Exception: Exception = %s", re)
            if self.con: 
                self.con.disconnect()
                self.con = None
            raise re
        except HTTPError as re:
            logger.error("Exception %s Occurred while calling REST API for object %s" %(re, object_name))
            raise re
        except ValueError as re:
            logger.error("Exception ValueError %s Occurred while calling REST API for object %s" %(re, object_name))
            raise re
        except AttributeError as re:
            logger.error("Exception AttributeError %s Occurred while calling REST API for object %s" %(re, object_name))
            raise re
        except Exception as re:
            logger.error("Exception %s Occurred while calling REST API for object %s" %(re, object_name))
            raise re
        return None
    
    def connect( self, dict_handler = None ):
        url = user = passwd = None
        verify = True
        if dict_handler:
            url = next(item for item in [dict_handler.get('l') , dict_handler.get('url')] if item is not None)
            user = next(item for item in [dict_handler.get('u') , dict_handler.get('user')] if item is not None)
            passwd = next(item for item in [dict_handler.get('p') , dict_handler.get('pw')] if item is not None)
            if "noverify" in dict_handler: verify = False
                 
        self.con = lxca_connection(url,user,passwd,verify)
        
        #clear the temp stored passwd
        passwd = None
        
        if self.con.connect() == True:
            self.con.test_connection()
            logger.debug("Connection to LXCA Success")
            return self.con    
        else:
            logger.error("Connection to LXCA Failed")
            self.con = None
            return self.con
    
    def disconnect( self ):
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")
        self.con.disconnect()
        self.con = None
        return True
    
    def get_log_level(self, dict_handler=None):
        lvl = None
        if dict_handler:
            lvl =  dict_handler['l'] or dict_handler['lvl']
        if lvl == None:
            lvl = lxca_rest().get_log_level()
        else:
            return self.set_log_level(lvl)
        return lvl
    
    def set_log_level(self, log_value):
        try:
            lxca_rest().set_log_level(log_value)
            logger.debug("Current Log Level is now set to " + str(logger.getEffectiveLevel()))
        except Exception as e:
            logger.error("Fail to set Log Level")
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
            status = next((item for item in [dict_handler.get('s') , dict_handler.get('status')] if item is not None),None)
            chassis_uuid = next((item for item in [dict_handler.get('c') , dict_handler.get('chassis')] if item is not None),None)
            
        if chassis_uuid:
            resp = lxca_rest().get_chassis(self.con.get_url(),self.con.get_session(),chassis_uuid,status)
            py_obj = json.loads(resp.text)
            py_obj = {'nodesList':py_obj["nodes"]}
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
            if "ports" in dict_handler: list_port = True

        if chassis_uuid:
            resp = lxca_rest().get_chassis(self.con.get_url(),self.con.get_session(),chassis_uuid,None)
            py_obj = json.loads(resp.text)
            py_obj = {'switchesList':py_obj["switches"]}
        elif list_port and (action==None):
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
            py_obj = {'fanmuxesList':py_obj["fanmuxes"]}
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
            py_obj = json.loads(resp.text)
            return py_obj
        except AttributeError as ValueError:
            return resp

    def do_manage( self, dict_handler = None ):
        ip_addr = None
        user = None
        pw = None
        rpw = None
        mp = None
        jobid = None
        type = None
        uuid = None
        force = None
        
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")
        
        if dict_handler:
            ip_addr = next((item for item in [dict_handler.get  ('i') , dict_handler.get('ip')] if item is not None),None)
            user = next((item for item in [dict_handler.get  ('u') , dict_handler.get('user')] if item is not None),None)
            pw = next((item for item in [dict_handler.get  ('p') , dict_handler.get('pw')] if item is not None),None)
            rpw = next((item for item in [dict_handler.get  ('r') , dict_handler.get('rpw')] if item is not None),None)
            jobid = next((item for item in [dict_handler.get  ('j') , dict_handler.get('job')] if item is not None),None)
            force = next((item for item in [dict_handler.get  ('f') , dict_handler.get('force')] if item is not None),None)
        
        resp = lxca_rest().do_manage(self.con.get_url(),self.con.get_session(),ip_addr,user,pw,rpw,force,jobid)
        
        try:
            py_obj = json.loads(resp.text)
            return py_obj
        except AttributeError as ValueError:
            return resp


    def do_unmanage( self, dict_handler = None ):
        endpoints = None
        force = None
        jobid = None
        
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")
        
        if dict_handler:
            endpoints = next((item for item in [dict_handler.get  ('i') , dict_handler.get('ip')] if item is not None),None)
            force = next((item for item in [dict_handler.get  ('f') , dict_handler.get('force')] if item is not None),False)
            jobid = next((item for item in [dict_handler.get  ('j') , dict_handler.get('job')] if item is not None),None)
            
        resp = lxca_rest().do_unmanage(self.con.get_url(),self.con.get_session(),endpoints,force,jobid)
        
        try:
            py_obj = json.loads(resp.text)
        except AttributeError as ValueError:
            return resp
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

        except AttributeError as ValueError:
            return resp

    def do_configpatterns( self, dict_handler = None ):
        patternid = None
        patternname = None
        includeSettings = None
        endpoint = None
        restart = None
        etype = None
        pattern_update_dict = None

        if not self.con:
            raise ConnectionError("Connection is not Initialized.")

        if dict_handler:
            patternid = next((item for item in [dict_handler.get  ('i') , dict_handler.get('id')] if item is not None),None)
            patternname = next((item for item in [dict_handler.get('n'), dict_handler.get('name')] if item is not None),
                             None)
            includeSettings = next((item for item in [dict_handler.get('includeSettings')] if item is not None),None)
            endpoint = next((item for item in [dict_handler.get  ('e') , dict_handler.get('endpoint')] if item is not None),None)
            restart = next((item for item in [dict_handler.get  ('r') , dict_handler.get('restart')] if item is not None),None)
            etype = next((item for item in [dict_handler.get  ('t') , dict_handler.get('type')] if item is not None),None)
            pattern_update_dict = next((item for item in [dict_handler.get('pattern_update_dict')] if item is not None), None)

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
                raise Exception("Pattern Name %s not found" %patternname)

        resp = lxca_rest().do_configpatterns(self.con.get_url(),self.con.get_session(),patternid, includeSettings, endpoint, restart, etype, pattern_update_dict)

        try:
            # if endpoint:
            #     return resp
            # else:
            py_obj = json.loads(resp.text)
            return py_obj
        
        except AttributeError as ValueError:
            return resp
    
    def get_configprofiles( self, dict_handler = None ):
        profileid = None
        profilename = None
        endpoint = None
        restart = None
        delete = None
        unassign = None
        powerdown = None
        resetimm = None
        force = None

        if not self.con:
            raise ConnectionError("Connection is not Initialized.")

        if dict_handler:
            profileid = next((item for item in [dict_handler.get  ('i') , dict_handler.get('id')] if item is not None),None)
            profilename = next((item for item in [dict_handler.get('n'), dict_handler.get('name')] if item is not None),
                             None)
            endpoint = next(
                (item for item in [dict_handler.get('e'), dict_handler.get('endpoint')] if item is not None), None)
            restart = next((item for item in [dict_handler.get('r'), dict_handler.get('restart')] if item is not None),
                           None)
            delete = next((item for item in [dict_handler.get('d'), dict_handler.get('delete')] if item is not None),
                           None)
            unassign = next((item for item in [dict_handler.get('u'), dict_handler.get('unassign')] if item is not None),
                          None)
            powerdown = next((item for item in [dict_handler.get('p'), dict_handler.get('powerdown')] if item is not None),
                None)
            resetimm = next(
                (item for item in [dict_handler.get('resetimm')] if item is not None),
                None)
            force = next((item for item in [dict_handler.get('f'), dict_handler.get('force')] if item is not None),
                         None)

        if profilename:
            resp = lxca_rest().put_configprofiles(self.con.get_url(), self.con.get_session(), profileid, profilename)
        elif endpoint and restart:
            resp = lxca_rest().post_configprofiles(self.con.get_url(), self.con.get_session(), profileid, endpoint, restart)
        elif profileid and delete and delete.lower() == 'true':
                resp = lxca_rest().delete_configprofiles(self.con.get_url(), self.con.get_session(), profileid)
        elif profileid and unassign and unassign.lower() == 'true':
                resp = lxca_rest().unassign_configprofiles(self.con.get_url(), self.con.get_session(), profileid, powerdown, resetimm, force)
        else:
            resp = lxca_rest().get_configprofiles(self.con.get_url(),self.con.get_session(),profileid)

        try:
            if len(resp.text):
                py_obj = json.loads(resp.text)
                return py_obj
            elif resp.status_code == 204:   # Its success for rename of profile with empty text
                return { 'ID':profileid, 'name':profilename}
        except AttributeError as ValueError:
            return resp
    
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
            if canceljobid or deletejobid:
                return resp
            else:
                py_obj = json.loads(resp.text)
                py_obj = {'jobsList':py_obj}
            return py_obj
        except AttributeError as ValueError:
            return resp



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
        except AttributeError as ValueError:
            return resp
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
        except AttributeError as ValueError:
            return resp
        
    def get_ffdc( self, dict_handler = None ): 
        uuid = None
        
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")
        
        if dict_handler:
            uuid = next((item for item in [dict_handler.get  ('u') , dict_handler.get('uuid')] if item is not None),None)
            
        resp = lxca_rest().get_ffdc(self.con.get_url(),self.con.get_session(),uuid)
        
        try:
            py_obj = json.loads(resp.text)
        except AttributeError as ValueError:
            return resp
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
            resp = lxca_rest().get_updatepolicy(self.con.get_url(), self.con.get_session(), info, jobid)

        try:
            py_obj = json.loads(resp.text)
            if info == "RESULTS":
                py_obj = py_obj["all"]
        except AttributeError as ValueError:
            return resp
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
            action = next((item for item in [dict_handler.get('a'), dict_handler.get('action')] if item is not None), None)
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
        except AttributeError as ValueError:
            return resp
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
            action = next((item for item in [dict_handler.get('a'), dict_handler.get('action')] if item is not None),
                          None)
            fixids = next((item for item in [dict_handler.get('f'), dict_handler.get('fixids')] if item is not None),
                          None)
            type = next((item for item in [dict_handler.get('t'), dict_handler.get('type')] if item is not None), None)
            jobid = next((item for item in [dict_handler.get('j'), dict_handler.get('jobid')] if item is not None), None)
            files = next((item for item in [dict_handler.get('files')] if item is not None),       None)
        if key:
            resp = lxca_rest().get_managementserver(self.con.get_url(), self.con.get_session(), key, fixids, type)
        elif action:
            resp = lxca_rest().set_managementserver(self.con.get_url(), self.con.get_session(), action, files, jobid, fixids)
        else:
            resp = lxca_rest().get_managementserver(self.con.get_url(), self.con.get_session(), key, fixids, type)

        try:
            py_obj = json.loads(resp.text)
        except AttributeError as ValueError:
            return resp
        return py_obj

    def do_updatecomp( self, dict_handler = None ):
        mode = None
        action = None
        server = None
        switch = None
        cmm = None
        storage = None
                
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")
        
        if dict_handler:
            mode = next((item for item in [dict_handler.get  ('m') , dict_handler.get('mode')] if item is not None),None)
            action = next((item for item in [dict_handler.get  ('a') , dict_handler.get('action')] if item is not None),None)
            server = next((item for item in [dict_handler.get  ('s') , dict_handler.get('server')] if item is not None),None)
            storage = next((item for item in [dict_handler.get  ('t') , dict_handler.get('storage')] if item is not None),None)
            switch = next((item for item in [dict_handler.get  ('w') , dict_handler.get('switch')] if item is not None),None)
            cmm = next((item for item in [dict_handler.get  ('c') , dict_handler.get('cmm')] if item is not None),None)
                        
        resp = lxca_rest().do_updatecomp(self.con.get_url(),self.con.get_session(),mode,action,server,switch,storage,cmm)
        
        try:
            if mode == None and action == None and server == None and  switch == None and storage == None and cmm == None :
                py_obj = json.loads(resp.text)
            else:
                py_obj = json.loads(resp._content)
            return py_obj
        except AttributeError as ValueError:
            return resp
        return py_obj

    def get_set_tasks(self, dict_handler=None):
        job_uuid = None
        includeChildren = False
        action = None
        status = None

        if not self.con:
            raise ConnectionError("Connection is not Initialized.")

        if dict_handler:
            job_uuid = next((item for item in [ dict_handler.get('jobUID')] if item is not None), None)
            includeChildren = next((item for item in [ dict_handler.get('children')] if item is not None), "false")
            if includeChildren != "false":
                includeChildren = 'true'
            action = next((item for item in [dict_handler.get('action')] if item is not None), None)
            updateList = next((item for item in [dict_handler.get('updateList')] if item is not None), None)
            #state = next((item for item in [dict_handler.get('state')] if item is not None), None)

        if job_uuid and action in ['cancel', 'delete']:
            resp = lxca_rest().put_tasks(self.con.get_url(), self.con.get_session(), job_uuid, action)
            py_obj = resp.status_code
        elif action in ['update']:
            resp = lxca_rest().put_tasks_update(self.con.get_url(), self.con.get_session(), updateList)
            py_obj = resp.status_code
        elif job_uuid:
            resp = lxca_rest().get_tasks_list(self.con.get_url(), self.con.get_session(), job_uuid, includeChildren)
            py_obj = json.loads(resp.text)
            py_obj = {'TaskList': py_obj[:]}
        else:
            resp = lxca_rest().get_tasks(self.con.get_url(), self.con.get_session())
            py_obj = json.loads(resp.text)
            py_obj = {'TaskList': py_obj[:]}
        return py_obj

    def get_set_manifests( self, dict_handler = None ):
        sol_id = None
        filepath = None
                
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")
        
        if dict_handler:
            sol_id = next((item for item in [dict_handler.get  ('i') , dict_handler.get('id')] if item is not None),None)
            filepath = next((item for item in [dict_handler.get  ('f') , dict_handler.get('file')] if item is not None),None)
                        
        resp = lxca_rest().get_set_manifests(self.con.get_url(),self.con.get_session(),sol_id,filepath)
        
        try:
            py_obj = json.loads(resp._content)
            return py_obj
        except AttributeError as ValueError:
            return resp
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
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")
        # parsing dict_handler to fetch args, kwargs
        osimages_info = ()
        if 'osimages_info' in dict_handler:
            osimages_info = (dict_handler['osimages_info'],)
            dict_handler.pop('osimages_info')
        kwargs = dict_handler

        putmethod_keylist = ['imageType','jobId', 'putid', 'deleteid']
        for key in list(kwargs.keys()):
            if key in putmethod_keylist:
                get_method = False
                break
        # parsing args for putId,postId,deleteId: refer osImages/<id>
        if 'postid' in osimages_info or 'putid' in osimages_info or 'deleteid' in osimages_info:
            get_method = False
        if 'remoteFileServers' in osimages_info and kwargs:
            get_method = False
            if 'id' in kwargs and list(kwargs.keys()).__len__() == 1:
                get_method = True
        if 'hostPlatforms' in osimages_info and kwargs:
            get_method = False
        if 'globalSettings' in osimages_info and kwargs:
            get_method = False
        if 'osdeployment' in osimages_info:
            get_method = False

        if get_method:
            # get methods calls refer above docstring
            resp = lxca_rest().get_osimage(osimages_info, url=self.con.get_url(), session=self.con.get_session(), **kwargs)
        else:
            resp = lxca_rest().set_osimage(osimages_info, url=self.con.get_url(), session=self.con.get_session(), **kwargs)
        try:
            py_obj = json.loads(resp._content)
            return py_obj
        except AttributeError as ValueError:
            return resp
        return py_obj


    def get_set_resourcegroups(self, dict_handler = None):
        '''
    
        '''
        
        uuid = name = desc = type = solutionVPD = members = criteria = None
        
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")

        # parsing dict_handler to fetch parameter    
        if dict_handler:
            uuid = next((item for item in [dict_handler.get('u') , dict_handler.get('uuid')] if item is not None),None)
            name = next((item for item in [dict_handler.get('n') , dict_handler.get('name')] if item is not None),None)
            desc = next((item for item in [dict_handler.get('d') , dict_handler.get('description')] if item is not None),None)
            type = next((item for item in [dict_handler.get('t') , dict_handler.get('type')] if item is not None),None)
            solutionVPD = next((item for item in [dict_handler.get('s') , dict_handler.get('solutionVPD')] if item is not None),None)
            members = next((item for item in [dict_handler.get('m') , dict_handler.get('members')] if item is not None),None)
            criteria = next((item for item in [dict_handler.get('c') , dict_handler.get('criteria')] if item is not None),None)
            
        resp = lxca_rest().get_set_resourcegroups(self.con.get_url(),self.con.get_session(),uuid,name,desc,type,solutionVPD,members,criteria)
        
        try:
            py_obj = json.loads(resp.text)
        except AttributeError as ValueError:
            return resp
        return py_obj
    