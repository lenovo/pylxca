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
        
class lxca_api ():
    '''
    Facade class which exposes interface for accessing various LXCA APIs
    '''
    __metaclass__ = Singleton
    
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
                          'log':self.get_log_level}
    
    def api( self, object_name, dict_handler = None, con = None ):
        
        if con: self.con = con

        try:
            return self.func_dict[object_name](dict_handler)
        except ConnectionError as re:
            logger.error("Connection Exception: Exception = %s", re)
            if self.con: self.con.disconnect()
            raise re
        except HTTPError as re:
            logger.error("Exception %s Occurred while calling REST API for object %s" %(re, object_name))
            raise re
        except ValueError as re:
            logger.error("Exception ValueError %s Occurred while calling REST API for object %s" %(re, object_name))
        except AttributeError as re:
            logger.error("Exception AttributeError %s Occurred while calling REST API for object %s" %(re, object_name))
        except Exception as re:
            logger.error("Exception %s Occurred while calling REST API for object %s" %(re, object_name))
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
        
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")
        
        if dict_handler:
            uuid = next((item for item in [dict_handler.get('u') , dict_handler.get('uuid')] if item is not None),None)
            chassis_uuid = next((item for item in [dict_handler.get('c') , dict_handler.get('chassis')] if item is not None),None)
            
        if chassis_uuid:
            resp = lxca_rest().get_chassis(self.con.get_url(),self.con.get_session(),chassis_uuid,None)
            py_obj = json.loads(resp.text)
            py_obj = {'switchesList':py_obj["switches"]}
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
            py_obj = {'powersuppliesList':py_obj["powersupplies"]}
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
        status = None
        
        if not self.con:
            raise ConnectionError("Connection is not Initialized.")
        
        if dict_handler:
            complexid = next((item for item in [dict_handler.get('i') , dict_handler.get('id')] if item is not None),None)
            complextype = next((item for item in [dict_handler.get('t') , dict_handler.get('type')] if item is not None),None)
            status = next((item for item in [dict_handler.get('s') , dict_handler.get('status')] if item is not None),None)
            
        resp = lxca_rest().get_scalablesystem(self.con.get_url(),self.con.get_session(),complexid,complextype,status)
        py_obj = json.loads(resp.text)
        return py_obj
