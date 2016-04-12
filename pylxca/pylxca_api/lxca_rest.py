'''
@since: 4 Sep 2015
@author: Prashant Bhosale <pbhosale@lenovo.com>, Girish Kumar <gkumar1@lenovo.com>
@license: Lenovo License
@copyright: Copyright 2016, Lenovo
@organization: Lenovo 
@summary: This module is for creating a connection session object for given xHMC 
'''

import logging, os, json, pprint, requests
import logging.config
from requests.exceptions import HTTPError

try:
    logging.captureWarnings(True)
except:
    pass

logger_conf_file = "lxca_logger.conf"
pylxca_logger = os.path.join(os.getenv('PYLXCA_API_PATH'), logger_conf_file)

logger = logging.getLogger(__name__)

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
            resp = session.get(url,verify=False,timeout=3)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error("REST API Exception: Exception = %s", re)
            raise re
        return resp
    
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
            resp = session.get(url, verify=False, timeout=3)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error("REST API Exception: Exception = %s", re)
            raise re
        return resp
        
    def get_switches(self,url, session, uuid):
        url = url + '/switches'
        
        if uuid:
            url = url + '/' + uuid
                    
        try:
            resp = session.get(url, verify=False, timeout=3)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error("REST API Exception: Exception = %s", re)
            raise re
        return resp

    def get_fan(self,url, session, uuid):
        url = url + '/fans'
        
        if uuid:
            url = url + '/' + uuid
                        
        try:
            resp = session.get(url, verify=False, timeout=3)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error("REST API Exception: Exception = %s", re)
            raise re
        return resp

    def get_powersupply(self,url, session, uuid):
        url = url + '/powerSupplies'
        
        if uuid:
            url = url + '/' + uuid
                        
        try:
            resp = session.get(url, verify=False, timeout=3)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error("REST API Exception: Exception = %s", re)
            raise re
        return resp

    def get_fanmux(self,url, session, uuid):
        url = url + '/fanMuxes'
        
        if uuid:
            url = url + '/' + uuid
                        
        try:
            resp = session.get(url, verify=False, timeout=3)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error("REST API Exception: Exception = %s", re)
            raise re
        return resp

    def get_cmm(self,url, session, uuid):
        url = url + '/cmms'
        
        if uuid:
            url = url + '/' + uuid
                        
        try:
            resp = session.get(url, verify=False, timeout=3)
            resp.raise_for_status()
        except HTTPError as re:
            raise re
        return resp

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
            resp = session.get(url, verify=False, timeout=3)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error("REST API Exception: Exception = %s", re)
            raise re
        return resp    
    
    def set_log_config(self):  
        logging.config.fileConfig(pylxca_logger)
        return

    def get_log_level(self):
        logger.debug("Current Log Level is: " + str(logger.getEffectiveLevel()))
        return logger.getEffectiveLevel()
        
    def set_log_level(self,log_value):
        logger.setLevel(log_value)
        return

    def do_discovery(self,url, session, ip_addr,jobid):
        try:
            if ip_addr:
                url = url + '/discoverRequest'
                payload = [{"ipAddresses":ip_addr.split(",")}]
                resp = session.post(url,data = json.dumps(payload),verify=False, timeout=3)
                resp.raise_for_status()
                if resp.status_code == requests.codes['ok']:
                    if resp.headers._store.has_key("location"):
                        job = resp.headers._store["location"][-1].split("/")[-1]
                        return job
                    else:
                        return None
            elif jobid:
                url = url + '/discoverRequest/jobs/' + jobid
                resp = session.get(url,verify=False, timeout=3)
                resp.raise_for_status()
            else:
                url = url + '/discovery'
                resp = session.get(url, verify=False, timeout=3)
                resp.raise_for_status()
                              
        except HTTPError as re:
            logger.error("Exception occured: %s",re)
            raise re
        return resp
