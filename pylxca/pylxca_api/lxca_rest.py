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
import ast

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
                if resp.status_code == requests.codes['ok'] or resp.status_code == requests.codes['created'] or resp.status_code == requests.codes['accepted']:
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

    def do_manage(self,url, session, ip_addr,user,pw,rpw,mp,type,jobid):
        try:
            #All input arguments ip_add, user, pw, rpw and mp are mandatory
            if ip_addr and user and pw and mp:
                url = url + '/manageRequest'
                
                payload = list()
                param_dict = dict()
                mp_data_list = list()
                param_dict["ipAddresses"]=ip_addr.split(",")
                param_dict["username"] = user
                param_dict["password"] = pw
                param_dict["type"] = type
                if rpw:param_dict["recoveryPassword"] = rpw
                for each_mp in mp.split(","):
                    mp_data = each_mp.split(";")
                    mp_data_list.append({'protocol': mp_data[0], 'port': long(mp_data[1]), 'enabled': bool(mp_data[2])})
                param_dict["managementPorts"] = mp_data_list                 
                payload = [param_dict]
                
                resp = session.post(url,data = json.dumps(payload),verify=False, timeout=3)
                resp.raise_for_status()
                
                if resp.status_code == requests.codes['ok'] or resp.status_code == requests.codes['created'] or resp.status_code == requests.codes['accepted']:
                    if resp.headers._store.has_key("location"):
                        job = resp.headers._store["location"][-1].split("/")[-1]
                        return job
                    else:
                        return None
            elif jobid:
                url = url + '/manageRequest/jobs/' + jobid
                resp = session.get(url,verify=False, timeout=3)
                resp.raise_for_status()
            else:
                logger.error("Invalid execution of manage REST API")
                raise Exception("Invalid execution of manage REST API")
                              
        except HTTPError as re:
            logger.error("Exception occured: %s",re)
            raise re
        return resp

    def do_unmanage(self,url, session, endpoints,force,jobid):
        
        endpoints_list = list()
        param_dict = dict()
        
        try:
            if endpoints:
                url = url + '/unmanageRequest'
                for each_ep in endpoints.split(","):
                    ip_addr = None
                    each_ep_dict = dict()
                    
                    ep_data = each_ep.split(";")
                    ip_addr = ep_data[0]
                    uuid = ep_data[1]
                    type = ep_data[2]
                    each_ep_dict = {"ipAddresses":ip_addr.split("#"),"type":type,"uuid":uuid}
                    endpoints_list.append(each_ep_dict)
                param_dict["endpoints"] = endpoints_list
                param_dict["forceUnmanage"] = force

                payload = param_dict
                resp = session.post(url,data = json.dumps(payload),verify=False, timeout=3)
                resp.raise_for_status()
                if resp.status_code == requests.codes['ok'] or resp.status_code == requests.codes['created'] or resp.status_code == requests.codes['accepted']:
                    if resp.headers._store.has_key("location"):
                        job = resp.headers._store["location"][-1].split("/")[-1]
                        return job
                    else:
                        return None
            elif jobid:
                url = url + '/unmanageRequest/jobs/' + jobid
                resp = session.get(url,verify=False, timeout=3)
                resp.raise_for_status()
            else:
                logger.error("Invalid execution of unmanage REST API")
                raise Exception("Invalid execution of unmanage REST API")
                              
        except HTTPError as re:
            logger.error("Exception occured: %s",re)
            raise re
        
        return resp

    def get_jobs(self,url, session,jobid,uuid,state,canceljobid,deletejobid):
        url = url + '/jobs'
        try: 
            if jobid:
                url = url + '/' + jobid
                
                if state:
                    if state == "Pending " or state == "Running" \
                    or state == "Complete" or state == "Cancelled" \
                    or state == "Running_With_Errors" or state == "Cancelled_With_Errors" \
                    or state == "Stopped_With_Error" or state == "Interrupted":
                        url = url + '?state=' + state
                        if uuid:
                            url = url + ',uuid=' + uuid
                    else:   
                        raise Exception("Invalid argument 'state': %s" %state)
                if state == None and uuid:
                    url = url + '?uuid=' + uuid   
                    
                resp = session.get(url, verify=False, timeout=3)
                resp.raise_for_status()
            elif canceljobid:
                url = url + '/' + canceljobid
                payload = {"cancelRequest":"true"}
                resp = session.put(url,data = json.dumps(payload),verify=False, timeout=3)
                if resp.status_code == requests.codes['ok'] or resp.status_code == requests.codes['created'] or resp.status_code == requests.codes['accepted']:
                    return True
                resp.raise_for_status()
            elif deletejobid:
                url = url + '/' + deletejobid
                resp = session.delete(url,verify=False, timeout=3)
                if resp.status_code == requests.codes['ok'] or resp.status_code == requests.codes['created'] or resp.status_code == requests.codes['accepted']:
                    return True
                resp.raise_for_status()
            else:
                if state:
                    if state == "Pending " or state == "Running" \
                    or state == "Complete" or state == "Cancelled" \
                    or state == "Running_With_Errors" or state == "Cancelled_With_Errors" \
                    or state == "Stopped_With_Error" or state == "Interrupted":
                        url = url + '?state=' + state
                        if uuid:
                            url = url + ',uuid=' + uuid
                    else:   
                        raise Exception("Invalid argument 'state': %s" %state)
                if state == None and uuid:
                    url = url + '?uuid=' + uuid  
                
                resp = session.get(url, verify=False, timeout=3)
                resp.raise_for_status()
        except HTTPError as re:
            logger.error("REST API Exception: Exception = %s", re)
            raise re
        return resp    
    
    def get_users(self,url, session, userid):
        url = url + '/userAccounts'
        
        if userid:
            url = url + '/' + userid
                        
        try:
            resp = session.get(url, verify=False, timeout=3)
            resp.raise_for_status()
        except HTTPError as re:
            raise re
        return resp
    
    def get_lxcalog(self,url, session, filter):
        url = url + '/events'
        
        if filter:
            url = url + '?filterWith=' + filter
                        
        try:
            resp = session.get(url, verify=False, timeout=3)
            resp.raise_for_status()
        except HTTPError as re:
            raise re
        return resp
    
    def get_ffdc(self,url, session, uuid):
        url = url + '/ffdc/endpoint'
        try:
            if uuid:
                url = url + '/' + uuid
                resp = session.get(url,verify=False, timeout=3)
                resp.raise_for_status()
                if resp.status_code == requests.codes['ok'] or resp.status_code == requests.codes['created'] or resp.status_code == requests.codes['accepted']:
                    job_info = ast.literal_eval(resp.content)    
                    if job_info.has_key("jobURL"):
                        job = job_info["jobURL"].split("/")[-1]
                        return job
                    else:
                        return resp
            else:
                logger.error("Invalid execution of ffdc REST API")
                raise Exception("Invalid execution of ffdc REST API")
                              
        except HTTPError as re:
            logger.error("Exception occured: %s",re)
            raise re