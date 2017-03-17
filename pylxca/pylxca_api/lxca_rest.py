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
import ast, json, re
import socket
import time

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
                url = url + '/discoverRequest/jobs/' + str(jobid)
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

    def do_manage(self,url, session, ip_addr,user,pw,rpw,mp,type,uuid,force,jobid):
        try:
            #All input arguments ip_add, user, pw, rpw and mp are mandatory
            # if ip_addr and user and pw and mp:
            if ip_addr and user and pw:
                url = url + '/manageRequest'

                payload = list()
                param_dict = dict()

                param_dict["ipAddresses"]=ip_addr.split(",")
                param_dict["username"] = user
                param_dict["password"] = pw
                if rpw:param_dict["recoveryPassword"] = rpw

                # do auto discovery
                disc_job_id = self.do_discovery(url.rsplit('/',1)[0], session, ip_addr,None)
                disc_progress = 0
                
                if disc_job_id:
                    while disc_progress < 100:
                        time.sleep(2) # delays for 5 seconds to allow discovery to complete
                        disc_job_resp = self.do_discovery(url.rsplit('/',1)[0], session, None,disc_job_id)
                        disc_resp_py_obj = json.loads(disc_job_resp.text)
                        disc_progress = disc_resp_py_obj['progress']
                 
                for key in disc_resp_py_obj.keys():
                    if isinstance(disc_resp_py_obj[key],list) and disc_resp_py_obj[key] != []: 
                        #Fetch Management Port value from Response
                        param_dict["managementPorts"] = disc_resp_py_obj[key][0]["managementPorts"]
                        #Fetch Type value from Response
                        param_dict["type"] = disc_resp_py_obj[key][0]["type"]
                        #Fetch UUID value from  Response
                        param_dict["uuid"] = disc_resp_py_obj[key][0]["uuid"]
                        
                        disc_ip_addr = disc_resp_py_obj[key][0]["ipAddresses"][0]
                        
                        param_dict["ipAddresses"] = [disc_ip_addr]
                        
                        if param_dict["type"] == "Rackswitch":
                            param_dict["os"] = disc_resp_py_obj[key][0]["os"]
                
                logger.debug("ip_addr = %s" %param_dict["ipAddresses"])
                
                if force == True:
                    param_dict["forceManage"] = True
                
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
                url = url + '/manageRequest/jobs/' + str(jobid)
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
                    #Fetch type value from input
                    type_list = ["Chassis","Rackswitch","ThinkServer","Storage","Rack-Tower"]
                    if type not in type_list:
                        raise Exception("Invalid Type Specified")
                    if type == "ThinkServer": type = "Lenovo ThinkServer"
                    elif type == "Storage": type = "Lenovo Storage"
                    elif type == "Rack-Tower": type = "Rack-Tower Server"
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
                url = url + '/unmanageRequest/jobs/' + str(jobid)
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

    def get_updatepolicy(self,url, session,policy,info):
        url = url + '/compliancePolicies'
        try:
            if info:
                if info == "FIRMWARE":
                    url = url + "/applicableFirmware"
                elif info == "RESULTS":
                    url = url + "/persistedResult"

            resp = session.get(url,verify=False, timeout=3)
            resp.raise_for_status()
            return resp

        except HTTPError as re:
            logger.error("Exception occured: %s",re)
            raise re

    def get_updaterepo(self,url, session,key):
        url = url + '/updateRepositories/firmware'
        try:
            if not key  == None \
                    and key == "supportedMts" or key == "size" \
                    or key == "lastRefreshed" or key == "importDir" \
                    or key == "publicKeys" or key == "updates" \
                    or key == "updatesByMt" or key == "updatesByMtByComp":
                url= url + "?key=" + key
            else:
                raise Exception("Invalid argument key")
            resp = session.get(url,verify=False, timeout=3)
            resp.raise_for_status()
            return resp

        except HTTPError as re:
            logger.error("Exception occured: %s",re)
            raise re

    def do_updatecomp(self,url, session,mode,action,server,switch,storage,cmm):
        serverlist = list()
        storagelist = list()
        cmmlist = list()
        switchlist = list()

        url = url + '/updatableComponents'
        try:

            if mode == None and action == None and server == None and  switch == None and storage == None and cmm == None :
                resp = session.get(url,verify=False, timeout=3)
                resp.raise_for_status()
                return resp

            if action == "apply" or action == "cancelApply" :
                
                url= url + "?action=" + action
                
                if not mode  == None and mode == "immediate" or mode == "delayed" :
                    url= url + "&mode=" + mode
                else:
                    raise Exception("Invalid argument mode")
        
                if server and len(server.split(","))==3:
                    server_data = server.split(",")
                    serverlist = [{"UUID": server_data[0],"Components": [{"Fixid": server_data[1],"Component": server_data[2]}]}]
    
                if switch and len(switch.split(","))==3:
                    switch_data = switch.split(",")
                    switchlist = [{"UUID": switch_data[0],"Components": [{"Fixid": switch_data[1],"Component": switch_data[2]}]}]
    
                if storage and len(storage.split(","))==3:
                    storage_data = storage.split(",")
                    storagelist = [{"UUID": storage_data[0],"Components": [{"Fixid": storage_data[1],"Component": storage_data[2]}]}]
    
                if cmm and len(cmm.split(","))==3:
                    cmm_data = cmm.split(",")
                    cmmlist = [{"UUID": cmm_data[0],"Components": [{"Fixid": cmm_data[1],"Component": cmm_data[2]}]}]
    
            elif action == "power" : 
                url= url + "?action=" + "powerState"
                
                if server and len(server.split(","))==2:
                    server_data = server.split(",")
                    serverlist = [{"UUID": server_data[0],"PowerState": server_data[1]}]
    
                if switch and len(switch.split(","))==2:
                    switch_data = switch.split(",")
                    switchlist = [{"UUID": switch_data[0],"PowerState": switch_data[1]}]
                
                if storage and len(storage.split(","))==2:
                    storage_data = storage.split(",")
                    storagelist = [{"UUID": storage_data[0],"PowerState": storage_data[1]}]
        
                if cmm and len(cmm.split(","))==2:
                    cmm_data = cmm.split(",")
                    cmmlist = [{"UUID": cmm_data[0],"PowerState": cmm_data[1]}]
                
            param_dict = dict()
            if serverlist:param_dict["ServerList"] = serverlist
            if storagelist:param_dict["StorageList"] = storagelist
            if cmmlist:param_dict["CMMList"] = cmmlist
            if switchlist:param_dict["SwitchList"] = switchlist

            payload = dict()
            payload["DeviceList"] = [param_dict]
            
            resp = session.put(url,data = json.dumps(payload),verify=False, timeout=3)
            resp.raise_for_status()
            return resp

        except HTTPError as re:
            logger.error("Exception occured: %s",re)
            raise re

    def get_configprofiles(self,url, session, profileid):
        url = url + '/profiles'
        
        if profileid:
            url = url + '/' + profileid

        try:
            resp = session.get(url, verify=False, timeout=3)
            resp.raise_for_status()
        except HTTPError as re:
            raise re
    
        return resp