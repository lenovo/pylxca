'''
Created on 4 Sep 2015

@author: Author: Prashant Bhosale <pbhosale@lenovo.com>

This module is for creating a connection session object for given xHMC 
'''

import logging, os
import logging.config
from requests.exceptions import HTTPError

try:
    logging.captureWarnings(True)
except:
    pass

logger = logging.getLogger(__name__)
logger_conf_file = "lxca_logger.conf"
pylxca_logger = os.path.join(os.getenv('PYLXCA_API_PATH'), logger_conf_file)

class lxca_rest:
    '''
    classdocs
    '''
    def get_chassis(self,url, session, uuid, status ):
        url = url + '/chassis'
        
        if uuid:
            url = url + "/" + uuid
            
        if status:
            if status == "managed" or status == "unmanaged":
                url = url + "?status=" + status
            else:
                raise Exception("Invalid argument 'status'")
        else:
            url = url + "?status=managed" 
            
        try:
            r = session.get(url,verify=False,timeout=3)
            r.raise_for_status()
        except HTTPError as re:
            raise re
        return r
    
    def get_nodes(self,url, session, uuid, status):
        url = url + '/nodes'
        
        if uuid:
            url = url + '/' + uuid
        
        if status:
            if status == "managed" or status == "unmanaged":
                url = url + "?status=" + status
            else:
                raise Exception("Invalid argument 'status'")
            
        try:
            r = session.get(url, verify=False, timeout=3)
            r.raise_for_status()
        except HTTPError as re:
            raise re
        return r
        
    def get_switches(self,url, session, uuid):
        url = url + '/switches'
        
        if uuid:
            url = url + '/' + uuid
                    
        try:
            r = session.get(url, verify=False, timeout=3)
            r.raise_for_status()
        except HTTPError as re:
            raise re
        return r

    def get_fan(self,url, session, uuid):
        url = url + '/fans'
        
        if uuid:
            url = url + '/' + uuid
                        
        try:
            r = session.get(url, verify=False, timeout=3)
            r.raise_for_status()
        except HTTPError as re:
            raise re
        return r

    def get_powersupply(self,url, session, uuid):
        url = url + '/powerSupplies'
        
        if uuid:
            url = url + '/' + uuid
                        
        try:
            r = session.get(url, verify=False, timeout=3)
            r.raise_for_status()
        except HTTPError as re:
            raise re
        return r

    def get_fanmux(self,url, session, uuid):
        url = url + '/fanMuxes'
        
        if uuid:
            url = url + '/' + uuid
                        
        try:
            r = session.get(url, verify=False, timeout=3)
            r.raise_for_status()
        except HTTPError as re:
            raise re
        return r

    def get_cmm(self,url, session, uuid):
        url = url + '/cmms'
        
        if uuid:
            url = url + '/' + uuid
                        
        try:
            r = session.get(url, verify=False, timeout=3)
            r.raise_for_status()
        except HTTPError as re:
            raise re
        return r

    def get_scalablesystem(self,url, session, complexid,complextype,status):
        url = url + '/scalableComplex'
        
        if complexid:
            url = url + '/' + complexid
            
        if complextype:
            if complextype == "flex" or complextype == "rackserver":
                url = url + "?complexType=" + complextype
            else:
                raise Exception("Invalid argument 'complexType': %s" %complextype) 
        elif status:
            if status == "managed" or status == "unmanaged":
                url = url + "?status=" + status
            else:
                raise Exception("Invalid argument 'status'")
                        
        try:
            r = session.get(url, verify=False, timeout=3)
            r.raise_for_status()
        except HTTPError as re:
            raise re
        return r    
    
    def set_log_config(self):        
        logging.config.fileConfig(pylxca_logger, disable_existing_loggers=False)
        return

    def get_log_level(self):
        logger.debug("Current Log Level is: " + str(logger.getEffectiveLevel()))
        return logger.getEffectiveLevel()
        
    def set_log_level(self,log_value):
        logger.setLevel(log_value)
        return
