'''
@since: 31 March 2016 
@author: Prashant Bhosale <pbhosale@lenovo.com>
@license: Lenovo License
@copyright: Copyright 2016, Lenovo
@organization: Lenovo 
@summary: Test Script for PyLXCA
'''
import sys
try:
    import pylxca 
except Exception as e:
    print "pyLXCA is not installed correctly"
    print "ERROR MSG ", str(e)
    sys.exit()

from pylxca.pylxca_cmd.lxca_pyshell import *
pyshell()

ip      = 'https://10.243.13.231'
user    = 'USERID'
passwd  = 'CME44ibm'
no_verify   = 'True'

# create a connection object

try:
    conn = connect(ip, user, passwd, no_verify)
    if conn == None:
        print " check with LXCA credential"
        sys.exit()
    print 'LXCA connection successful'    
except Exception as e:
    print   "LXCA connection error, please check lxca connection"
    print   "ERROR MSG ", str(e)


# collectin managed chassis info
chassisList = chassis(conn, status = 'managed')
num_chassis = len(chassisList['chassisList'])

print   'number of managed chassis: ', num_chassis

for c in chassisList['chassisList']:
    print   '------'
    print   'status: %s, model: %s, Health: %s, Name: %s, uuid: %s' \
            %(c['status'], c['model'], c['cmmHealthState'], c['name'], c['uuid'])
    print   'nodes in chassis [%s], %s: ' %(c['name'], str(len(c['nodes'])))        

# collection of managed compute nodes

compute_nodes = nodes(conn, status = 'managed')

print ''
print ''
print 'managed compute nodes'
for cnodes in compute_nodes['nodeList']:
    print   '------'
    print 'name: %s, heath: %s, ipaddress: %s' \
            %( cnodes['name'], cnodes['overallHealthState'], cnodes['ipv4Addresses'])

print 'End'   

